# Text to Speech Module
# Uses pyttsx3 for offline voice synthesis

import pyttsx3
import threading

class TextToSpeech:
    """Converts text to speech with voice output"""
    
    def __init__(self, rate=150, volume=0.9):
        """
        Initialize text-to-speech engine
        
        Args:
            rate: Speech rate (150-200 recommended)
            volume: Volume level (0.0-1.0)
        """
        self.engine = pyttsx3.init()
        self.rate = rate
        self.volume = volume
        self.is_speaking = False
        
        # Configure engine
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        
        # Try to set a better voice
        voices = self.engine.getProperty('voices')
        if voices:
            # Prefer female voice if available
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        
        print("✓ Text-to-Speech initialized")
    
    def speak(self, text, wait=True):
        """
        Speak text using offline synthesis
        
        Args:
            text: Text to speak
            wait: Wait for speech to complete (default: True)
        """
        if not text or not text.strip():
            return
        
        try:
            self.is_speaking = True
            print(f"🔊 Speaking: {text}")
            
            self.engine.say(text)
            
            if wait:
                self.engine.runAndWait()
            else:
                # Run in separate thread
                thread = threading.Thread(target=self.engine.runAndWait)
                thread.daemon = True
                thread.start()
            
            self.is_speaking = False
        except Exception as e:
            print(f"✗ TTS Error: {e}")
            self.is_speaking = False
    
    def speak_async(self, text):
        """
        Speak text asynchronously (non-blocking)
        
        Args:
            text: Text to speak
        """
        thread = threading.Thread(target=self.speak, args=(text, True))
        thread.daemon = True
        thread.start()
    
    def set_rate(self, rate):
        """Set speech rate (50-300)"""
        self.rate = rate
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        """Set volume (0.0-1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        self.engine.setProperty('volume', self.volume)
    
    def set_voice(self, gender='female'):
        """
        Set voice gender
        
        Args:
            gender: 'female' or 'male'
        """
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if gender.lower() in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                print(f"✓ Voice set to: {voice.name}")
                return
        print(f"✗ Voice '{gender}' not found")
    
    def stop(self):
        """Stop current speech"""
        try:
            self.engine.stop()
            self.is_speaking = False
            print("⏹ Speech stopped")
        except Exception as e:
            print(f"✗ Error stopping speech: {e}")
    
    def list_voices(self):
        """List available voices"""
        voices = self.engine.getProperty('voices')
        print("\n📢 Available Voices:")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name}")
        return voices


if __name__ == "__main__":
    # Test TTS
    tts = TextToSpeech()
    tts.list_voices()
    tts.speak("Hello! I am Jarvis, your personal AI assistant.")
    tts.speak("How can I help you today?")
