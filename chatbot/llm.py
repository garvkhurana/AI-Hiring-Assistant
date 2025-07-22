import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_MODEL = "llama3-8b-8192"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def query_llm(messages, temperature=0.3):
    """
    Query the Groq LLM API with proper error handling
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please set your API key.")
    
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    try:
        response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        response_data = response.json()
        
        # Check if the response has the expected structure
        if "choices" not in response_data or not response_data["choices"]:
            raise ValueError("Invalid response structure from Groq API")
        
        return response_data["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        raise Exception("Request to Groq API timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise Exception("Invalid Groq API key. Please check your API key.")
        elif response.status_code == 429:
            raise Exception("Rate limit exceeded. Please wait a moment and try again.")
        else:
            raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error occurred: {e}")
    except KeyError as e:
        raise Exception(f"Unexpected response format from Groq API: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")