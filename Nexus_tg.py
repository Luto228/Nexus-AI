import asyncio
import json

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message

from config.env import BOT_TOKEN
from core.ai_engine import send_prompt

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello! I'm your personal assistant. How can I help you today?")

@dp.message()
async def send_message(message: Message):
    try:
        response = send_prompt.full_prompt(message.text)
        action = response.get("action", "please retry again with a clear prompt.")
        answer = response.get("answer", "No answer provided.")
    except (ValueError, json.JSONDecodeError, KeyError) as e:
        await message.answer(f"Error: {e}")
        return
    if action == "chat":
        await message.answer(answer)
    elif action == "reminder":
        await message.answer(answer)
        try:
            time = response.get("time", "please provide a valid time.")
            target = response.get("target", "please provide a valid target.")
        except KeyError as e:
            await message.answer(f"Error: {e}")
            return
    elif action == "database":
        await message.answer(answer)
        try:
            db_type = response.get("type", "please provide a valid type.")
            value = response.get("value", "please provide a valid value.")
            category = response.get("category", "please provide a valid category.")
        except KeyError as e:
            await message.answer(f"Error: {e}")
            return
        
if __name__ == '__main__':
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')