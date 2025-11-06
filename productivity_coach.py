import random
from datetime import datetime, timedelta

class ProductivityCoach:
    def __init__(self):
        self.last_break_time = datetime.now()
        self.stress_count = 0
        self.fatigue_count = 0
        self.work_session_start = datetime.now()
        
        self.micro_breaks = [
            "Take a 2-minute break: Stand up, stretch your arms above your head, and roll your shoulders.",
            "Quick eye break: Look at something 20 feet away for 20 seconds (20-20-20 rule).",
            "Desk stretch: Interlace fingers, push palms away from you, and hold for 10 seconds.",
            "Neck relief: Gently tilt your head to each side, holding for 5 seconds.",
            "Stand and walk around your desk for 1 minute to boost circulation."
        ]
        
        self.breathing_exercises = [
            "Box Breathing: Inhale 4 counts → Hold 4 → Exhale 4 → Hold 4. Repeat 4 times.",
            "4-7-8 Technique: Breathe in for 4, hold for 7, exhale slowly for 8. Do 3 cycles.",
            "Deep Belly Breathing: Place hand on belly, breathe deeply so belly rises. 5 breaths.",
            "Alternate Nostril: Close right nostril, inhale left. Switch. Exhale right. Repeat 5x.",
            "Calm Breathing: Breathe in through nose for 3, out through mouth for 6. Repeat 5 times."
        ]
        
        self.focus_music = [
            "🎵 Try: Lo-fi hip hop beats - great for concentration without distraction",
            "🎵 Suggestion: Classical music (Mozart, Bach) - proven to enhance focus",
            "🎵 Listen to: Nature sounds (rain, ocean waves) - calming and focusing",
            "🎵 Try: Binaural beats at 40Hz - supports deep concentration",
            "🎵 Suggestion: Ambient electronic music - minimal lyrics, maximum focus"
        ]
        
        self.productivity_tips = [
            "Pomodoro Technique: Work for 25 minutes, break for 5. You're doing great!",
            "Hydration check: Have you had water in the last hour? Stay hydrated for better focus.",
            "Posture check: Sit up straight, feet flat on floor, screen at eye level.",
            "Task batching: Group similar tasks together to minimize context switching.",
            "Two-minute rule: If a task takes less than 2 minutes, do it now."
        ]
        
        self.stress_relief = [
            "Progressive Muscle Relaxation: Tense and release each muscle group for 5 seconds.",
            "Mindful moment: Close eyes, focus on 3 things you can hear right now.",
            "Quick meditation: Sit quietly, focus on breath for just 2 minutes.",
            "Gratitude pause: Think of 3 things you're grateful for right now.",
            "Visualization: Imagine your favorite peaceful place for 30 seconds."
        ]
    
    def analyze_emotion(self, emotion, confidence=0.8):
        """Analyze emotion and provide productivity coaching"""
        emotion = emotion.lower()
        current_time = datetime.now()
        time_since_break = (current_time - self.last_break_time).total_seconds() / 60
        work_duration = (current_time - self.work_session_start).total_seconds() / 60
        
        response = {
            'alert': False,
            'message': '',
            'suggestions': [],
            'urgency': 'low'
        }
        
        # Detect stress
        if emotion in ['angry', 'anxious', 'stressed', 'frustrated']:
            self.stress_count += 1
            if self.stress_count >= 3:
                response['alert'] = True
                response['urgency'] = 'high'
                response['message'] = "⚠️ I've detected elevated stress levels. Let's take a moment to reset."
                response['suggestions'] = [
                    random.choice(self.breathing_exercises),
                    random.choice(self.stress_relief),
                    "Consider a 5-minute walk to clear your mind."
                ]
                self.stress_count = 0
        
        # Detect fatigue
        elif emotion in ['tired', 'sad', 'bored', 'neutral'] and confidence > 0.7:
            self.fatigue_count += 1
            if self.fatigue_count >= 4 or time_since_break > 50:
                response['alert'] = True
                response['urgency'] = 'medium'
                response['message'] = "💤 You seem fatigued. Time for a quick recharge!"
                response['suggestions'] = [
                    random.choice(self.micro_breaks),
                    "Get some fresh air - even 2 minutes helps!",
                    random.choice(self.focus_music)
                ]
                self.fatigue_count = 0
                self.last_break_time = current_time
        
        # Long work session without break
        elif time_since_break > 60:
            response['alert'] = True
            response['urgency'] = 'medium'
            response['message'] = "⏰ You've been working for over an hour. Break time!"
            response['suggestions'] = [
                random.choice(self.micro_breaks),
                random.choice(self.breathing_exercises),
                "Hydrate: Drink a glass of water."
            ]
            self.last_break_time = current_time
        
        # Positive reinforcement for good emotions
        elif emotion in ['happy', 'focused', 'energetic']:
            if work_duration > 25 and work_duration % 25 < 5:
                response['message'] = "✨ Great focus! Keep up the momentum."
                response['suggestions'] = [random.choice(self.productivity_tips)]
        
        # General productivity tips
        elif time_since_break > 30 and not response['alert']:
            response['message'] = "💡 Productivity tip:"
            response['suggestions'] = [random.choice(self.productivity_tips)]
        
        return response
    
    def get_break_suggestion(self):
        """Get a random break suggestion"""
        return {
            'micro_break': random.choice(self.micro_breaks),
            'breathing': random.choice(self.breathing_exercises),
            'music': random.choice(self.focus_music)
        }
    
    def reset_session(self):
        """Reset work session"""
        self.work_session_start = datetime.now()
        self.last_break_time = datetime.now()
        self.stress_count = 0
        self.fatigue_count = 0
