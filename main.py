import asyncio
import json
import datetime

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message

from config.env import BOT_TOKEN
from core.ai_engine import send_prompt
from services.reminder_service import add_reminder, get_status, update_status

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()

async def check_reminders():
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        fetchall_pending = get_status()
        for user_pending in fetchall_pending:
            reminder_id = user_pending[0]
            user_id = user_pending[1]
            time = user_pending[2]
            task = user_pending[3]
            if time == current_time:
                await bot.send_message(user_id, f"Reminder: {task}!")
                update_status(reminder_id)
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(check_reminders())
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
    except Exception as e:
        await message.answer(f"Error: {e}")
        return
    if action == "chat":
        await message.answer(answer)
    elif action == "reminder":
        await message.answer(answer)
        try:
            add_reminder(user_id=message.from_user.id, time = response.get("time", "No time provided"), task = response.get("target", "No task provided"))
        except Exception as e:
            await message.answer(f"Error: {e}")
            return
    elif action == "database":
        await message.answer(answer)
        try:
            print("Nothing for now")
        except Exception as e:
            await message.answer(f"Error: {e}")
            return
        
if __name__ == '__main__':
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')