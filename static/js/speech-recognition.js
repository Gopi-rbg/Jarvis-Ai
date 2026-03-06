// Speech Recognition Module
class SpeechRecognitionModule {
    constructor() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.isListening = false;
        this.wakeWordEncountered = false;
        this.wakeWord = 'jarvis';
        this.callback = null;
        this.errorCallback = null;
        
        this.setupRecognition();
    }

    setupRecognition() {
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';

        this.recognition.onstart = () => {
            this.isListening = true;
            if (this.callback) this.callback('start');
        };

        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript.toLowerCase();

                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            // Check for wake word
            if (!this.wakeWordEncountered && finalTranscript.includes(this.wakeWord)) {
                this.wakeWordEncountered = true;
                if (this.callback) this.callback('wake-word', this.wakeWord);
                return;
            }

            // Process command after wake word
            if (this.wakeWordEncountered && finalTranscript) {
                const command = finalTranscript.replace(this.wakeWord, '').trim();
                if (command && this.callback) {
                    this.callback('command', command);
                }
                this.stop();
            }

            if (this.callback) {
                this.callback('interim', interimTranscript);
            }
        };

        this.recognition.onerror = (event) => {
            const errorMessage = this.getErrorMessage(event.error);
            if (this.errorCallback) this.errorCallback(errorMessage, event.error);
        };

        this.recognition.onend = () => {
            this.isListening = false;
            if (this.callback) this.callback('end');
        };
    }

    start() {
        this.wakeWordEncountered = false;
        try {
            this.recognition.start();
        } catch (e) {
            console.log('Speech recognition already started');
        }
    }

    stop() {
        this.recognition.stop();
    }

    abort() {
        this.recognition.abort();
    }

    setWakeWord(word) {
        this.wakeWord = word.toLowerCase();
    }

    setLanguage(lang) {
        this.recognition.lang = lang;
    }

    getErrorMessage(error) {
        const errors = {
            'no-speech': 'No speech was detected. Please try again.',
            'audio-capture': 'No microphone was found. Ensure that it is connected.',
            'network': 'Network error occurred.',
            'not-allowed': 'Microphone access was denied.',
            'service-not-allowed': 'Speech recognition service not allowed.',
            'bad-grammar': 'Speech recognition error.',
            'aborted': 'Speech recognition was aborted.',
        };
        return errors[error] || 'An error occurred: ' + error;
    }

    onResult(callback) {
        this.callback = callback;
    }

    onError(callback) {
        this.errorCallback = callback;
    }
}

// Export for use in other modules
window.SpeechRecognitionModule = SpeechRecognitionModule;
