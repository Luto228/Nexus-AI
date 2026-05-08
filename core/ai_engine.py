import datetime
import json
import google.generativeai as genai
from config.env import GEMINI_API_KEY

class Aibrain:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )

        self.system_prompt = """You are a helpful assistant. Understand the user's intent and return ONLY a JSON object.
    Options:
    - If user just wants to talk (e.g., "hi", "how are you", "привет"):
      {"action": "chat", "answer": "your friendly response here"}
      
    - If user wants to set a reminder (e.g., "remind me to drink water at 5pm"):
      {"action": "reminder", "target": "task description", "time": "HH:MM", "answer": "Confirmation message"}
      
    - If user talks about money/facts (e.g., "spent 5$ on coffee"):
      {"action": "database", "type": "expense/income/fact", "value": "val", "category": "cat", "answer": "Confirmation message"}

    Rules:
    1. ALWAYS return valid JSON. No markdown, no "```json".
    2. If the message is a simple greeting or talk, ALWAYS use "action": "chat".
    3. Use "time" format HH:MM. Default time is 12:00.
    4. Current date context is provided above. Calculate relative times correctly.
    5. If you truly don't understand, use "action": "chat" and ask for clarification in "answer" instead of returning an error.
"""

    async def full_prompt(self, user_prompt):
        now = datetime.datetime.now()
        date_context = f"Current date and time: {now.strftime('%Y-%m-%d %H:%M, %A')}\n"
        
        total_prompt = f"{date_context}\n{self.system_prompt}\n\nUser message: {user_prompt}"

        response = await self.model.generate_content_async(total_prompt)
        
        try:
            return json.loads(response.text)
        except (json.JSONDecodeError, AttributeError) as e:
            raise ValueError(f"AI JSON error: {e} | Raw: {response.text}")

send_prompt = Aibrain()