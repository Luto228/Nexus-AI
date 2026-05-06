import requests
import json
import datetime
from config.env import GEMINI_API_KEY

class Aibrain:
    def __init__(self):
        self.model_name = 'gemini-2.0-flash'
        self.version = 'v1beta'
        self.api_key = GEMINI_API_KEY
        self.url = f'https://generativelanguage.googleapis.com/{self.version}/models/{self.model_name}:generateContent?key={self.api_key}'

        self.system_prompt = """Understand what exactly the message is about options:
    Structure:
        "Chat": {"action": "chat", "answer": "text"},
        "Reminder": {"action": "reminder", "target": "task", "time": "HH:MM", "answer": "text"},
        "Database": {"action": "database", "type": "expense/income/fact", "value": "val", "category": "cat", "answer": "text"},
        "Error": {"action": "Error", "type": "Logical/Impossible", "solution": "text"}

    Rules:
        1. Always start with "action".
        2. "time" must ALWAYS be in HH:MM format.
        3. If the user mentions a day/date but NOT a specific time, set "time" to "12:00" by default.
        4. If the user uses relative words (tomorrow, next Monday, in 2 hours), calculate the result HH:MM based on the Current date and time provided above.
        5. If data is missing (e.g., no task or no date/time at all), ask for it in "answer".
        6. No explanations outside JSON.
"""

    def full_prompt(self, user_prompt):
        now = datetime.datetime.now()
        date_context = f"Current date and time: {now.strftime('%Y-%m-%d %H:%M, %A')}\n"
        
        total_prompt = date_context + self.system_prompt + "\nUser message: " + user_prompt
        
        payload = {
            "contents": [
                {
                    "parts": [{"text": total_prompt}]
                }
            ]
        }
        
        print(f"DEBUG URL: |{self.url}|") 
        print(f"DEBUG PAYLOAD: {json.dumps(payload, indent=2)}")

        headers = {'Content-Type': 'application/json'}

        bot_request = requests.post(self.url, json=payload, headers=headers)
        
        if bot_request.status_code == 200:
            try:
                full_response = bot_request.json()
                action_response = full_response['candidates'][0]['content']['parts'][0]['text']
                
                clean_json = action_response.replace('```json', '').replace('```', '').strip()
                
                return json.loads(clean_json)
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                raise ValueError(f"AI processing error: {e}")
        else:
            raise ValueError(f"An error occurred: {bot_request.status_code} - {bot_request.text}")

send_prompt = Aibrain()