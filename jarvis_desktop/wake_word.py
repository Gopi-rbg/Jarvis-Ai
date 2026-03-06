# Wake Word Detection Module
# Uses Vosk for offline, efficient wake word and speech recognition

import pyaudio
import json
import os
from vosk import Model, KaldiRecognizer

class WakeWordDetector:
    """Detects wake word 'Jarvis' using Vosk offline speech recognition"""
    
    def __init__(self, wake_word="jarvis"):
        """
        Initialize Vosk model for wake word detection
        
        Args:
            wake_word: The wake word to listen for (default: "jarvis")
        """
        self.wake_word = wake_word.lower()
        self.model = None
        self.recognizer = None
        self.stream = None
        self.is_listening = False
        
        try:
            # Download model from: https://alphacephei.com/vosk/models
            # Place it in the jarvis_desktop/models directory
            model_path = os.path.join(os.path.dirname(__file__), 'models', 'vosk-model-en-us-0.22')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"Vosk model not found at {model_path}\n"
                    "Download from: https://alphacephei.com/vosk/models\n"
                    f"Extract to: {os.path.dirname(__file__)}/models/"
                )
            
            self.model = Model(model_path)
            self.audio = pyaudio.PyAudio()
            print("✓ Wake word detector initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing wake word detector: {e}")
            raise
    
    def start_listening(self):
        """Start listening for wake word"""
        try:
            self.recognizer = KaldiRecognizer(self.model, 16000)
            self.stream = self.audio.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4096
            )
            self.stream.start_stream()
            self.is_listening = True
            print(f"🎤 Listening for wake word '{self.wake_word}'...")
        except Exception as e:
            print(f"✗ Error starting listening: {e}")
            raise
    
    def detect_wake_word(self, timeout=None):
        """
        Listen for wake word
        
        Args:
            timeout: Timeout in seconds (None = infinite)
            
        Returns:
            True if wake word detected, False otherwise
        """
        if not self.is_listening:
            self.start_listening()
        
        try:
            while True:
                data = self.stream.read(4096, exception_on_overflow=False)
                
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('result', [])
                    
                    if text:
                        text_str = ' '.join(t['conf'] for t in text if 'conf' in t)
                        print(f"Speech detected: {text}")
                    
                    # Check for wake word in result
                    full_text = result.get('result', [])
                    if full_text:
                        speech_text = ' '.join([t.get('conf', '') for t in full_text])
                        if self.wake_word in speech_text.lower():
                            print(f"✓ Wake word '{self.wake_word}' detected!")
                            return True
                else:
                    # Partial result
                    partial = json.loads(self.recognizer.PartialResult())
                    partial_text = partial.get('partial', '')
                    if self.wake_word in partial_text.lower():
                        print(f"✓ Wake word '{self.wake_word}' detected!")
                        return True
        except KeyboardInterrupt:
            print("\n⏸ Listening stopped")
            return False
        except Exception as e:
            print(f"✗ Error detecting wake word: {e}")
            return False
    
    def stop_listening(self):
        """Stop listening for wake word"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.is_listening = False
        print("⏹ Stopped listening")
    
    def get_speech_input(self, timeout=30):
        """
        Get speech input from user after wake word detected
        
        Returns:
            Recognized speech text, or None if no speech detected
        """
        if not self.is_listening:
            self.start_listening()
        
        print(f"🎙 Listening for command (timeout: {timeout}s)...")
        
        try:
            import time
            start_time = time.time()
            
            while True:
                data = self.stream.read(4096, exception_on_overflow=False)
                
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    recognized_text = result.get('result', [])
                    
                    if recognized_text:
                        # Extract the text from recognition results
                        text = ' '.join([t.get('conf', '') for t in recognized_text])
                        if text.strip():
                            print(f"✓ Command recognized: {text}")
                            return text
                
                # Check timeout
                if time.time() - start_time > timeout:
                    print("⏱ Speech recognition timeout")
                    return None
        except Exception as e:
            print(f"✗ Error getting speech input: {e}")
            return None
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_listening()
        if self.audio:
            self.audio.terminate()
        print("✓ Wake word detector cleaned up")


if __name__ == "__main__":
    # Test wake word detection
    detector = WakeWordDetector()
    try:
        detector.start_listening()
        if detector.detect_wake_word():
            command = detector.get_speech_input()
            print(f"Got command: {command}")
    finally:
        detector.cleanup()
