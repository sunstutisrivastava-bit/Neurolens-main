import random

class NeuroLensChatbot:
    def __init__(self):
        self.conversation_state = 'greeting'
        self.user_responses = {}
        self.question_index = 0
        self.asked_questions = set()
        
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
            "How do you handle difficult emotions?"
        ]
        
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
    
    def get_response(self, user_input):
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