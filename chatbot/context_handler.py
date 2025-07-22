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
                    "You are an AI Hiring Assistant working for a tech recruitment agency. "
                    "Collect candidate details (name, email, phone, experience, position, location, tech stack). "
                    "Then ask 3–5 technical questions based on their declared stack. Stay professional and don't chat casually."
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
        self.ready_for_questions = False
        self.questions_generated = False

    def get_bot_response(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

        
        if user_input.lower().strip() == "go ahead" and self.ready_for_questions:
            return self._generate_questions()

        
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
                    
                    self._save_candidate_data()
                    self.ready_for_questions = True
                    return "✅ All details collected successfully! Please click the button below to proceed to technical questions."
            else:
                
                retry_msg = self._get_validation_error(key, user_input)
                self.messages.append({"role": "assistant", "content": retry_msg})
                return retry_msg

        
        if self.questions_generated:
            response = f"Thank you for your answer: '{user_input}'\n\nPlease continue with the next question or let me know when you're done."
            self.messages.append({"role": "assistant", "content": response})
            return response

        
        try:
            response = query_llm(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            error_msg = f"I'm having trouble processing your request. Error: {str(e)}"
            self.messages.append({"role": "assistant", "content": error_msg})
            return error_msg

    def _generate_questions(self):
        """Generate technical questions based on tech stack"""
        tech_prompt = generate_tech_questions(self.data["tech_stack"])
        self.messages.append({"role": "assistant", "content": tech_prompt})
        self.ready_for_questions = False
        self.questions_generated = True
        return tech_prompt

    def _get_validation_error(self, key, value):
        """Get appropriate validation error message"""
        if key == "email":
            return " Please enter a valid email address (e.g., john@example.com)."
        elif key == "phone":
            return " Please enter a valid 10-digit phone number (numbers only)."
        elif key == "experience":
            return " Please enter your years of experience as a number (0-49)."
        elif key in ["name", "position", "location", "tech_stack"]:
            return f" Please enter a valid {key.replace('_', ' ')} (at least 2 characters)."
        return " Invalid input. Please try again."

    def end(self):
        self.messages.append({"role": "assistant", "content": "Thank you for your time! Have a great day! 👋"})

    def _is_valid_input(self, key, value):
        """Validate user input based on field type"""
        if not value or not value.strip():
            return False
            
        value = value.strip()
        
        if key == "email":
            
            return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))
        elif key == "phone":
            
            clean_phone = re.sub(r'[^\d]', '', value)
            return len(clean_phone) == 10 and clean_phone.isdigit()
        elif key == "experience":
            
            try:
                exp = int(value)
                return 0 <= exp < 50
            except ValueError:
                return False
        elif key in ["name", "position", "location", "tech_stack"]:
            return len(value) >= 2
        return True

    def start(self):
        """Start the conversation by asking for the first piece of info"""
        first_key = list(self.data.keys())[self.stage]
        prompt = get_info_prompt(first_key)
        self.messages.append({"role": "assistant", "content": prompt})
        return prompt

    def _save_candidate_data(self):
        """Save candidate data to JSON file"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/candidate_data.json", "a", encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False)
                f.write("\n")
        except Exception as e:
            print(f"Warning: Could not save candidate data: {e}")


def save_candidate_data(data):
    """Legacy function for backward compatibility"""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/candidate_data.json", "a", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")
    except Exception as e:
        print(f"Warning: Could not save candidate data: {e}")