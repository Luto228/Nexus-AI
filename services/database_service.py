import aiosqlite

DB_PATH = 'data/database.db'

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                value REAL NOT NULL,
                category TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
        await db.commit()

async def add_record(user_id, type, value, category):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO records (user_id, type, value, category) VALUES (?, ?, ?, ?)", (user_id, type, value, category))
        await db.commit()

async def get_record(user_id, type, category):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT SUM(value) FROM records WHERE user_id = ? AND category = ? AND type = ?", 
        (user_id, category, type)) as cursor:
            row = await cursor.fetchone()
            if row and row[0] is not None:
                total = row[0]
                return total
            else:
                total = 0
                return total