import sqlite3
from datetime import datetime
import uuid
import base64

class EmotionAnchors:
    def __init__(self, db_path='neurolens.db'):
        self.db_path = db_path
        self._init_db()
        self.positive_emotions = ['happy', 'joyful', 'calm', 'euphoric', 'surprised']
        self.color_map = {
            'happy': '#FFD166',
            'joyful': '#00F5D4',
            'calm': '#06D6A0',
            'euphoric': '#00F5FF',
            'surprised': '#FFD54F'
        }
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS emotion_anchors
                     (id TEXT PRIMARY KEY, user_id INTEGER, emotion TEXT, 
                      color TEXT, image_data TEXT, note TEXT, 
                      confidence REAL, created_at TEXT)''')
        conn.commit()
        conn.close()
    
    def should_create_anchor(self, emotion, confidence):
        return emotion in self.positive_emotions and confidence > 0.8
    
    def create_anchor(self, user_id, emotion, confidence, image_data, note=''):
        anchor_id = str(uuid.uuid4())
        color = self.color_map.get(emotion, '#00F5FF')
        created_at = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO emotion_anchors 
                     (id, user_id, emotion, color, image_data, note, confidence, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (anchor_id, user_id, emotion, color, image_data, note, confidence, created_at))
        conn.commit()
        conn.close()
        
        return {'id': anchor_id, 'emotion': emotion, 'color': color}
    
    def get_anchors(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT id, emotion, color, note, created_at 
                     FROM emotion_anchors WHERE user_id=? 
                     ORDER BY created_at DESC''', (user_id,))
        anchors = [{'id': r[0], 'emotion': r[1], 'color': r[2], 'note': r[3], 'created_at': r[4]} 
                   for r in c.fetchall()]
        conn.close()
        return anchors
    
    def get_anchor(self, anchor_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT emotion, color, image_data, note, created_at 
                     FROM emotion_anchors WHERE id=?''', (anchor_id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                'emotion': row[0],
                'color': row[1],
                'image_data': row[2],
                'note': row[3],
                'created_at': row[4]
            }
        return None
    
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
