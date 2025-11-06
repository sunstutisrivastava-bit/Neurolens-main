from datetime import datetime, timedelta
from collections import defaultdict
import statistics

class MoodForecast:
    def __init__(self):
        self.emotion_scores = {
            'happy': 5, 'joyful': 5, 'excited': 4,
            'neutral': 3, 'calm': 3,
            'sad': 1, 'angry': 2, 'anxious': 2, 'fear': 1, 'stressed': 2, 'tired': 2
        }
        
        self.warnings = {
            'sunday_evening': "You seem more stressed every Sunday evening — take some time for relaxation today.",
            'monday_morning': "Monday mornings tend to be tough for you. Start with something you enjoy!",
            'declining_trend': "I've noticed your mood declining over the past few days. Consider reaching out to someone you trust.",
            'low_weekend': "Your weekend mood has been lower than usual. Plan something enjoyable for next weekend.",
            'evening_dip': "Your mood tends to drop in the evenings. Try a calming routine before bed.",
            'stress_pattern': "You show increased stress during {day}s. Consider scheduling lighter tasks on these days.",
            'depressive_cycle': "⚠️ Warning: Detecting a potential depressive pattern. Please consider talking to a mental health professional."
        }
    
    def analyze_mood_history(self, emotion_logs):
        """Analyze emotion history and generate forecast"""
        if not emotion_logs:
            return None
        
        # Organize data by time patterns
        by_day_of_week = defaultdict(list)
        by_time_of_day = defaultdict(list)
        daily_averages = []
        
        for log in emotion_logs:
            username, emotion, confidence, timestamp = log
            dt = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else timestamp
            
            score = self.emotion_scores.get(emotion.lower(), 3) * confidence
            
            # Group by day of week
            day_name = dt.strftime('%A')
            by_day_of_week[day_name].append(score)
            
            # Group by time of day
            hour = dt.hour
            if 5 <= hour < 12:
                time_period = 'morning'
            elif 12 <= hour < 17:
                time_period = 'afternoon'
            elif 17 <= hour < 21:
                time_period = 'evening'
            else:
                time_period = 'night'
            by_time_of_day[time_period].append(score)
            
            # Daily average
            daily_averages.append((dt.date(), score))
        
        # Generate insights
        insights = self._generate_insights(by_day_of_week, by_time_of_day, daily_averages)
        
        return insights
    
    def _generate_insights(self, by_day, by_time, daily_data):
        """Generate actionable insights from patterns"""
        insights = {
            'warnings': [],
            'patterns': [],
            'recommendations': [],
            'risk_level': 'low'
        }
        
        # Analyze day of week patterns
        day_averages = {day: statistics.mean(scores) for day, scores in by_day.items() if scores}
        
        if day_averages:
            lowest_day = min(day_averages, key=day_averages.get)
            if day_averages[lowest_day] < 2.5:
                insights['warnings'].append(self.warnings['stress_pattern'].format(day=lowest_day))
                insights['patterns'].append(f"Low mood detected on {lowest_day}s (avg: {day_averages[lowest_day]:.1f}/5)")
        
        # Check for Sunday evening stress
        if 'Sunday' in day_averages and day_averages['Sunday'] < 2.8:
            insights['warnings'].append(self.warnings['sunday_evening'])
        
        # Check for Monday morning blues
        if 'Monday' in day_averages and day_averages['Monday'] < 2.5:
            insights['warnings'].append(self.warnings['monday_morning'])
        
        # Analyze time of day patterns
        time_averages = {time: statistics.mean(scores) for time, scores in by_time.items() if scores}
        
        if 'evening' in time_averages and time_averages['evening'] < 2.5:
            insights['warnings'].append(self.warnings['evening_dip'])
            insights['recommendations'].append("Create a calming evening routine: dim lights, avoid screens, try meditation.")
        
        # Analyze trends (last 7 days)
        if len(daily_data) >= 7:
            recent_data = daily_data[-7:]
            recent_scores = [score for _, score in recent_data]
            
            # Check for declining trend
            if len(recent_scores) >= 3:
                first_half = statistics.mean(recent_scores[:len(recent_scores)//2])
                second_half = statistics.mean(recent_scores[len(recent_scores)//2:])
                
                if second_half < first_half - 0.5:
                    insights['warnings'].append(self.warnings['declining_trend'])
                    insights['risk_level'] = 'medium'
                    insights['recommendations'].append("Schedule time with friends or family this week.")
            
            # Check for consistently low mood (potential depression)
            avg_recent = statistics.mean(recent_scores)
            if avg_recent < 2.0:
                insights['warnings'].append(self.warnings['depressive_cycle'])
                insights['risk_level'] = 'high'
                insights['recommendations'].extend([
                    "Consider speaking with a mental health professional.",
                    "Reach out to a trusted friend or family member.",
                    "National Suicide Prevention Lifeline: 988"
                ])
        
        # Positive patterns
        if day_averages:
            best_day = max(day_averages, key=day_averages.get)
            if day_averages[best_day] > 4.0:
                insights['patterns'].append(f"You feel best on {best_day}s! Try to schedule enjoyable activities then.")
        
        # General recommendations based on overall mood
        if daily_data:
            overall_avg = statistics.mean([score for _, score in daily_data])
            
            if overall_avg < 3.0:
                insights['recommendations'].extend([
                    "Maintain a regular sleep schedule (7-9 hours).",
                    "Exercise for 20-30 minutes daily, even a short walk helps.",
                    "Practice gratitude: write down 3 good things each day."
                ])
            elif overall_avg >= 4.0:
                insights['patterns'].append("Your overall mood is positive! Keep up your current routines.")
        
        return insights
    
    def get_daily_forecast(self, emotion_logs):
        """Get forecast for today based on historical patterns"""
        today = datetime.now()
        day_name = today.strftime('%A')
        hour = today.hour
        
        if hour < 12:
            time_period = 'morning'
        elif hour < 17:
            time_period = 'afternoon'
        elif hour < 21:
            time_period = 'evening'
        else:
            time_period = 'night'
        
        forecast = {
            'day': day_name,
            'time': time_period,
            'prediction': 'neutral',
            'confidence': 0.7,
            'advice': ''
        }
        
        # Analyze historical data for this day/time
        if emotion_logs:
            same_day_scores = []
            for log in emotion_logs:
                username, emotion, confidence, timestamp = log
                dt = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else timestamp
                
                if dt.strftime('%A') == day_name:
                    score = self.emotion_scores.get(emotion.lower(), 3)
                    same_day_scores.append(score)
            
            if same_day_scores:
                avg_score = statistics.mean(same_day_scores)
                
                if avg_score >= 4:
                    forecast['prediction'] = 'positive'
                    forecast['advice'] = f"{day_name}s are usually good for you! Enjoy your day."
                elif avg_score < 2.5:
                    forecast['prediction'] = 'challenging'
                    forecast['advice'] = f"{day_name}s can be tough. Be kind to yourself today."
                    forecast['confidence'] = 0.8
                else:
                    forecast['advice'] = f"Your {day_name} mood is typically balanced. Stay mindful."
        
        return forecast
    
    def get_weekly_outlook(self, emotion_logs):
        """Get mood outlook for the upcoming week"""
        outlook = {
            'summary': '',
            'watch_days': [],
            'good_days': [],
            'tips': []
        }
        
        if not emotion_logs:
            return outlook
        
        # Analyze by day of week
        by_day = defaultdict(list)
        for log in emotion_logs:
            username, emotion, confidence, timestamp = log
            dt = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else timestamp
            day_name = dt.strftime('%A')
            score = self.emotion_scores.get(emotion.lower(), 3)
            by_day[day_name].append(score)
        
        day_averages = {day: statistics.mean(scores) for day, scores in by_day.items() if scores}
        
        for day, avg in day_averages.items():
            if avg < 2.5:
                outlook['watch_days'].append(day)
            elif avg >= 4.0:
                outlook['good_days'].append(day)
        
        if outlook['watch_days']:
            outlook['summary'] = f"Watch out for: {', '.join(outlook['watch_days'])}. Plan self-care activities."
            outlook['tips'].append("Schedule lighter workload on challenging days.")
        
        if outlook['good_days']:
            outlook['tips'].append(f"Leverage your energy on {', '.join(outlook['good_days'])} for important tasks.")
        
        return outlook
