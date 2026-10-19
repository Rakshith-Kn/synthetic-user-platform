import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def get_llm():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set in the .env file"
        )

    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0.8,
        google_api_key=api_key
    )