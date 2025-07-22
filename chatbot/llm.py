import os
import requests
from dotenv import load_dotenv
load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def query_llm(messages, temperature=0.3):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
