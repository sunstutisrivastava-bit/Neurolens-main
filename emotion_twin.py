import sqlite3
from datetime import datetime, timedelta
from collections import Counter

class EmotionTwin:
    def __init__(self):
        self.emotion_colors = {
            'sad': '#4FC3F7',
            'happy': '#FFD54F',
            'angry': '#EF5350',
            'neutral': '#90A4AE',
            'surprised': '#FFD54F',
            'fear': '#BA68C8'
        }
    
    def get_emotion_profile(self, user_id):
        """Build user's emotional fingerprint"""
        conn = sqlite3.connect('neurolens.db')
        c = conn.cursor()
        
        # Get last 7 days of emotions
        c.execute('''SELECT emotion, timestamp FROM emotion_logs 
                     WHERE user_id = ? AND datetime(timestamp) >= datetime('now', '-7 days')
                     ORDER BY timestamp DESC''', (user_id,))
        emotions = c.fetchall()
        conn.close()
        
        if not emotions:
            return None
        
        emotion_counts = Counter([e[0] for e in emotions])
        total = len(emotions)
        
        return {
            'dominant_emotion': emotion_counts.most_common(1)[0][0],
            'emotion_distribution': {k: round(v/total*100, 1) for k, v in emotion_counts.items()},
            'total_logs': total,
            'recent_emotion': emotions[0][0] if emotions else 'neutral'
        }
    
    def twin_response(self, user_id, user_message=None):
        """Generate personalized twin response based on emotion history"""
        profile = self.get_emotion_profile(user_id)
        
        if not profile:
            return {
                'message': "I'm still learning about you. Let me observe your emotions for a bit.",
                'color': self.emotion_colors['neutral'],
                'suggestion': None
            }
        
        recent = profile['recent_emotion']
        dominant = profile['dominant_emotion']
        sad_count = profile['emotion_distribution'].get('sad', 0)
        
        # Generate response based on patterns
        if sad_count > 40:
            return {
                'message': f"I've noticed you've been feeling down {sad_count}% of the time lately. Want to try a mood boost?",
                'color': self.emotion_colors['sad'],
                'suggestion': 'breathing'
            }
        elif recent == 'sad' and sad_count > 20:
            return {
                'message': "You seem low right now, and I've seen this pattern before. A short walk might help reset your energy.",
                'color': self.emotion_colors['sad'],
                'suggestion': 'break'
            }
        elif recent == 'angry':
            return {
                'message': "I sense some tension. Based on your patterns, a 2-minute breathing exercise usually helps you.",
                'color': self.emotion_colors['angry'],
                'suggestion': 'breathing'
            }
        elif recent == 'happy':
            return {
                'message': f"I love seeing that smile! You've been happy {profile['emotion_distribution'].get('happy', 0)}% of the time. Keep it up!",
                'color': self.emotion_colors['happy'],
                'suggestion': None
            }
        elif recent == 'fear':
            return {
                'message': "You seem stressed. Let's try a relaxation session - it's worked for you before.",
                'color': self.emotion_colors['fear'],
                'suggestion': 'relaxation'
            }
        else:
            return {
                'message': f"Your dominant emotion lately has been {dominant}. Want to check your weekly reflection?",
                'color': self.emotion_colors.get(dominant, '#90A4AE'),
                'suggestion': 'forecast'
            }
    
    def get_weekly_reflection(self, user_id):
        """Generate weekly mood summary"""
        conn = sqlite3.connect('neurolens.db')
        c = conn.cursor()
        
        c.execute('''SELECT emotion, timestamp FROM emotion_logs 
                     WHERE user_id = ? AND datetime(timestamp) >= datetime('now', '-7 days')''', (user_id,))
        emotions = c.fetchall()
        conn.close()
        
        if not emotions:
            return "Not enough data yet. Keep using NeuroLens!"
        
        emotion_counts = Counter([e[0] for e in emotions])
        happiest = emotion_counts.get('happy', 0)
        saddest = emotion_counts.get('sad', 0)
        
        summary = f"This week, I observed {len(emotions)} emotional moments. "
        
        if happiest > saddest:
            summary += f"You seemed happiest {happiest} times! "
        else:
            summary += f"You had {saddest} low moments. "
        
        # Time-based insights
        morning_emotions = [e for e in emotions if 6 <= datetime.fromisoformat(e[1]).hour < 12]
        evening_emotions = [e for e in emotions if 18 <= datetime.fromisoformat(e[1]).hour < 24]
        
        if morning_emotions:
            morning_mood = Counter([e[0] for e in morning_emotions]).most_common(1)[0][0]
            summary += f"Mornings were mostly {morning_mood}. "
        
        if evening_emotions:
            evening_mood = Counter([e[0] for e in evening_emotions]).most_common(1)[0][0]
            summary += f"Evenings were mostly {evening_mood}."
        
        return summary
