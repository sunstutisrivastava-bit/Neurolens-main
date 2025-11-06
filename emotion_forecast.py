import sqlite3
from datetime import datetime, timedelta
from collections import Counter
import statistics

class EmotionForecast:
    def __init__(self, db_path='neurolens.db'):
        self.db_path = db_path
    
    def get_emotion_logs(self, user_id, days=7):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        c.execute('SELECT emotion, timestamp FROM emotion_logs WHERE user_id=? AND timestamp > ? ORDER BY timestamp',
                  (user_id, cutoff))
        logs = c.fetchall()
        conn.close()
        return logs
    
    def extract_features(self, logs):
        if len(logs) < 3:
            return None
        
        emotions = [log[0] for log in logs]
        positive = ['happy', 'calm', 'surprised', 'joyful']
        negative = ['sad', 'angry', 'fear', 'stressed']
        
        positive_count = sum(1 for e in emotions if e in positive)
        positive_ratio = positive_count / len(emotions)
        
        changes = sum(1 for i in range(1, len(emotions)) if emotions[i] != emotions[i-1])
        volatility = changes / len(emotions)
        
        emotion_counts = Counter(emotions)
        dominant = emotion_counts.most_common(1)[0][0]
        
        return {
            'positive_ratio': positive_ratio,
            'volatility': volatility,
            'dominant_emotion': dominant,
            'total_logs': len(emotions)
        }
    
    def predict_tomorrow(self, user_id):
        logs = self.get_emotion_logs(user_id, days=7)
        features = self.extract_features(logs)
        
        if not features:
            return {
                'forecast': 'neutral',
                'confidence': 0.5,
                'emoji': '😐',
                'weather': '🌤️',
                'recommendation': 'Start logging emotions to get personalized forecasts!'
            }
        
        # Simple rule-based prediction
        if features['positive_ratio'] > 0.7:
            forecast = 'happy'
            emoji = '😊'
            weather = '☀️'
            rec = 'Your outlook is bright! Capture your good mood with journaling.'
            confidence = 0.85
        elif features['positive_ratio'] < 0.3:
            forecast = 'sad'
            emoji = '😔'
            weather = '🌧️'
            rec = 'Plan self-care early and take a short evening walk.'
            confidence = 0.78
        elif features['volatility'] > 0.6:
            forecast = 'stressed'
            emoji = '😰'
            weather = '⛈️'
            rec = 'High emotional shifts detected. Try grounding exercises.'
            confidence = 0.72
        else:
            forecast = 'calm'
            emoji = '😌'
            weather = '🌤️'
            rec = 'Perfect for reflection or reading.'
            confidence = 0.68
        
        return {
            'forecast': forecast,
            'confidence': round(confidence, 2),
            'emoji': emoji,
            'weather': weather,
            'recommendation': rec
        }
    
    def get_3day_forecast(self, user_id):
        logs = self.get_emotion_logs(user_id, days=14)
        features = self.extract_features(logs)
        
        if not features:
            return [
                {'day': 'Today', 'mood': 'neutral', 'emoji': '😐', 'weather': '🌤️', 'tip': 'Start logging emotions!'},
                {'day': 'Tomorrow', 'mood': 'neutral', 'emoji': '😐', 'weather': '🌤️', 'tip': 'Keep tracking your mood.'},
                {'day': 'Day After', 'mood': 'neutral', 'emoji': '😐', 'weather': '🌤️', 'tip': 'Build your emotional data.'}
            ]
        
        # Generate 3-day forecast with slight variations
        base = self.predict_tomorrow(user_id)
        
        forecasts = [
            {
                'day': 'Today',
                'mood': features['dominant_emotion'],
                'emoji': base['emoji'],
                'weather': base['weather'],
                'tip': 'Current emotional state detected.'
            },
            {
                'day': 'Tomorrow',
                'mood': base['forecast'],
                'emoji': base['emoji'],
                'weather': base['weather'],
                'tip': base['recommendation']
            }
        ]
        
        # Day after tomorrow - slight trend continuation
        if features['positive_ratio'] > 0.6:
            forecasts.append({
                'day': 'Day After',
                'mood': 'happy',
                'emoji': '😊',
                'weather': '☀️',
                'tip': 'Positive trend continuing!'
            })
        else:
            forecasts.append({
                'day': 'Day After',
                'mood': 'calm',
                'emoji': '😌',
                'weather': '🌥️',
                'tip': 'Stabilizing period ahead.'
            })
        
        return forecasts
