import sqlite3
import hashlib
from datetime import datetime

def init_db():
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        parent_id INTEGER,
        user_type TEXT DEFAULT 'child',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Emotion logs table
    c.execute('''CREATE TABLE IF NOT EXISTS emotion_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        emotion TEXT NOT NULL,
        confidence REAL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Chat logs table
    c.execute('''CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        response TEXT NOT NULL,
        sentiment TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, role, parent_id=None, user_type='child'):
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password, role, parent_id, user_type) VALUES (?, ?, ?, ?, ?)',
                  (username, hash_password(password), role, parent_id, user_type))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    c.execute('SELECT id, role, parent_id, user_type FROM users WHERE username = ? AND password = ?',
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result

def log_emotion(user_id, emotion, confidence):
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    c.execute('INSERT INTO emotion_logs (user_id, emotion, confidence) VALUES (?, ?, ?)',
              (user_id, emotion, confidence))
    conn.commit()
    conn.close()

def log_chat(user_id, message, response, sentiment):
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    c.execute('INSERT INTO chat_logs (user_id, message, response, sentiment) VALUES (?, ?, ?, ?)',
              (user_id, message, response, sentiment))
    conn.commit()
    conn.close()

def get_child_emotions(parent_id):
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    c.execute('''SELECT u.username, e.emotion, e.confidence, e.timestamp 
                 FROM emotion_logs e 
                 JOIN users u ON e.user_id = u.id 
                 WHERE u.parent_id = ? 
                 ORDER BY e.timestamp DESC LIMIT 100''', (parent_id,))
    results = c.fetchall()
    conn.close()
    return results

def get_child_chats(parent_id):
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    c.execute('''SELECT u.username, c.message, c.response, c.sentiment, c.timestamp 
                 FROM chat_logs c 
                 JOIN users u ON c.user_id = u.id 
                 WHERE u.parent_id = ? 
                 ORDER BY c.timestamp DESC LIMIT 50''', (parent_id,))
    results = c.fetchall()
    conn.close()
    return results

def get_children(parent_id):
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    c.execute('SELECT id, username FROM users WHERE parent_id = ?', (parent_id,))
    results = c.fetchall()
    conn.close()
    return results

init_db()