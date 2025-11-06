import random

class NeuroLensChatbot:
    def __init__(self):
        self.conversation_state = 'greeting'
        self.user_responses = {}
        self.question_index = 0
        self.asked_questions = set()
        self.detected_emotion = None
        
        self.question_pool = [
            "How was your day today?",
            "What's your favorite hobby or activity?",
            "What's your favorite color and why?",
            "How have you been sleeping lately?",
            "What makes you feel most relaxed?",
            "How often do you spend time with friends or family?",
            "What's something that made you smile recently?",
            "How do you usually handle stress?",
            "What's your energy level like most days?",
            "What are you looking forward to?",
            "Tell me about your best friend.",
            "What's your favorite season and why?",
            "How do you feel when you wake up in the morning?",
            "What kind of music do you enjoy?",
            "Describe your ideal weekend.",
            "What's been challenging for you lately?",
            "How do you celebrate small victories?",
            "What helps you feel better when you're down?",
            "Tell me about a place that makes you happy.",
            "What's your favorite way to spend time alone?",
            "How do you connect with others?",
            "What gives you a sense of purpose?",
            "How has your appetite been recently?",
            "What's something you're proud of?",
            "How do you handle difficult emotions?",
            "What's your favorite food and why?",
            "Do you have any pets? Tell me about them.",
            "What's your favorite book or movie?",
            "How do you spend your free time?",
            "What makes you feel confident?",
            "Tell me about a happy memory.",
            "What's your favorite subject in school?",
            "How do you feel about trying new things?",
            "What's your biggest dream or goal?",
            "How do you deal with disappointment?",
            "What's your favorite game to play?",
            "Tell me about someone you admire.",
            "What makes you laugh the most?",
            "How do you like to exercise or stay active?",
            "What's your favorite time of day?",
            "How do you feel about changes in your life?",
            "What's something new you learned recently?",
            "How do you show kindness to others?",
            "What's your favorite thing about yourself?",
            "How do you feel when you're with your family?",
            "What's a skill you'd like to learn?",
            "How do you calm yourself when upset?",
            "What's your favorite outdoor activity?",
            "Tell me about your daily routine.",
            "What makes you feel safe and secure?",
            "How do you express your feelings?",
            "What's your favorite way to help others?",
            "How do you feel about school or work?",
            "What's something that excites you?",
            "How do you handle conflicts with friends?",
            "What's your favorite holiday and why?",
            "How do you feel about your future?",
            "What's something that worries you?",
            "How do you like to be comforted?",
            "What's your favorite thing to do on a rainy day?",
            "How do you feel when you accomplish something?",
            "What's your favorite way to relax before bed?",
            "How do you stay motivated?",
            "What's something you're grateful for?",
            "How do you feel about making new friends?",
            "What's your favorite childhood memory?",
            "How do you handle feeling lonely?",
            "What's your favorite thing about nature?",
            "How do you feel when someone compliments you?",
            "What's your favorite way to be creative?",
            "How do you deal with feeling overwhelmed?",
            "What's your favorite thing to talk about?",
            "How do you feel about asking for help?",
            "What's something that inspires you?",
            "How do you celebrate your achievements?",
            "What's your favorite way to spend time with friends?",
            "How do you feel about your hobbies?",
            "What's something that makes you unique?",
            "How do you handle feeling sad?",
            "What's your favorite way to learn new things?"
        ]
        
        self.emotion_responses = {
            'sad': {
                'empathy': [
                    "I can sense you're feeling down. It's okay to feel sad sometimes. Would you like to talk about what's bothering you?",
                    "I'm here for you. Sadness is a natural emotion, and it's important to acknowledge it.",
                    "I notice you might be feeling low. Remember, this feeling is temporary and you're not alone."
                ],
                'coping': [
                    "Try taking deep breaths - inhale for 4 counts, hold for 4, exhale for 4. This can help calm your mind.",
                    "Consider reaching out to a friend or loved one. Connection can really help when we're feeling down.",
                    "Sometimes a short walk or listening to uplifting music can shift our mood. Would you like to try that?",
                    "Writing down your feelings in a journal can help process emotions. Have you tried that?"
                ]
            },
            'angry': {
                'empathy': [
                    "I can tell you're feeling frustrated or angry. It's completely valid to feel this way.",
                    "Anger is a natural response. Let's work through this together.",
                    "I understand you're upset. Take a moment to breathe - I'm here to listen."
                ],
                'coping': [
                    "Try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
                    "Physical activity like a quick walk or some stretches can help release tension.",
                    "Count to 10 slowly before responding to what's bothering you. This gives your mind time to calm.",
                    "Try progressive muscle relaxation - tense and release each muscle group from toes to head."
                ]
            },
            'anxious': {
                'empathy': [
                    "I sense you might be feeling anxious or worried. These feelings can be overwhelming.",
                    "Anxiety can be tough. Remember, you've gotten through difficult moments before.",
                    "I'm here with you. Let's take this one step at a time."
                ],
                'coping': [
                    "Try box breathing: Breathe in for 4, hold for 4, out for 4, hold for 4. Repeat 4 times.",
                    "Focus on what you can control right now. Make a list of small, manageable tasks.",
                    "Ground yourself in the present moment. What are 3 things you can see right now?",
                    "Remember: feelings aren't facts. Challenge anxious thoughts by asking 'Is this really true?'"
                ]
            },
            'happy': {
                'empathy': [
                    "I love seeing you happy! Your positive energy is wonderful.",
                    "That's fantastic! It's great to see you in such good spirits.",
                    "Your happiness is contagious! Keep embracing these positive moments."
                ],
                'coping': [
                    "Savor this moment! Take a mental snapshot to remember this feeling.",
                    "Share your joy with someone you care about - happiness multiplies when shared!",
                    "Consider writing down what made you happy today in a gratitude journal."
                ]
            },
            'neutral': {
                'empathy': [
                    "You seem calm and balanced right now. That's a good place to be.",
                    "I appreciate you taking time to check in with yourself."
                ],
                'coping': [
                    "This is a great time for reflection. What's one thing you're grateful for today?",
                    "Use this calm moment to set a positive intention for the rest of your day."
                ]
            },
            'fear': {
                'empathy': [
                    "I can sense you're feeling scared or worried. It's brave of you to acknowledge this.",
                    "Fear is your mind trying to protect you. Let's work through this together.",
                    "You're safe right now. I'm here with you."
                ],
                'coping': [
                    "Focus on your breath. Slow, deep breathing signals safety to your nervous system.",
                    "Name your fear out loud or write it down. Sometimes naming it reduces its power.",
                    "Ask yourself: What's the worst that could happen? What's the best? What's most likely?",
                    "Reach out to someone you trust. You don't have to face this alone."
                ]
            }
        }
        
        self.responses = {
            'greeting': [
                "Hello! I'm your NeuroLens wellness assistant. I can help analyze your emotional well-being. Would you like to start a quick wellness check?",
                "Hi there! I'm here to help understand your emotional state through some friendly questions. Ready to begin?",
                "Welcome! I can help assess your mood and well-being. Shall we start with a few questions?"
            ],
            'emotions': [
                "NeuroLens can detect emotions like happy, sad, angry, surprised, fear, and disgust from both facial expressions and voice patterns.",
                "Our system analyzes facial expressions and voice tone to identify emotional states in real-time."
            ],
            'positive_response': [
                "That sounds wonderful! It's great to hear positive things.",
                "That's really nice to hear! Positive experiences are so important.",
                "I'm glad to hear that! It sounds like you're doing well."
            ],
            'concerning_response': [
                "I understand that can be challenging. Remember, it's okay to have difficult days.",
                "Thank you for sharing that with me. It's important to acknowledge how we're feeling.",
                "I hear you. Sometimes things can feel overwhelming, and that's completely normal."
            ],
            'neutral_response': [
                "Thank you for sharing that with me.",
                "I appreciate you being open about that.",
                "That's helpful to know."
            ]
        }
    
    def analyze_response(self, response):
        response_lower = response.lower()
        positive_words = ['good', 'great', 'happy', 'wonderful', 'amazing', 'love', 'enjoy', 'excited', 'fantastic', 'excellent', 'bright', 'colorful', 'well', 'fine', 'relaxed', 'often', 'daily', 'smile', 'laugh', 'exercise', 'music', 'high', 'energetic', 'looking forward']
        negative_words = ['bad', 'terrible', 'sad', 'depressed', 'awful', 'hate', 'tired', 'exhausted', 'dark', 'black', 'poorly', 'badly', 'stressed', 'anxious', 'rarely', 'never', 'alone', 'lonely', 'cry', 'nothing', 'low', 'drained', 'worried', 'scared']
        
        positive_count = sum(1 for word in positive_words if word in response_lower)
        negative_count = sum(1 for word in negative_words if word in response_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'concerning'
        else:
            return 'neutral'
    
    def set_detected_emotion(self, emotion):
        """Set the detected emotion from facial/voice analysis"""
        self.detected_emotion = emotion.lower() if emotion else None
    
    def get_emotion_aware_response(self):
        """Generate emotion-aware response based on detected emotion"""
        if not self.detected_emotion:
            return None
        
        emotion = self.detected_emotion
        if emotion in ['sad', 'sadness']:
            emotion = 'sad'
        elif emotion in ['angry', 'anger']:
            emotion = 'angry'
        elif emotion in ['fear', 'scared']:
            emotion = 'fear'
        elif emotion in ['happy', 'joy', 'joyful']:
            emotion = 'happy'
        elif emotion in ['anxious', 'worried', 'stress']:
            emotion = 'anxious'
        else:
            emotion = 'neutral'
        
        if emotion in self.emotion_responses:
            empathy = random.choice(self.emotion_responses[emotion]['empathy'])
            coping = random.choice(self.emotion_responses[emotion]['coping'])
            return f"{empathy} {coping}"
        return None
    
    def get_response(self, user_input, detected_emotion=None):
        # Update detected emotion if provided
        if detected_emotion:
            self.set_detected_emotion(detected_emotion)
        
        # Check if we should provide emotion-aware response
        if self.detected_emotion and random.random() < 0.3:  # 30% chance to give emotion-aware response
            emotion_response = self.get_emotion_aware_response()
            if emotion_response:
                return emotion_response
        
        user_input_lower = user_input.lower()
        
        # Handle system questions
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'start']):
            if self.conversation_state != 'greeting':
                self.conversation_state = 'greeting'
                return random.choice(self.responses['greeting'])
            else:
                return "I'm ready to help! Would you like to start a wellness check?"
        elif any(word in user_input_lower for word in ['emotion', 'detect', 'how it works']):
            return random.choice(self.responses['emotions'])
        elif any(word in user_input_lower for word in ['yes', 'sure', 'okay', 'start']) and self.conversation_state == 'greeting':
            self.conversation_state = 'questioning'
            self.question_index = 0
            return f"Great! Let's start. {self.get_next_question()}"
        elif any(word in user_input_lower for word in ['no', 'not now', 'maybe later']) and self.conversation_state == 'greeting':
            return "No problem! I'm here whenever you're ready. You can ask me about NeuroLens or emotion detection anytime."
        
        # Handle wellness questions
        if self.conversation_state == 'questioning':
            # Store the response
            self.user_responses[self.question_index] = user_input
            
            # Analyze the response
            sentiment = self.analyze_response(user_input)
            
            # Provide appropriate feedback
            if sentiment == 'positive':
                feedback = random.choice(self.responses['positive_response'])
            elif sentiment == 'concerning':
                feedback = random.choice(self.responses['concerning_response'])
            else:
                feedback = random.choice(self.responses['neutral_response'])
            
            # Move to next question or provide summary
            self.question_index += 1
            
            if self.question_index < 10 and len(self.asked_questions) < len(self.question_pool):
                return f"{feedback} {self.get_next_question()}"
            else:
                # End of questions - provide summary
                self.conversation_state = 'complete'
                return self.generate_summary()
        
        # Default responses
        if self.conversation_state == 'greeting':
            return "Would you like to start a wellness check or learn about NeuroLens?"
        return "I'm here to help with wellness questions or information about NeuroLens. Would you like to start a wellness check or ask about our emotion detection system?"
    
    def generate_summary(self):
        positive_responses = 0
        concerning_responses = 0
        
        for response in self.user_responses.values():
            sentiment = self.analyze_response(response)
            if sentiment == 'positive':
                positive_responses += 1
            elif sentiment == 'concerning':
                concerning_responses += 1
        
        if positive_responses > concerning_responses:
            return "Thank you for sharing! Based on our conversation, you seem to be doing well overall. Keep up the positive mindset! Remember, NeuroLens is here to help monitor your emotional well-being."
        elif concerning_responses > positive_responses:
            return "Thank you for being open with me. It sounds like you might be going through some challenges. Remember, it's important to talk to someone you trust or a professional if you're feeling overwhelmed. NeuroLens can help track your emotional patterns over time."
        else:
            return "Thank you for the conversation! Everyone has ups and downs, and that's completely normal. NeuroLens can help you better understand your emotional patterns. Take care of yourself!"
    
    def get_next_question(self):
        available_questions = [q for q in self.question_pool if q not in self.asked_questions]
        if available_questions:
            question = random.choice(available_questions)
            self.asked_questions.add(question)
            return question
        return "Thank you for sharing so much with me!"