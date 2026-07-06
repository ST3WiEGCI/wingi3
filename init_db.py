import sqlite3

conn = sqlite3.connect("rlcoach.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS replays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    replay_id TEXT UNIQUE,
    location TEXT,
    local_file TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database ready: rlcoach.db")