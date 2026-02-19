import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
import os

# ---------------- INITIALIZE GROQ ----------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- EMBEDDING MODEL ----------------
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# ---------------- CHROMA DB ----------------
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="medical_rag",
    embedding_function=embedding_function
)


class RAGChat:

    # ------------------------------------------------
    # Add report + diet context (only once per session)
    # ------------------------------------------------
    def add_context(self, session_id: str, report_text: str, diet_plan: str):

        documents = [
            report_text[:3000],   # limit report size
            diet_plan[:2000]      # limit diet size
        ]

        ids = [
            f"{session_id}_report",
            f"{session_id}_diet"
        ]

        metadatas = [
            {"session_id": session_id, "type": "report"},
            {"session_id": session_id, "type": "diet"}
        ]

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    # ------------------------------------------------
    # Retrieve only relevant small context
    # ------------------------------------------------
    def query_context(self, session_id: str, query: str):

        results = collection.query(
            query_texts=[query],
            n_results=1,  # reduce token usage
            where={"session_id": session_id}
        )

        if results and results["documents"]:
            context = results["documents"][0][0]
            return context[:1500]  # truncate context

        return ""

    # ------------------------------------------------
    # Chat with optimized prompt
    # ------------------------------------------------
    def chat(self, session_id: str, user_message: str):

        context = self.query_context(session_id, user_message)

        prompt = f"""
You are a medical nutrition assistant.

Use the context below if relevant.
If not relevant, answer generally but safely.

Context:
{context}

Question:
{user_message}

Give short, clear, safe answer (max 5-6 sentences).
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # correct model name
                messages=[
                    {"role": "system", "content": "You are a professional medical nutrition assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,      # reduced tokens
                temperature=0.5      # stable answers
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return "⚠️ AI service temporarily unavailable. Please try again later."


# Create global instance
rag_chat = RAGChat()
