import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.env import BOT_TOKEN
from core.ai_engine import send_prompt
from services.reminder_service import add_reminder, get_pending_reminders, update_status, init_db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def check_reminders():
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        pending_reminders = await get_pending_reminders(current_time)
        
        for r_id, u_id, r_time, r_task in pending_reminders:
            try:
                await bot.send_message(u_id, f"Reminder: {r_task}!")
                await update_status(r_id)
            except Exception as e:
                print(f"Send error: {e}")
        
        await asyncio.sleep(30)

async def main():
    await init_db()
    
    asyncio.create_task(check_reminders())
    
    print("Bot is starting...")
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello! I'm your personal assistant. How can I help you today?")

@dp.message()
async def handle_message(message: Message):
    try:
        response = await send_prompt.full_prompt(message.text)
        
        action = response.get("action", "Error")
        answer = response.get("answer", "No answer provided.")

        if action == "chat":
            await message.answer(answer)
            
        elif action == "reminder":
            time = response.get("time", "12:00")
            task = response.get("target", "Task")
            
            await add_reminder(user_id=message.from_user.id, time=time, task=task)
            await message.answer(answer)
            
        elif action == "database":
            await message.answer(answer)
            print("Database action requested")
            
        elif action == "Error":
            solution = response.get("solution", "Please try again with a clearer prompt.")
            await message.answer(f"Error: {solution}")

    except Exception as e:
        await message.answer(f"An error occurred: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
    