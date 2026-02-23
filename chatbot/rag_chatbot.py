import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

def run_chatbot(report_text, patient_profile):

    # Check API Key
    if "GROQ_API_KEY" not in st.secrets:
        st.error("Groq API Key not found. Please add it to secrets.toml")
        return

    # Initialize Groq LLM
    llm = ChatGroq(
        temperature=0.1,
        model="llama-3.1-8b-instant",
        groq_api_key=st.secrets["GROQ_API_KEY"]
    )

    # Maintain Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if user_input := st.chat_input("Ask a question about your report or diet..."):

        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            system_prompt = f"""
            You are an AI clinical nutrition assistant.

            Patient:
            {patient_profile}

            Report Summary:
            {report_text[:1000]}

            Instructions:
            - Answer clearly and briefly.
            - Consider sugar, cholesterol, BMI, and risk.
            - If food is risky, suggest safer alternatives.'
            """

            messages = [SystemMessage(content=system_prompt)]

            for m in st.session_state.messages[-2:]:
                if m["role"] == "user":
                    messages.append(HumanMessage(content=m["content"]))
                else:
                    messages.append(AIMessage(content=m["content"]))

            try:
                response = llm.invoke(messages)
                full_response = response.content
                st.markdown(full_response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

            except Exception as e:
                st.error(f"AI Error: {str(e)}")