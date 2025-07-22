import requests
import os

def query_llm(messages):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❗ GROQ_API_KEY is not set in environment variables.")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 1024
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"❗ Groq API Error {response.status_code}: {response.text}")
