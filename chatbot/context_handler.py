from chatbot.prompts import get_info_prompt, generate_tech_questions
from chatbot.llm import query_llm
import json
import os
import re

class ChatContext:
    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI Hiring Assistant working for a global tech recruitment agency. "
                    "Please interact in the candidate's preferred language if possible (supports English, Hindi, Spanish, French, etc). "
                    "Your job is to collect details like name, email, phone, experience, desired position, location, and tech stack. "
                    "After that, generate 3–5 relevant technical questions based on their stack. Remain professional but friendly. "
                    "Always ask one question at a time and ensure clarity. "
                    "If the candidate provides invalid input, politely ask them to try again. "
                    "Stay professional and don't chat casually."
                )
            }
        ]
        self.started = False
        self.data = {
            "name": None,
            "email": None,
            "phone": None,
            "experience": None,
            "position": None,
            "location": None,
            "tech_stack": None
        }
        self.stage = 0
        self.questions_triggered = False

    def get_bot_response(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

        
        if self.stage < len(self.data):
            key = list(self.data.keys())[self.stage]
            if self._is_valid_input(key, user_input):
                self.data[key] = user_input.strip()
                self.stage += 1

                if self.stage < len(self.data):
                    next_key = list(self.data.keys())[self.stage]
                    prompt = get_info_prompt(next_key)
                    self.messages.append({"role": "assistant", "content": prompt})
                    return prompt
                else:
                    
                    save_candidate_data(self.data)
                    tech_prompt = generate_tech_questions(self.data["tech_stack"])
                    self.messages.append({"role": "assistant", "content": tech_prompt})
                    self.questions_triggered = True
                    return tech_prompt
            else:
                retry = f"❗ Invalid {key.replace('_', ' ')}. Please try again."
                self.messages.append({"role": "assistant", "content": retry})
                return retry

        # LLM chat continues after questions
        response = query_llm(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response

    def end(self):
        self.messages.append({"role": "assistant", "content": "🙏 Thank you and goodbye!"})

    def _is_valid_input(self, key, value):
        value = value.strip()
        if key == "email":
            return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))
        elif key == "phone":
            return bool(re.match(r"^\d{10}$", value))
        elif key == "experience":
            return value.isdigit() and int(value) < 50
        elif key in ["name", "position", "location", "tech_stack"]:
            return len(value) > 1
        return True

    def start(self):
        first_key = list(self.data.keys())[self.stage]
        prompt = get_info_prompt(first_key)
        self.messages.append({"role": "assistant", "content": prompt})
        return prompt

def save_candidate_data(data):
    os.makedirs("data", exist_ok=True)
    with open("data/candidate_data.json", "a") as f:
        json.dump(data, f)
        f.write("\n")
