import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
import uuid

# Initialize Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize embedding model
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Initialize ChromaDB
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="medical_rag",
    embedding_function=embedding_function
)


class RAGChat:

    def add_context(self, session_id: str, report_text: str, diet_plan: str):

        documents = [
            f"Medical Report:\n{report_text}",
            f"Diet Plan:\n{diet_plan}"
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

    def query_context(self, session_id: str, query: str):

        results = collection.query(
            query_texts=[query],
            n_results=2,
            where={"session_id": session_id}
        )

        if results and results["documents"]:
            return "\n\n".join(results["documents"][0])

        return ""

    def chat(self, session_id: str, user_message: str):

        context = self.query_context(session_id, user_message)

        prompt = f"""
You are a medical nutrition assistant.

Use the following context to answer:

{context}

User question:
{user_message}

Answer clearly and safely.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        return response.choices[0].message.content.strip()


rag_chat = RAGChat()
