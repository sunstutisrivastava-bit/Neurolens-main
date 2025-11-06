import random
from datetime import datetime

class MicroEmpathy:
    def __init__(self):
        self.prompts = {
            'angry': {
                'corporate': [
                    "You sound tense. Let's take three deep breaths before replying.",
                    "Try pausing — sometimes silence makes your point better than words.",
                    "You seem frustrated. Want to draft your response before sending it?"
                ],
                'student': [
                    "You look frustrated — maybe take a short walk and revisit the problem.",
                    "Breathe. Learning takes time — you've got this.",
                    "Feeling stuck? Try explaining the problem out loud."
                ],
                'general': [
                    "Take a moment. Your calm response will be more powerful.",
                    "Let's pause and reset. You're in control."
                ]
            },
            'sad': {
                'general': [
                    "It's okay to feel low. Want to hear a calming tune?",
                    "You're doing your best. That's enough right now.",
                    "Feeling down? Remember, this feeling is temporary.",
                    "You've overcome challenges before. You can do it again."
                ]
            },
            'fear': {
                'corporate': [
                    "You seem anxious. Want to draft your thoughts first?",
                    "Feeling nervous? Take 2 minutes to center yourself."
                ],
                'student': [
                    "You look stressed. Let's try a quick focus exercise.",
                    "Anxiety before a test? Remember to breathe deeply."
                ],
                'general': [
                    "You seem stressed. Let's try a relaxation session.",
                    "Take three slow breaths. You've got this."
                ]
            },
            'neutral': {
                'general': [
                    "You look tired. Try 2 minutes of eyes-closed rest?",
                    "You've been focused for long — a water break might help.",
                    "Feeling neutral? Maybe it's time for a quick stretch."
                ]
            },
            'happy': {
                'general': [
                    "Love seeing that energy! Keep it up!",
                    "You're glowing today! Share that positivity.",
                    "Great mood! This is the perfect time to tackle challenges."
                ]
            }
        }
    
    def get_context(self, user_type, hour=None):
        """Determine context based on user type and time"""
        if hour is None:
            hour = datetime.now().hour
        
        if user_type == 'corporate':
            return 'corporate'
        elif user_type in ['student', 'college']:
            return 'student'
        else:
            return 'general'
    
    def get_empathy_prompt(self, emotion, user_type='general'):
        """Get appropriate empathy prompt"""
        context = self.get_context(user_type)
        
        # Get prompts for emotion and context
        emotion_prompts = self.prompts.get(emotion, {})
        
        # Try context-specific first, fallback to general
        if context in emotion_prompts:
            prompt_list = emotion_prompts[context]
        elif 'general' in emotion_prompts:
            prompt_list = emotion_prompts['general']
        else:
            return {
                'prompt': "Take a moment for yourself. You're doing great.",
                'action': None
            }
        
        prompt = random.choice(prompt_list)
        
        # Determine suggested action
        action = None
        if 'breath' in prompt.lower():
            action = 'breathing'
        elif 'walk' in prompt.lower() or 'stretch' in prompt.lower():
            action = 'break'
        elif 'calm' in prompt.lower() or 'relax' in prompt.lower():
            action = 'relaxation'
        
        return {
            'prompt': prompt,
            'action': action,
            'emotion': emotion
        }
