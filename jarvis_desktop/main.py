#!/usr/bin/env python3
# Main Jarvis Application
# Continuous background listening loop with wake word detection

import sys
import os
from datetime import datetime

# Add jarvis_desktop to path
sys.path.insert(0, os.path.dirname(__file__))

from wake_word import WakeWordDetector
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from commands import SystemCommands
from gemini_brain import GeminiBrain, SimpleBrain

class Jarvis:
    """Main Jarvis AI Assistant Application"""
    
    def __init__(self):
        """Initialize Jarvis"""
        print("\n" + "="*60)
        print("  🤖 JARVIS AI VOICE ASSISTANT")
        print("="*60)
        print("Initializing modules...\n")
        
        try:
            # Initialize modules
            self.wake_word_detector = WakeWordDetector(wake_word="jarvis")
            self.speech_to_text = SpeechToText(use_vosk=True)  # Offline recognition
            self.text_to_speech = TextToSpeech(rate=150, volume=0.9)
            self.system_commands = SystemCommands()
            
            # Try Gemini, fallback to Simple Brain
            try:
                self.brain = GeminiBrain()
            except ValueError:
                print("⚠ Gemini API not configured, using Simple Brain for Q&A\n")
                self.brain = SimpleBrain()
            
            self.is_running = False
            self.command_history = []
            
            print("\n✓ All modules initialized successfully!")
            print("📢 Say 'Jarvis' to activate, then give your command.\n")
            
        except Exception as e:
            print(f"✗ Initialization failed: {e}")
            sys.exit(1)
    
    def parse_command(self, user_input):
        """
        Parse user input and determine action type
        
        Args:
            user_input: Raw user input/command
            
        Returns:
            (action_type, target, parameters)
        """
        user_input = user_input.lower().strip()
        
        # Remove 'jarvis' prefix if present
        if user_input.startswith('jarvis'):
            user_input = user_input[6:].strip()
        
        # Application opening commands
        applications = ['chrome', 'firefox', 'vscode', 'code', 'spotify', 'discord', 
                       'telegram', 'calculator', 'notepad', 'vlc', 'obs', 'blender']
        
        for app in applications:
            if f'open {app}' in user_input or f'launch {app}' in user_input:
                return ('open_app', app, None)
        
        # Website opening
        if 'open' in user_input or 'go to' in user_input:
            words = user_input.split()
            if 'open' in words:
                idx = words.index('open')
                if idx + 1 < len(words):
                    website = ' '.join(words[idx+1:])
                    return ('open_website', website, None)
        
        # YouTube search
        if 'youtube' in user_input or 'play' in user_input:
            if 'search' in user_input:
                query = user_input.replace('search', '').replace('youtube', '').strip()
                return ('youtube_search', query, None)
            return ('youtube', '', None)
        
        # Google search
        if 'search' in user_input or 'google' in user_input:
            query = user_input.replace('search', '').replace('google', '')
            query = query.replace('for', '').strip()
            return ('google_search', query, None)
        
        # System control
        if 'shutdown' in user_input:
            return ('shutdown', '', 60)
        if 'restart' in user_input:
            return ('restart', '', 60)
        
        # Default to Q&A
        return ('ask_ai', user_input, None)
    
    def execute_command(self, action_type, target, params):
        """
        Execute command based on action type
        
        Args:
            action_type: Type of action to execute
            target: Target (app name, website, query, etc)
            params: Additional parameters
            
        Returns:
            Response message
        """
        try:
            if action_type == 'open_app':
                response = self.system_commands.open_application(target)
            
            elif action_type == 'open_website':
                response = self.system_commands.open_website(target)
            
            elif action_type == 'youtube_search':
                response = self.system_commands.open_youtube(target)
            
            elif action_type == 'youtube':
                response = self.system_commands.open_youtube()
            
            elif action_type == 'google_search':
                response = self.system_commands.search_google(target)
            
            elif action_type == 'shutdown':
                response = "Initiating shutdown. You can cancel by pressing Ctrl+C"
                self.text_to_speech.speak(response)
                self.system_commands.shutdown_computer(params)
                return
            
            elif action_type == 'restart':
                response = "Initiating restart"
                self.text_to_speech.speak(response)
                self.system_commands.restart_computer(params)
                return
            
            elif action_type == 'ask_ai':
                print(f"\n🧠 Asking AI: {target}")
                response = self.brain.get_response(target)
            
            else:
                response = "I didn't understand that command"
            
            # Log command
            self.command_history.append({
                'timestamp': datetime.now().isoformat(),
                'command': target,
                'action': action_type,
                'response': response
            })
            
            return response
        
        except Exception as e:
            error_msg = f"Error executing command: {e}"
            print(f"✗ {error_msg}")
            return error_msg
    
    def run(self):
        """Main application loop"""
        self.is_running = True
        
        print("\n🎤 Starting continuous listening...\n")
        
        try:
            while self.is_running:
                try:
                    # Listen for wake word
                    print("⏳ Waiting for wake word 'Jarvis'...")
                    
                    if self.wake_word_detector.detect_wake_word():
                        # Beep to indicate activation
                        self.text_to_speech.speak("Yes?")
                        
                        # Get user command
                        command = self.speech_to_text.recognize(timeout=10)
                        
                        if command:
                            print(f"\n👤 User: {command}")
                            
                            # Parse command
                            action_type, target, params = self.parse_command(command)
                            print(f"📋 Action: {action_type} | Target: {target}")
                            
                            # Execute command
                            response = self.execute_command(action_type, target, params)
                            
                            if response:
                                print(f"\n🤖 Jarvis: {response}\n")
                                self.text_to_speech.speak(response)
                        else:
                            self.text_to_speech.speak("I didn't catch that. Please try again.")
                
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"✗ Error in main loop: {e}")
                    continue
        
        except KeyboardInterrupt:
            print("\n\n⏹ Shutting down Jarvis...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up resources...")
        self.wake_word_detector.cleanup()
        
        # Save command history
        self.save_command_history()
        
        print("✓ Jarvis shutdown complete")
        self.is_running = False
    
    def save_command_history(self):
        """Save command history to file"""
        try:
            import json
            history_file = os.path.join(os.path.dirname(__file__), 'command_history.json')
            
            with open(history_file, 'w') as f:
                json.dump(self.command_history, f, indent=2)
            
            print(f"✓ Command history saved ({len(self.command_history)} commands)")
        except Exception as e:
            print(f"✗ Error saving command history: {e}")
    
    def get_status(self):
        """Get Jarvis status"""
        return {
            'running': self.is_running,
            'commands_executed': len(self.command_history),
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Entry point"""
    print("""
╔════════════════════════════════════════════════════════════╗
║       JARVIS - AI VOICE ASSISTANT                         ║
║  Speaks "Jarvis" to activate, then give your command      ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    jarvis = Jarvis()
    jarvis.run()


if __name__ == "__main__":
    main()
