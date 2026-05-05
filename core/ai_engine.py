from config.env import GEMINI_API_KEY
import requests
import json

class Aibrain:
    def __init__(self):
        self.ai_model = "gemini-2.0-flash" 
        self.api_key = GEMINI_API_KEY
        self.url = f'https://generativelanguage.googleapis.com/v1/models/{self.ai_model}:generateContent?key={self.api_key}'
        self.system_prompt = """understand what exactly the message is about options:
    Structure:
        Chat: {"action": "chat", "answer": "text"}

        Reminder: {"action": "reminder", "target": "task", "time": "time", "answer": "text"}

        Database: {"action": "database", "type": "expense/income/fact", "value": "val", "category": "cat", "answer": "text"}

        Rules:
            Always start with "action".
            If data is missing, ask for it in "answer".
            No explanations outside JSON."""
    def full_prompt(self, user_prompt):
        self.user_prompt = user_prompt
        total_prompt = self.system_prompt + self.user_prompt
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": total_prompt
                        }
                    ]
                }
            ]
        }
        bot_request = requests.post(self.url, json=payload)
        if bot_request.status_code == 200:
            try:
                full_response = bot_request.json()
                action_response = full_response['candidates'][0]['content']['parts'][0]['text']
                action_json = json.loads(action_response)
                return action_json
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                raise ValueError("An error occurred while decoding the response.")
        else:
            raise ValueError(f"An error occurred: {bot_request.status_code} - {bot_request.text}")
send_prompt = Aibrain()
