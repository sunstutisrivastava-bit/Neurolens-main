import sqlite3
import random
from datetime import datetime

class NeuroChallenges:
    def __init__(self):
        self.challenges = [
            {
                'id': 1,
                'name': 'Smile Tracker',
                'description': 'Hold a genuine smile for 10 seconds',
                'type': 'image',
                'target_emotion': 'happy',
                'duration': 10,
                'reward': 10,
                'feedback': 'Beautiful! You just activated your mirror neurons. Smiling releases dopamine — your happiness hormone!'
            },
            {
                'id': 2,
                'name': 'Calm Control',
                'description': 'Stay calm and neutral for 15 seconds',
                'type': 'image',
                'target_emotion': 'neutral',
                'duration': 15,
                'reward': 15,
                'feedback': 'Excellent! You achieved emotional calm. Your vagus nerve thanks you.'
            },
            {
                'id': 3,
                'name': 'Expression Match',
                'description': 'Match the target emotion shown',
                'type': 'image',
                'target_emotion': 'surprised',
                'duration': 5,
                'reward': 20,
                'feedback': 'You nailed it! That expression recharges your emotional intelligence score.'
            }
        ]
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect('neurolens.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            coins INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            last_challenge DATE
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS challenge_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            challenge_id INTEGER,
            completed INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        conn.close()
    
    def get_daily_challenge(self):
        return random.choice(self.challenges)
    
    def verify_challenge(self, challenge_id, detected_emotion, duration_met):
        challenge = next((c for c in self.challenges if c['id'] == challenge_id), None)
        if not challenge:
            return False
        return detected_emotion == challenge['target_emotion'] and duration_met
    
    def complete_challenge(self, user_id, challenge_id):
        challenge = next((c for c in self.challenges if c['id'] == challenge_id), None)
        if not challenge:
            return None
        
        conn = sqlite3.connect('neurolens.db')
        c = conn.cursor()
        
        # Update user stats
        c.execute('SELECT coins, streak FROM user_stats WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        
        if result:
            new_coins = result[0] + challenge['reward']
            new_streak = result[1] + 1
            c.execute('UPDATE user_stats SET coins = ?, streak = ?, last_challenge = ? WHERE user_id = ?',
                     (new_coins, new_streak, datetime.now().date(), user_id))
        else:
            new_coins = challenge['reward']
            new_streak = 1
            c.execute('INSERT INTO user_stats (user_id, coins, streak, last_challenge) VALUES (?, ?, ?, ?)',
                     (user_id, new_coins, new_streak, datetime.now().date()))
        
        # Log challenge completion
        c.execute('INSERT INTO challenge_logs (user_id, challenge_id, completed) VALUES (?, ?, 1)',
                 (user_id, challenge_id))
        
        conn.commit()
        conn.close()
        
        return {
            'coins_earned': challenge['reward'],
            'total_coins': new_coins,
            'streak': new_streak,
            'feedback': challenge['feedback']
        }
    
    def get_user_stats(self, user_id):
        conn = sqlite3.connect('neurolens.db')
        c = conn.cursor()
        c.execute('SELECT coins, streak FROM user_stats WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        
        c.execute('SELECT COUNT(*) FROM challenge_logs WHERE user_id = ? AND completed = 1', (user_id,))
        completed = c.fetchone()[0]
        
        conn.close()
        
        if result:
            return {'coins': result[0], 'streak': result[1], 'completed': completed}
        return {'coins': 0, 'streak': 0, 'completed': 0}
