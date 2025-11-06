import sqlite3
from datetime import datetime, date
import uuid
import base64

class EmotionAnchors:
    def __init__(self, db_path='neurolens.db'):
        self.db_path = db_path
        self._init_db()
        self.color_map = {
            'happy': '#FFD166',
            'sad': '#118AB2',
            'angry': '#EF5350',
            'neutral': '#90A4AE',
            'surprised': '#FFD54F',
            'fear': '#9B5DE5',
            'calm': '#06D6A0'
        }
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS emotion_anchors
                     (id TEXT PRIMARY KEY, user_id INTEGER, emotion TEXT, 
                      color TEXT, image_data TEXT, note TEXT, 
                      confidence REAL, created_at TEXT, capture_date TEXT)''')
        conn.commit()
        conn.close()
    
    def can_create_anchor_today(self, user_id):
        today = date.today().isoformat()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT COUNT(*) FROM emotion_anchors 
                     WHERE user_id=? AND capture_date=?''', (user_id, today))
        count = c.fetchone()[0]
        conn.close()
        return count < 10
    
    def create_anchor(self, user_id, emotion, confidence, image_data, note=''):
        if not self.can_create_anchor_today(user_id):
            return {'error': 'Daily limit reached (10 photos per day)'}
        
        anchor_id = str(uuid.uuid4())
        color = self.color_map.get(emotion, '#00F5FF')
        created_at = datetime.now().isoformat()
        capture_date = date.today().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO emotion_anchors 
                     (id, user_id, emotion, color, image_data, note, confidence, created_at, capture_date)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (anchor_id, user_id, emotion, color, image_data, note, confidence, created_at, capture_date))
        conn.commit()
        conn.close()
        
        return {'id': anchor_id, 'emotion': emotion, 'color': color, 'success': True}
    
    def get_anchors(self, user_id, limit=100):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT id, emotion, color, note, created_at, capture_date 
                     FROM emotion_anchors WHERE user_id=? 
                     ORDER BY created_at DESC LIMIT ?''', (user_id, limit))
        anchors = [{'id': r[0], 'emotion': r[1], 'color': r[2], 'note': r[3], 
                    'created_at': r[4], 'capture_date': r[5]} 
                   for r in c.fetchall()]
        conn.close()
        return anchors
    
    def get_daily_count(self, user_id):
        today = date.today().isoformat()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT COUNT(*) FROM emotion_anchors 
                     WHERE user_id=? AND capture_date=?''', (user_id, today))
        count = c.fetchone()[0]
        conn.close()
        return count
    
    def get_anchor(self, anchor_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT emotion, color, image_data, note, created_at, capture_date 
                     FROM emotion_anchors WHERE id=?''', (anchor_id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                'emotion': row[0],
                'color': row[1],
                'image_data': row[2],
                'note': row[3],
                'created_at': row[4],
                'capture_date': row[5]
            }
        return None
    
    def update_anchor_note(self, anchor_id, note):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''UPDATE emotion_anchors SET note=? WHERE id=?''', (note, anchor_id))
        conn.commit()
        conn.close()
        return {'success': True}
    
    def get_random_positive_anchor(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT id, emotion, color, note 
                     FROM emotion_anchors WHERE user_id=? 
                     ORDER BY RANDOM() LIMIT 1''', (user_id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return {'id': row[0], 'emotion': row[1], 'color': row[2], 'note': row[3]}
        return None
