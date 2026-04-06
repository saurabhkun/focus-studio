import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "focus_studio.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            display_name TEXT,
            avatar_color TEXT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            streak INTEGER DEFAULT 0,
            last_study_date TEXT,
            total_minutes INTEGER DEFAULT 0,
            created_at TEXT
        )
    ''')

    # sessions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            duration_minutes INTEGER,
            session_type TEXT,
            date TEXT,
            xp_earned INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # tasks table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            task_text TEXT,
            due_date TEXT,
            is_done INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # badges table
    c.execute('''
        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            badge_key TEXT,
            earned_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # friends table
    c.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            friend_id INTEGER,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(friend_id) REFERENCES users(id)
        )
    ''')
    
    # messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            content TEXT,
            sent_at TEXT,
            is_read INTEGER DEFAULT 0,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id)
        )
    ''')
    
    # classrooms table
    c.execute('''
        CREATE TABLE IF NOT EXISTS classrooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            subject TEXT,
            created_by INTEGER,
            join_code TEXT UNIQUE,
            created_at TEXT,
            FOREIGN KEY(created_by) REFERENCES users(id)
        )
    ''')
    
    # classroom_members table
    c.execute('''
        CREATE TABLE IF NOT EXISTS classroom_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            classroom_id INTEGER,
            user_id INTEGER,
            role TEXT,
            joined_at TEXT,
            FOREIGN KEY(classroom_id) REFERENCES classrooms(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # classroom_messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS classroom_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            classroom_id INTEGER,
            user_id INTEGER,
            content TEXT,
            sent_at TEXT,
            FOREIGN KEY(classroom_id) REFERENCES classrooms(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# Generic execution wrappers
def fetch_one(query, params=()):
    conn = get_connection()
    c = conn.cursor()
    c.execute(query, params)
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def fetch_all(query, params=()):
    conn = get_connection()
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def execute_query(query, params=()):
    conn = get_connection()
    c = conn.cursor()
    c.execute(query, params)
    lastrowid = c.lastrowid
    conn.commit()
    conn.close()
    return lastrowid

# Example Specific Helpers
def get_user_by_username(username):
    return fetch_one("SELECT * FROM users WHERE username = ?", (username,))

def get_user_by_id(user_id):
    return fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))

def create_user(username, password_hash, display_name, avatar_color):
    created_at = datetime.now().isoformat()
    return execute_query('''
        INSERT INTO users (username, password_hash, display_name, avatar_color, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password_hash, display_name, avatar_color, created_at))

def update_user_stats(user_id, xp_gain, minutes_gain):
    execute_query('''
        UPDATE users 
        SET xp = xp + ?, total_minutes = total_minutes + ?
        WHERE id = ?
    ''', (xp_gain, minutes_gain, user_id))

def get_user_badges(user_id):
    return fetch_all("SELECT badge_key, earned_at FROM badges WHERE user_id = ?", (user_id,))
    
def add_badge(user_id, badge_key):
    # Check if badge already exists
    existing = fetch_one("SELECT id FROM badges WHERE user_id = ? AND badge_key = ?", (user_id, badge_key))
    if not existing:
        earned_at = datetime.now().isoformat()
        execute_query("INSERT INTO badges (user_id, badge_key, earned_at) VALUES (?, ?, ?)", (user_id, badge_key, earned_at))

def get_tasks(user_id):
    return fetch_all("SELECT * FROM tasks WHERE user_id = ? ORDER BY is_done ASC, created_at DESC", (user_id,))

# Initialize on import
init_db()
