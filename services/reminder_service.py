import aiosqlite

DB_PATH = 'reminder.db'

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                time TEXT NOT NULL,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )''')
        await db.commit()

async def add_reminder(user_id, time, task):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO reminders (user_id, time, task) VALUES (?, ?, ?)", 
            (user_id, time, task)
        )
        await db.commit()

async def get_pending_reminders():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT id, user_id, time, task FROM reminders WHERE status = 'pending'") as cursor:
            return await cursor.fetchall()

async def update_status(reminder_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE reminders SET status = 'done' WHERE id = ?", (reminder_id,))
        await db.commit()