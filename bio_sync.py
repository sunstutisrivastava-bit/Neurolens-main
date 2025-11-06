import random

class BioSync:
    def __init__(self):
        pass
    
    def get_simulated_biometrics(self):
        """Simulate biometric data for demo"""
        return {
            'heart_rate': random.randint(60, 100),
            'sleep_hours': round(random.uniform(5, 9), 1),
            'steps': random.randint(1000, 10000)
        }
    
    def compute_mind_health_score(self, emotion, heart_rate, sleep_hours, steps):
        """Calculate overall mind health score"""
        score = 100
        
        # Emotion impact
        if emotion in ['sad', 'angry', 'fear']:
            score -= 20
        elif emotion == 'happy':
            score += 10
        
        # Heart rate factor
        if heart_rate > 100:
            score -= 15
        elif heart_rate < 70:
            score += 5
        
        # Sleep quality
        if sleep_hours < 6:
            score -= 10
        elif sleep_hours > 8:
            score += 5
        
        # Activity level
        if steps < 3000:
            score -= 5
        elif steps > 7000:
            score += 10
        
        return max(0, min(100, score))
    
    def get_wellness_message(self, score):
        """Get message based on mind health score"""
        if score >= 80:
            return {
                'message': "You're glowing — keep it up!",
                'icon': '🌞',
                'color': '#00FF00'
            }
        elif score >= 60:
            return {
                'message': "You're doing fine — take a short stretch.",
                'icon': '🌤',
                'color': '#00BBF9'
            }
        elif score >= 40:
            return {
                'message': "Looks like you need some rest.",
                'icon': '🌥',
                'color': '#9B5DE5'
            }
        else:
            return {
                'message': "High stress detected — let's breathe together.",
                'icon': '🌧',
                'color': '#EF476F'
            }
    
    def get_bio_sync_data(self, emotion):
        """Get complete bio-sync analysis"""
        biometrics = self.get_simulated_biometrics()
        score = self.compute_mind_health_score(
            emotion,
            biometrics['heart_rate'],
            biometrics['sleep_hours'],
            biometrics['steps']
        )
        wellness = self.get_wellness_message(score)
        
        return {
            'emotion': emotion,
            'heart_rate': biometrics['heart_rate'],
            'sleep_hours': biometrics['sleep_hours'],
            'steps': biometrics['steps'],
            'mind_health_score': score,
            'wellness_message': wellness['message'],
            'wellness_icon': wellness['icon'],
            'wellness_color': wellness['color']
        }
