import random
from datetime import datetime

class RolePersonalization:
    def __init__(self):
        self.student_quotes = [
            "Success is the sum of small efforts repeated day in and day out. - Robert Collier",
            "The expert in anything was once a beginner. Keep going!",
            "Study hard now, shine bright later!",
            "Your future is created by what you do today, not tomorrow.",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "Education is the passport to the future. - Malcolm X"
        ]
        
        self.focus_games = [
            {"name": "Memory Match", "duration": "5 min", "benefit": "Improves concentration"},
            {"name": "Number Sequence", "duration": "3 min", "benefit": "Enhances focus"},
            {"name": "Word Association", "duration": "4 min", "benefit": "Boosts cognitive speed"},
            {"name": "Pattern Recognition", "duration": "5 min", "benefit": "Sharpens attention"}
        ]
        
        self.college_prompts = [
            "Journal Prompt: What's one thing you learned about yourself this week?",
            "Reflection: Describe a moment when you felt proud of yourself recently.",
            "Challenge: Write about a fear you want to overcome this semester.",
            "Gratitude: List 3 people who positively impacted your week.",
            "Growth: What skill do you want to develop in the next month?",
            "Connection: Reach out to one classmate you haven't talked to in a while."
        ]
        
        self.peer_topics = [
            "Study Group: Looking for calculus study buddies!",
            "Mental Health: How do you manage exam stress?",
            "Campus Life: Best spots for quiet studying?",
            "Career: Internship tips and experiences",
            "Wellness: Healthy eating on a student budget",
            "Social: Weekend plans and campus events"
        ]
        
        self.corporate_reminders = [
            "Posture Check: Sit up straight, shoulders back, feet flat on floor.",
            "Eye Break: Look away from screen, focus on something 20 feet away for 20 seconds.",
            "Stretch Break: Roll your shoulders, stretch your neck side to side.",
            "Hydration: Time for a water break! Stay hydrated for better focus.",
            "Movement: Stand up and walk around for 2 minutes.",
            "Breathing: Take 3 deep breaths - in through nose, out through mouth."
        ]
        
        self.mental_resets = [
            "5-Minute Reset: Close eyes, practice box breathing (4-4-4-4).",
            "Quick Walk: Step outside or walk around the office for 3 minutes.",
            "Desk Yoga: Seated spinal twist, neck rolls, shoulder shrugs.",
            "Mindful Moment: Focus on 3 things you can see, hear, and feel.",
            "Power Pose: Stand tall, hands on hips, hold for 2 minutes (confidence boost!).",
            "Gratitude Break: Think of 3 things going well at work today."
        ]
    
    def get_personalized_content(self, role, emotion=None):
        """Get role-specific personalized content"""
        content = {
            'role': role,
            'primary': [],
            'secondary': [],
            'activities': []
        }
        
        if role == 'student':
            content['primary'] = [
                {'type': 'quote', 'content': random.choice(self.student_quotes)},
                {'type': 'game', 'content': random.choice(self.focus_games)}
            ]
            content['secondary'] = [
                "Study Tip: Use the Pomodoro Technique - 25 min study, 5 min break",
                "Focus Boost: Try studying in 90-minute blocks with 15-minute breaks",
                "Memory Hack: Teach what you learned to someone else"
            ]
            
            if emotion in ['stressed', 'anxious']:
                content['activities'].append({
                    'title': 'Quick Study Break',
                    'description': 'Play a 5-minute focus game to reset your mind',
                    'action': 'Start Game'
                })
        
        elif role == 'college':
            content['primary'] = [
                {'type': 'journal', 'content': random.choice(self.college_prompts)},
                {'type': 'peer', 'content': random.choice(self.peer_topics)}
            ]
            content['secondary'] = [
                "Connect: Join a study group or campus club this week",
                "Balance: Schedule both academic and social activities",
                "Self-Care: Don't skip meals or sleep for studying"
            ]
            
            if emotion in ['lonely', 'sad']:
                content['activities'].append({
                    'title': 'Peer Connection',
                    'description': 'Browse the peer connection board and reach out',
                    'action': 'View Board'
                })
            
            content['activities'].append({
                'title': 'Daily Journal',
                'description': 'Take 5 minutes to reflect on your day',
                'action': 'Start Writing'
            })
        
        elif role == 'corporate':
            content['primary'] = [
                {'type': 'posture', 'content': random.choice(self.corporate_reminders)},
                {'type': 'reset', 'content': random.choice(self.mental_resets)}
            ]
            content['secondary'] = [
                "Productivity: Block calendar time for deep work",
                "Wellness: Take all your vacation days - they're important!",
                "Boundaries: Set clear work hours and stick to them"
            ]
            
            if emotion in ['stressed', 'tired', 'frustrated']:
                content['activities'].append({
                    'title': 'Mental Reset Break',
                    'description': '5-minute guided reset to refresh your mind',
                    'action': 'Start Reset'
                })
            
            content['activities'].append({
                'title': 'Posture Check',
                'description': 'Quick ergonomic assessment and adjustment',
                'action': 'Check Now'
            })
        
        return content
    
    def get_daily_challenge(self, role):
        """Get role-specific daily challenge"""
        challenges = {
            'student': [
                "Today's Challenge: Study for 25 minutes without checking your phone",
                "Focus Challenge: Complete one assignment before taking any breaks",
                "Memory Challenge: Review your notes from yesterday's class",
                "Productivity Challenge: Organize your study space before starting"
            ],
            'college': [
                "Social Challenge: Have a meaningful conversation with someone new",
                "Wellness Challenge: Cook a healthy meal instead of ordering out",
                "Academic Challenge: Attend office hours for one of your classes",
                "Growth Challenge: Learn one new thing outside your major"
            ],
            'corporate': [
                "Wellness Challenge: Take a proper lunch break away from your desk",
                "Productivity Challenge: Complete your most important task first",
                "Connection Challenge: Check in with a colleague you haven't talked to",
                "Balance Challenge: Leave work on time today"
            ]
        }
        
        return random.choice(challenges.get(role, challenges['corporate']))
    
    def get_role_specific_tips(self, role, time_of_day):
        """Get tips based on role and time of day"""
        tips = {
            'student': {
                'morning': "Morning Study: Your brain is fresh - tackle difficult subjects now!",
                'afternoon': "Afternoon Slump: Take a 10-minute walk to re-energize.",
                'evening': "Evening Review: Review what you learned today before bed.",
                'night': "Sleep Time: Aim for 8-9 hours - your brain needs it for memory!"
            },
            'college': {
                'morning': "Morning Routine: Start with breakfast and a quick workout.",
                'afternoon': "Social Time: Perfect time for group study or club meetings.",
                'evening': "Wind Down: Journal about your day and plan tomorrow.",
                'night': "Rest: Avoid all-nighters - they hurt more than help!"
            },
            'corporate': {
                'morning': "Peak Hours: Schedule important meetings and deep work now.",
                'afternoon': "Energy Dip: Take a walk or have a healthy snack.",
                'evening': "Wrap Up: Review accomplishments and plan tomorrow.",
                'night': "Disconnect: Stop checking work emails - you've earned rest!"
            }
        }
        
        hour = datetime.now().hour
        if 5 <= hour < 12:
            period = 'morning'
        elif 12 <= hour < 17:
            period = 'afternoon'
        elif 17 <= hour < 21:
            period = 'evening'
        else:
            period = 'night'
        
        return tips.get(role, tips['corporate']).get(period, "Take care of yourself!")
    
    def get_focus_game(self):
        """Get a random focus improvement game"""
        return random.choice(self.focus_games)
    
    def get_journal_prompt(self):
        """Get a random journaling prompt"""
        return random.choice(self.college_prompts)
    
    def get_peer_topic(self):
        """Get a random peer connection topic"""
        return random.choice(self.peer_topics)
