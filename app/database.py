import sqlite3
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "pocketsmart.db"

def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c=conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS recommendations(
      id TEXT PRIMARY KEY,
      username TEXT NOT NULL,
      recommendation_type TEXT NOT NULL,
      input_summary TEXT NOT NULL,
      full_result TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    """)
    c.commit(); c.close()

def create_user(username,email,password_hash):
    c=conn()
    try:
        c.execute("INSERT INTO users(username,email,password_hash,created_at) VALUES(?,?,?,?)",
                  (username,email,password_hash,datetime.now(timezone.utc).isoformat()))
        c.commit(); return True
    except sqlite3.IntegrityError:
        return False
    finally: c.close()

def get_user(username):
    c=conn(); r=c.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone(); c.close()
    return dict(r) if r else None

def add_recommendation(rid,username,kind,summary,result):
    c=conn(); c.execute("INSERT INTO recommendations VALUES(?,?,?,?,?,?)",
        (rid,username,kind,summary,result,datetime.now(timezone.utc).isoformat())); c.commit(); c.close()

def list_recommendations(username):
    c=conn(); rows=c.execute("SELECT * FROM recommendations WHERE username=? ORDER BY created_at DESC",(username,)).fetchall(); c.close()
    return [dict(r) for r in rows]

def get_recommendation(rid,username):
    c=conn(); r=c.execute("SELECT * FROM recommendations WHERE id=? AND username=?",(rid,username)).fetchone(); c.close()
    return dict(r) if r else None
