import sqlite3

db = sqlite3.connect('reminder.db')
cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    time TEXT NOT NULL,
    task TEXT NOT NULL,
    status TEXT DEFAULT 'pending'
    )''')

def add_reminder(user_id, time, task):
    cursor.execute("INSERT INTO reminders (user_id, time, task) VALUES (?, ?, ?)", (user_id, time, task))
    db.commit()
def get_status():
    cursor.execute("SELECT * FROM reminders WHERE status = 'pending'")
    fetchall_pending = cursor.fetchall()
    return fetchall_pending
def update_status(id):
    cursor.execute("UPDATE reminders SET status = 'done' WHERE id = ?", (id,))