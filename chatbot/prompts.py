def generate_greeting():
    return "👋 Hello! I’m TalentScout, your AI Hiring Assistant. Let’s get started with a few quick questions."

def get_info_prompt(field):
    prompts = {
        "name": "Please enter your full name.",
        "email": "What's your email address?",
        "phone": "Can you share your phone number?",
        "experience": "How many years of experience do you have?",
        "position": "What position(s) are you interested in?",
        "location": "Where are you currently based?",
        "tech_stack": "Please list the technologies you're familiar with (languages, frameworks, tools)."
    }
    return prompts.get(field, "Please provide the requested information.")

def generate_tech_questions(tech_stack):
    return f"Based on your tech stack ({tech_stack}), here are a few questions to assess your skills."

def end_conversation_check(user_input):
    return any(x in user_input.lower() for x in ["exit", "quit", "bye", "thank you"])
