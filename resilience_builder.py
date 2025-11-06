import sqlite3
from datetime import datetime, timedelta
import statistics

class ResilienceBuilder:
    def __init__(self, db_path='neurolens.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS resilience_metrics
                     (user_id INTEGER, week_start TEXT, score REAL, 
                      volatility REAL, recovery_speed REAL, positive_ratio REAL,
                      PRIMARY KEY (user_id, week_start))''')
        c.execute('''CREATE TABLE IF NOT EXISTS weekly_goals
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
                      week_start TEXT, goal_text TEXT, completed INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()
    
    def calculate_resilience_score(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get last 7 days of emotions
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        c.execute('''SELECT emotion, timestamp FROM emotion_logs 
                     WHERE user_id=? AND timestamp > ? ORDER BY timestamp''',
                  (user_id, week_ago))
        logs = c.fetchall()
        conn.close()
        
        if len(logs) < 3:
            return {'score': 30, 'volatility': 0.5, 'recovery_speed': 0.3, 'positive_ratio': 0.4, 'tree_state': 'sprout'}
        
        emotions = [log[0] for log in logs]
        
        # Calculate metrics
        positive_emotions = ['happy', 'calm', 'surprised']
        negative_emotions = ['sad', 'angry', 'fear', 'stressed']
        
        positive_count = sum(1 for e in emotions if e in positive_emotions)
        positive_ratio = positive_count / len(emotions)
        
        # Volatility: how often emotion changes
        changes = sum(1 for i in range(1, len(emotions)) if emotions[i] != emotions[i-1])
        volatility = changes / len(emotions) if len(emotions) > 1 else 0.5
        
        # Recovery speed: time from negative to positive
        recovery_times = []
        for i in range(len(emotions)-1):
            if emotions[i] in negative_emotions and emotions[i+1] in positive_emotions:
                recovery_times.append(1)
        recovery_speed = len(recovery_times) / max(1, sum(1 for e in emotions if e in negative_emotions))
        
        # Calculate resilience score (0-100)
        score = (positive_ratio * 0.4 + recovery_speed * 0.3 + (1 - volatility) * 0.3) * 100
        
        # Determine tree state
        if score < 30:
            tree_state = 'sprout'
        elif score < 60:
            tree_state = 'sapling'
        elif score < 80:
            tree_state = 'young_tree'
        else:
            tree_state = 'flourishing'
        
        return {
            'score': round(score, 1),
            'volatility': round(volatility, 2),
            'recovery_speed': round(recovery_speed, 2),
            'positive_ratio': round(positive_ratio, 2),
            'tree_state': tree_state
        }
    
    def save_weekly_metrics(self, user_id, metrics):
        week_start = datetime.now().strftime('%Y-%W')
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO resilience_metrics 
                     (user_id, week_start, score, volatility, recovery_speed, positive_ratio)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, week_start, metrics['score'], metrics['volatility'],
                   metrics['recovery_speed'], metrics['positive_ratio']))
        conn.commit()
        conn.close()
    
    def generate_weekly_goal(self, user_id, metrics):
        score = metrics['score']
        recovery = metrics['recovery_speed']
        positive = metrics['positive_ratio']
        
        if recovery > 0.7:
            goal = "You've bounced back faster this week — try one gratitude reflection today."
        elif positive > 0.6:
            goal = "You stayed positive 3 days in a row — celebrate with a reward sound 🎵."
        elif metrics['volatility'] > 0.6:
            goal = "Mood swings increased — do a 2-min grounding exercise."
        elif score < 40:
            goal = "Start small: take 3 deep breaths when you feel overwhelmed."
        else:
            goal = "Keep building resilience — try a 5-minute mindfulness break today."
        
        week_start = datetime.now().strftime('%Y-%W')
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO weekly_goals (user_id, week_start, goal_text) VALUES (?, ?, ?)',
                  (user_id, week_start, goal))
        conn.commit()
        conn.close()
        
        return goal
    
    def get_weekly_trend(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT week_start, score FROM resilience_metrics 
                     WHERE user_id=? ORDER BY week_start DESC LIMIT 4''', (user_id,))
        data = c.fetchall()
        conn.close()
        return [{'week': d[0], 'score': d[1]} for d in reversed(data)]
