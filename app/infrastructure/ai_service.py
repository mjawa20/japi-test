from openai import OpenAI
from app.config.config import settings
from typing import List, Dict, Any, Optional
from enum import Enum

class OnboardingStep(str, Enum):
    WELCOME = "welcome"
    ASK_GOAL = "ask_goal"
    ASK_LEVEL = "ask_level"
    COMPLETE = "complete"

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"
        self.system_prompt = """
        You are Japi, an AI English tutor. Your role is to help users improve their English skills through conversation.
        - Be friendly, patient, and encouraging
        - Correct mistakes in a constructive way
        - Adapt your language to the user's level (Beginner/Intermediate/Advanced)
        - Focus on practical, conversational English
        - Keep responses concise and natural
        - If the user makes a mistake, first repeat their sentence correctly, then explain the correction
        - Ask follow-up questions to keep the conversation going
        - For beginners: Use simple vocabulary and short sentences
        - For intermediate: Use a wider range of vocabulary and more complex structures
        - For advanced: Use natural, idiomatic English with more complex structures
        """

    def _get_system_message(self, user_level: Optional[str] = None) -> Dict[str, str]:
        """Get the system message with level-specific instructions"""
        level_instruction = ""
        if user_level:
            level_instruction = f"\nThe user has indicated they are at the {user_level} level. "
            if user_level.lower() == 'beginner':
                level_instruction += "Use simple vocabulary and short sentences. Focus on basic grammar and common phrases."
            elif user_level.lower() == 'intermediate':
                level_instruction += "Use a wider range of vocabulary and slightly more complex sentences. Gently correct mistakes and explain when needed."
            else:  # advanced
                level_instruction += "Use natural, idiomatic English. Focus on fluency, nuance, and more complex language structures."
        
        return {
            "role": "system",
            "content": self.system_prompt + level_instruction
        }

    def _is_valid_goal_response(self, message: str) -> bool:
        """Check if the user's response is a valid learning goal."""
        message = message.lower().strip()
        if len(message) < 5:
            return False
        
        # Common invalid responses
        invalid_responses = [
            'i don\'t know', 'dunno', 'not sure', 'idk', 'nothing',
            'i don\'t have one', 'no idea', 'not sure yet', 'i don\'t care'
        ]
        
        return not any(inv in message for inv in invalid_responses)

    def _is_valid_level_response(self, message: str) -> bool:
        """Check if the user's response contains a valid English level."""
        message = message.lower()
        return any(level in message for level in ["beginner", "intermediate", "advanced"])

    def _detect_onboarding_step(self, conversation_history: List[Dict[str, str]]) -> OnboardingStep:
        """Detect the current step of the onboarding process."""
        if not conversation_history:
            return OnboardingStep.WELCOME
            
        # Get all messages in order
        ai_messages = [msg for msg in conversation_history if msg["role"] == "ai"]
        user_messages = [msg for msg in conversation_history if msg["role"] == "user"]
        
        # If no AI messages yet, we're at welcome
        if not ai_messages:
            return OnboardingStep.WELCOME
            
        last_ai = ai_messages[-1]["content"].lower()
        
        # Check if we're asking for a goal
        if any(phrase in last_ai for phrase in ["what's your english learning goal", "what you'd like to achieve"]):
            if user_messages and len(user_messages) > 0:
                last_user = user_messages[-1]["content"]
                if not self._is_valid_goal_response(last_user):
                    return OnboardingStep.ASK_GOAL
            return OnboardingStep.ASK_GOAL
            
        # Check if we're asking for level
        if any(phrase in last_ai for phrase in ["what is your current english level", "tell me your current english level", "beginner/intermediate/advanced"]):
            if user_messages and len(user_messages) > 0:
                last_user = user_messages[-1]["content"]
                if not self._is_valid_level_response(last_user):
                    return OnboardingStep.ASK_LEVEL
            return OnboardingStep.ASK_LEVEL
            
        # Default to welcome if we can't determine the step
        return OnboardingStep.WELCOME

    def generate_onboarding_response(
        self, 
        user_name: str, 
        conversation_history: List[Dict[str, str]],
        user_goal: Optional[str] = None,
        user_level: Optional[str] = None
    ) -> str:
        """Generate an AI response for the onboarding conversation."""
        onboarding_step = self._detect_onboarding_step(conversation_history)
        
        if onboarding_step == OnboardingStep.WELCOME:
            return f"Hi {user_name}! Welcome to Japi. What's your English learning goal?"
            
        elif onboarding_step == OnboardingStep.ASK_GOAL:
            last_message = conversation_history[-1]["content"].lower()
            if any(phrase in last_message for phrase in ["i want", "i'd like", "i need", "my goal", "i wish", "improve", "learn", "help with"]):
                return f"That's a great goal, {user_name}! What is your current English level? (Beginner/Intermediate/Advanced)"
            else:
                return f"Hi {user_name}! To help you better, could you tell me what you'd like to achieve with your English? For example: 'I want to improve my speaking skills'"
        
        elif onboarding_step == OnboardingStep.ASK_LEVEL:
            last_message = conversation_history[-1]["content"].lower()
            if any(level in last_message for level in ["beginner", "intermediate", "advanced"]):
                detected_level = next((level for level in ["beginner", "intermediate", "advanced"] if level in last_message), "intermediate")
                return f"Got it! Let's begin with a practice conversation."
            else:
                return "I'm not sure I understand. Could you please tell me your current English level? (Beginner/Intermediate/Advanced)"
        
        # If we reach here, onboarding is complete
        return "Let's start our English practice! What would you like to talk about?"

    def generate_chat_response(
        self, 
        conversation_history: List[Dict[str, str]],
        user_name: str,
        user_level: Optional[str] = None
    ) -> str:
        """Generate a response for regular chat after onboarding is complete."""
        try:
            # Prepare messages with system prompt
            messages = [self._get_system_message(user_level)]
            
            # Add conversation history
            for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                role = "assistant" if msg["role"] == "ai" else "user"
                messages.append({"role": role, "content": msg["content"]})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "I'm sorry, I'm having trouble generating a response. Could you please rephrase that or try again later?"

# Create and export the AI service instance
ai = AIService()

# Export OnboardingStep for use in other modules
__all__ = ['ai', 'OnboardingStep', 'AIService']
