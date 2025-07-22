# 🤖 TalentScout – AI Hiring Assistant Chatbot

TalentScout is an AI-powered hiring assistant chatbot built using **Llama 3 via the Groq API**, designed to streamline the candidate screening process. It collects candidate details like name, email, phone, experience, role, location, and tech stack, then automatically generates relevant technical questions.

---

## 🌟 Features

- 📋 Collects structured candidate information.
- 🧠 Automatically generates 3–5 technical questions based on tech stack.
- 🌍 Multilingual Prompt Support (English, Hindi, French, Spanish, etc.)
- 💬 Real-time conversation powered by Groq's Llama-3 API.
- 🎨 Colorful and responsive Streamlit UI.
- 🧠 Context retained and shown in sidebar.
- ✅ No "Go Ahead" input needed — smooth transition to questions.

---

## 🧠 Tech Stack

| Component    | Technology               |
|--------------|---------------------------|
| UI           | [Streamlit](https://streamlit.io)         |
| LLM          | [LLaMA 3](https://huggingface.co/meta-llama) via [Groq API](https://console.groq.com/) |
| Language     | Python 3.8+               |
| Deployment   | Localhost|
| Style        | Custom HTML/CSS in Streamlit |
| Persistence  | JSON file (`data/candidate_data.json`) |



## 🛠 Installation Guide

### 1. ✅ Clone the Repository

bash"""
git clone https://github.com/your-username/talent-scout-chatbot.git

cd talent-scout-chatbot"""

2. ✅ Install Required Python Libraries
bash
"""pip install -r requirements.txt"""

🔐 Fetching Your Groq API Key
Go to: https://console.groq.com/keys

Sign up or log in.

Click “Create API Key” and copy it.

Paste it into the Streamlit sidebar when prompted.

🔒 Your key is only used locally and never stored.

▶️ Running the App
bash
"""streamlit run app.py"""

Then open http://localhost:8501 in your browser.


📦 Output Storage
All candidate responses are saved in:
data/candidate_data.json
Each candidate's data is stored as a new JSON line for easy parsing or future analytics.

🧪 Example Flow
You enter your Groq API key.

Bot asks: “What is your name?”

Bot collects all other information (email, phone, etc.).

It automatically generates technical questions based on the candidate’s tech stack.

You answer, and it continues the LLM chat.

💡 Future Improvements

🎯 Admin dashboard for reviewing all candidates.

✉️ Email summaries or CSV export.

🌐 Language auto-detection.

📊 Scoring candidate responses using AI.



