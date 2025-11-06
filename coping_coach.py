import sqlite3
from datetime import datetime
import random

class CopingCoach:
    def __init__(self, db_path='neurolens.db'):
        self.db_path = db_path
        self._init_db()
        self.coping_actions = {
            'sad': [
                {'type': 'reflection', 'title': 'Gratitude Moment', 'text': 'Write one line about what went well today.', 'duration': 60},
                {'type': 'physical', 'title': 'Gentle Movement', 'text': 'Stand up and stretch your arms above your head for 30 seconds.', 'duration': 30},
                {'type': 'affirmation', 'title': 'Self-Compassion', 'text': 'Say to yourself: "This feeling is temporary. I am doing my best."', 'duration': 30}
            ],
            'angry': [
                {'type': 'breathing', 'title': 'Calm Breathing', 'text': 'Breathe out slowly for 10 seconds. Let the tension go.', 'duration': 60},
                {'type': 'physical', 'title': 'Release Tension', 'text': 'Clench your fists tight for 5 seconds, then release. Repeat 3 times.', 'duration': 45},
                {'type': 'distraction', 'title': 'Mental Break', 'text': 'Count backwards from 100 by 7s to reset your mind.', 'duration': 60}
            ],
            'fear': [
                {'type': 'breathing', 'title': 'Box Breathing', 'text': 'Inhale 4s, hold 4s, exhale 4s, hold 4s. Repeat 4 times.', 'duration': 64},
                {'type': 'grounding', 'title': '5 Senses Grounding', 'text': 'Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.', 'duration': 90},
                {'type': 'affirmation', 'title': 'Safety Reminder', 'text': 'Say: "I am safe right now. This moment is okay."', 'duration': 30}
            ],
            'stressed': [
                {'type': 'breathing', 'title': 'Deep Breathing', 'text': 'Take 5 deep breaths. Inhale through nose, exhale through mouth.', 'duration': 60},
                {'type': 'physical', 'title': 'Shoulder Release', 'text': 'Roll your shoulders back 5 times, then forward 5 times.', 'duration': 30},
                {'type': 'reflection', 'title': 'Priority Check', 'text': 'Write down the ONE most important thing right now.', 'duration': 60}
            ],
            'anxious': [
                {'type': 'breathing', 'title': '4-7-8 Breathing', 'text': 'Inhale 4s, hold 7s, exhale 8s. Repeat 3 times.', 'duration': 57},
                {'type': 'grounding', 'title': 'Body Scan', 'text': 'Notice your feet on the floor. Feel your body in the chair. You are here.', 'duration': 45},
                {'type': 'distraction', 'title': 'Mental Shift', 'text': 'Name 5 blue things you can see around you right now.', 'duration': 30}
            ]
        }
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS coping_actions
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
                      emotion_before TEXT, coping_type TEXT, coping_title TEXT,
                      emotion_after TEXT, created_at TEXT)''')
        conn.commit()
        conn.close()
    
    def should_suggest(self, emotion):
        negative_emotions = ['sad', 'angry', 'fear', 'stressed', 'anxious']
        return emotion in negative_emotions
    
    def get_coping_action(self, emotion):
        actions = self.coping_actions.get(emotion, self.coping_actions['stressed'])
        return random.choice(actions)
    
    def log_action(self, user_id, emotion_before, coping_type, coping_title, emotion_after=''):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO coping_actions 
                     (user_id, emotion_before, coping_type, coping_title, emotion_after, created_at)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, emotion_before, coping_type, coping_title, emotion_after, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_history(self, user_id, limit=10):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT emotion_before, coping_title, emotion_after, created_at 
                     FROM coping_actions WHERE user_id=? 
                     ORDER BY created_at DESC LIMIT ?''', (user_id, limit))
        history = [{'emotion_before': r[0], 'coping_title': r[1], 'emotion_after': r[2], 'created_at': r[3]} 
                   for r in c.fetchall()]
        conn.close()
        return history
