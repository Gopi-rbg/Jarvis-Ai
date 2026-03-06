// Text-to-Speech Module
class TextToSpeechModule {
    constructor() {
        window.synth = window.synth || window.speechSynthesis;
        this.voices = [];
        this.volume = 0.7;
        this.pitch = 1.0;
        this.rate = 0.9;
        this.selectedVoice = null;
        
        this.loadVoices();
        window.speechSynthesis.onvoiceschanged = () => this.loadVoices();
    }

    loadVoices() {
        this.voices = window.speechSynthesis.getVoices();
        if (this.voices.length > 0 && !this.selectedVoice) {
            // Try to find a female voice first
            this.selectedVoice = this.voices.find(voice => voice.name.includes('Female')) || this.voices[0];
        }
    }

    speak(text, onComplete) {
        return new Promise((resolve, reject) => {
            if (!text || text.trim() === '') {
                reject(new Error('No text to speak'));
                return;
            }

            // Cancel any ongoing speech
            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.volume = this.volume;
            utterance.pitch = this.pitch;
            utterance.rate = this.rate;
            
            if (this.selectedVoice) {
                utterance.voice = this.selectedVoice;
            }

            utterance.onstart = () => {
                if (onComplete) onComplete('start');
            };

            utterance.onend = () => {
                if (onComplete) onComplete('end');
                resolve();
            };

            utterance.onerror = (event) => {
                console.error('Speech synthesis error:', event);
                if (onComplete) onComplete('error', event.error);
                reject(new Error(event.error));
            };

            window.speechSynthesis.speak(utterance);
        });
    }

    setVoice(voiceIndex) {
        if (voiceIndex < this.voices.length) {
            this.selectedVoice = this.voices[voiceIndex];
        }
    }

    setVoiceByType(type) {
        const voiceType = type.toLowerCase();
        if (voiceType === 'female') {
            this.selectedVoice = this.voices.find(v => v.name.includes('Female')) || this.voices[0];
        } else if (voiceType === 'male') {
            this.selectedVoice = this.voices.find(v => v.name.includes('Male')) || this.voices[1] || this.voices[0];
        }
    }

    setVolume(volume) {
        this.volume = Math.min(1, Math.max(0, volume / 100));
    }

    setRate(rate) {
        this.rate = rate;
    }

    setPitch(pitch) {
        this.pitch = pitch;
    }

    stop() {
        window.speechSynthesis.cancel();
    }

    pause() {
        window.speechSynthesis.pause();
    }

    resume() {
        window.speechSynthesis.resume();
    }

    getVoices() {
        return this.voices;
    }

    getVoiceNames() {
        return this.voices.map(v => v.name);
    }

    isSpeaking() {
        return window.speechSynthesis.speaking;
    }
}

// Export for use in other modules
window.TextToSpeechModule = TextToSpeechModule;
