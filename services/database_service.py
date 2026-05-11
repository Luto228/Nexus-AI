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
        if category.lower() in ["all", "total", "всего"]:
            query = "SELECT SUM(value) FROM records WHERE user_id = ? AND type LIKE ?"
            params = (user_id, f"%{type}%")
        else:
            query = "SELECT SUM(value) FROM records WHERE user_id = ? AND category LIKE ? AND type LIKE ?"
            params = (user_id, f"%{category}%", f"%{type}%")

        async with db.execute(query, params) as cursor:
            row = await cursor.fetchone()
            return row[0] if row and row[0] is not None else 0