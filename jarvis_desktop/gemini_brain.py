# Gemini AI Brain Module
# Integrates with Google Gemini API for intelligent responses

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiBrain:
    """AI Brain powered by Google Gemini API"""
    
    def __init__(self, api_key=None):
        """
        Initialize Gemini API
        
        Args:
            api_key: Google Gemini API key
                    If None, will look for GEMINI_API_KEY in environment
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found!\n"
                "Get one from: https://ai.google.dev/\n"
                "Set GEMINI_API_KEY environment variable"
            )
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat_history = []
        
        print("✓ Gemini AI Brain initialized")
    
    def ask(self, question):
        """
        Ask Gemini a question
        
        Args:
            question: The question to ask
            
        Returns:
            Response from Gemini
        """
        try:
            print(f"🧠 Thinking...")
            response = self.model.generate_content(question)
            answer = response.text
            
            # Store in history
            self.chat_history.append({
                'question': question,
                'answer': answer
            })
            
            return answer
        except Exception as e:
            print(f"✗ Gemini Error: {e}")
            return "I encountered an error processing your request. Please try again."
    
    def ask_with_context(self, question, context=""):
        """
        Ask question with context/history
        
        Args:
            question: The question
            context: Previous conversation context
            
        Returns:
            Response from Gemini
        """
        full_prompt = f"{context}\n\nQuestion: {question}"
        return self.ask(full_prompt)
    
    def get_response(self, user_input):
        """
        Get AI response to user input
        
        Args:
            user_input: User's command or question
            
        Returns:
            AI response
        """
        # Build context from recent history
        context = ""
        if len(self.chat_history) > 0:
            context = "Recent conversation:\n"
            for item in self.chat_history[-3:]:  # Last 3 exchanges
                context += f"Q: {item['question']}\nA: {item['answer']}\n"
        
        return self.ask_with_context(user_input, context)
    
    def clear_history(self):
        """Clear conversation history"""
        self.chat_history = []
        print("✓ Chat history cleared")
    
    def get_history(self):
        """Get conversation history"""
        return self.chat_history


class SimpleBrain:
    """Fallback brain without API (for offline use)"""
    
    def __init__(self):
        """Initialize simple brain with predefined responses"""
        self.responses = {
            'hello': "Hello! I'm Jarvis, your personal AI assistant. How can I help?",
            'hi': "Hi there! Ready to assist you.",
            'how are you': "I'm functioning perfectly, thank you for asking!",
            'what can you do': "I can open applications, control your computer, answer questions, and much more!",
            'who are you': "I'm Jarvis, your personal AI assistant inspired by Iron Man.",
            'joke': "Why did the programmer quit his job? Because he didn't get arrays!",
            'time': "I can't tell time directly, but you can ask your system clock.",
        }
        print("✓ Simple Brain initialized (Offline Mode)")
    
    def ask(self, question):
        """
        Find simple response to question
        
        Args:
            question: The question
            
        Returns:
            Response
        """
        question_lower = question.lower()
        
        for key, response in self.responses.items():
            if key in question_lower:
                return response
        
        return f"I don't have a specific response for '{question}', but I can help with many things!"
    
    def get_response(self, user_input):
        """Get response to user input"""
        return self.ask(user_input)


if __name__ == "__main__":
    # Test Gemini Brain
    try:
        brain = GeminiBrain()
        response = brain.ask("What is Python?")
        print(f"Response: {response}")
    except ValueError as e:
        print(f"Using Simple Brain instead: {e}")
        brain = SimpleBrain()
        response = brain.get_response("What can you do?")
        print(f"Response: {response}")
