# Speech to Text Module
# Handles conversion of audio to text using SpeechRecognition or Vosk

import speech_recognition as sr
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import os

class SpeechToText:
    """Converts speech audio to text"""
    
    def __init__(self, use_vosk=True):
        """
        Initialize speech-to-text engine
        
        Args:
            use_vosk: Use Vosk for offline recognition (default: True)
                     If False, uses Google Speech Recognition (requires internet)
        """
        self.use_vosk = use_vosk
        self.recognizer = None
        self.microphone = None
        
        if not use_vosk:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            print("✓ SpeechRecognition initialized (Google Cloud)")
        else:
            print("✓ Vosk Speech-to-Text initialized (Offline)")
    
    def recognize_speech_google(self, timeout=10):
        """
        Recognize speech using Google Cloud Speech Recognition
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Recognized text or None
        """
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            print("⏳ Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"✓ Recognized: {text}")
            return text
        
        except sr.UnknownValueError:
            print("✗ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"✗ Google Speech Recognition error: {e}")
            return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def recognize_speech_vosk(self, timeout=10):
        """
        Recognize speech using Vosk (offline)
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Recognized text or None
        """
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'models', 'vosk-model-en-us-0.22')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found at {model_path}")
            
            model = Model(model_path)
            recognizer = KaldiRecognizer(model, 16000)
            
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4096
            )
            stream.start_stream()
            
            print("🎤 Listening...")
            import time
            start_time = time.time()
            
            while True:
                data = stream.read(4096, exception_on_overflow=False)
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = ' '.join([t.get('conf', '') for t in result.get('result', [])])
                    
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    
                    if text.strip():
                        print(f"✓ Recognized: {text}")
                        return text
                
                # Check timeout
                if time.time() - start_time > timeout:
                    print("⏱ Recognition timeout")
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    return None
        except Exception as e:
            print(f"✗ Vosk error: {e}")
            return None
    
    def recognize(self, timeout=10):
        """
        Recognize speech using configured engine
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Recognized text or None
        """
        if self.use_vosk:
            return self.recognize_speech_vosk(timeout)
        else:
            return self.recognize_speech_google(timeout)


if __name__ == "__main__":
    # Test speech recognition
    stt = SpeechToText(use_vosk=True)
    text = stt.recognize()
    print(f"Final result: {text}")
