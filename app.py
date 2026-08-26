import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv(override=True)

# Page configuration
st.set_page_config(
    page_title="MindBridge",
    page_icon="🧠",
    layout="centered"
)

# Title
st.title("🧠 MindBridge")
st.subheader("AI Student Support Assistant")

st.write(
    "MindBridge is an AI-powered assistant designed to provide "
    "supportive and context-aware responses to students."
)

# Check API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

# Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("How are you feeling today?")

if user_input:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # MindBridge system prompt
    prompt = f"""
You are MindBridge, an AI student support assistant.

Your purpose is to provide supportive, empathetic, and helpful
responses to students.

Guidelines:
- Be friendly and respectful.
- Listen carefully to the student's concerns.
- Give practical and encouraging suggestions.
- Do not judge the student.
- Keep responses clear and easy to understand.
- Do not claim to be a doctor, therapist, or emergency service.
- If a student appears to be in immediate danger or talks about
  harming themselves, encourage them to contact emergency services,
  a trusted person, or a qualified mental-health professional.

Student message:
{user_input}

Respond naturally and supportively.
"""

    try:
        with st.chat_message("assistant"):
            with st.spinner("MindBridge is thinking..."):
                response = llm.invoke(prompt)
                answer = response.content

            st.markdown(answer)

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error(f"Unable to generate a response: {e}")