import sqlite3
from datetime import datetime, timedelta
from collections import Counter
import random

class MindRooms:
    def __init__(self, db_path='neurolens.db'):
        self.db_path = db_path
        self.rooms = {
            'serenity': {'name': 'Serenity Space', 'emotions': ['calm', 'happy', 'neutral'], 'color': '#4FC3F7', 'sound': 'ocean', 'bpm': 60},
            'ember': {'name': 'Ember Room', 'emotions': ['angry', 'stressed'], 'color': '#EF5350', 'sound': 'heartbeat', 'bpm': 80},
            'hope': {'name': 'Hope Garden', 'emotions': ['sad', 'fear'], 'color': '#BA68C8', 'sound': 'piano', 'bpm': 72},
            'energy': {'name': 'Energy Flow', 'emotions': ['surprised', 'joyful'], 'color': '#FFD54F', 'sound': 'synth', 'bpm': 90}
        }
    
    def get_user_emotion_vector(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        cutoff = (datetime.now() - timedelta(hours=6)).isoformat()
        c.execute('SELECT emotion FROM emotion_logs WHERE user_id=? AND timestamp > ?', (user_id, cutoff))
        emotions = [row[0] for row in c.fetchall()]
        conn.close()
        
        if not emotions:
            return None
        
        emotion_counts = Counter(emotions)
        dominant = emotion_counts.most_common(1)[0][0]
        return dominant
    
    def assign_room(self, user_id):
        emotion = self.get_user_emotion_vector(user_id)
        
        if not emotion:
            return self.rooms['serenity']
        
        for room_id, room_data in self.rooms.items():
            if emotion in room_data['emotions']:
                return room_data
        
        return self.rooms['serenity']
    
    def get_room_participants(self, room_name):
        return random.randint(3, 12)
