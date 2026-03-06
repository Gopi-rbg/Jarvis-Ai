# Jarvis Desktop Package
"""
Jarvis AI Voice Assistant - Desktop Application
Continuous background listening with wake word detection
"""

__version__ = "2.0.0"
__author__ = "Gopi"

from .wake_word import WakeWordDetector
from .speech_to_text import SpeechToText
from .text_to_speech import TextToSpeech
from .commands import SystemCommands
from .gemini_brain import GeminiBrain, SimpleBrain

__all__ = [
    'WakeWordDetector',
    'SpeechToText',
    'TextToSpeech',
    'SystemCommands',
    'GeminiBrain',
    'SimpleBrain',
]
