 python
    import sqlite3
    import os
    from datetime import datetime
    
    DB_PATH = os.path.expanduser("~/telegram-bot/bot_data.db")
    
    def init_db():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            created_date TEXT,
            status TEXT DEFAULT 'active'
        )""")
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            remind_date TEXT,
            created_date TEXT
        )""")
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mood TEXT,
            note TEXT,
            checkin_date TEXT
        )""")
        
        conn.commit()
        conn.close()
    
    def add_goal(user_id, title, description):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO goals (user_id, title, description, created_date, status) VALUES (?, ?, ?, ?, 'active')",
                     (user_id, title, description, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
    
    def get_goals(user_id):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.execute("SELECT id, title, status FROM goals WHERE user_id = ? AND status != 'completed'", (user_id,))
        rows = cur.fetchall()
        conn.close()
        return rows
    
    def complete_goal(user_id, goal_id):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE goals SET status = 'completed' WHERE id = ? AND user_id = ?", (goal_id, user_id))
        conn.commit()
        conn.close()
    
    def add_checkin(user_id, mood, note):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO checkins (user_id, mood, note, checkin_date) VALUES (?, ?, ?, ?)",
                     (user_id, mood, note, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
    
    def get_recent_checkins(user_id, limit=7):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.execute("SELECT mood, note, checkin_date FROM checkins WHERE user_id = ? ORDER BY checkin_date DESC LIMIT ?", (user_id, limit))
        rows = cur.fetchall()
        conn.close()
        return rows
    
    init_db()
    
    
    5. Onderaan de pagina: bij Commit changes voeg je een bericht toe zoals Voeg storage.py toe
    6. Klik op de groene knop Commit changes
    
    
    

