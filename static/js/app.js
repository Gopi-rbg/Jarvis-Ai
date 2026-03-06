// Main Jarvis App
class JarvisApp {
    constructor() {
        this.speechRecognition = new SpeechRecognitionModule();
        this.textToSpeech = new TextToSpeechModule();
        this.isProcessing = false;
        this.autoListen = true;
        this.conversationHistory = [];
        this.volume = 70;

        this.initializeEventListeners();
        this.loadSettings();
        this.setupSpeechRecognitionCallbacks();
        this.startTime();
    }

    initializeEventListeners() {
        // Mic button
        document.getElementById('micButton').addEventListener('click', () => this.toggleListening());

        // Control buttons
        document.getElementById('clearBtn').addEventListener('click', () => this.clearChat());
        document.getElementById('volumeBtn').addEventListener('click', () => this.toggleVolumeControl());
        document.getElementById('settingsBtn').addEventListener('click', () => this.showSection('settingsSection'));
        document.getElementById('settingsBtn2').addEventListener('click', () => this.showSection('settingsSection'));
        document.getElementById('historyBtn').addEventListener('click', () => this.showSection('historySection'));
        
        // Settings
        document.getElementById('saveSetting').addEventListener('click', () => this.saveSettings());
        document.getElementById('clearAllBtn').addEventListener('click', () => this.clearAllHistory());

        // Volume slider
        document.getElementById('volumeSlider').addEventListener('input', (e) => {
            this.volume = parseInt(e.target.value);
            this.textToSpeech.setVolume(this.volume);
        });

        // Home button (Logo)
        document.querySelector('.logo').addEventListener('click', () => this.showSection('dashboardSection'));
    }

    setupSpeechRecognitionCallbacks() {
        this.speechRecognition.onResult((type, data) => {
            switch (type) {
                case 'start':
                    this.updateStatus('Listening...');
                    break;
                case 'wake-word':
                    this.updateStatus('Wake word detected!');
                    this.playAudio('beep');
                    break;
                case 'command':
                    this.processCommand(data);
                    break;
                case 'interim':
                    this.updateInterimTranscript(data);
                    break;
                case 'end':
                    if (!this.isProcessing && this.autoListen) {
                        setTimeout(() => this.startListening(), 1000);
                    }
                    break;
            }
        });

        this.speechRecognition.onError((message, error) => {
            this.updateStatus('Error: ' + message);
            console.error('Speech recognition error:', error);
            if (this.autoListen && !this.isProcessing) {
                setTimeout(() => this.startListening(), 1000);
            }
        });
    }

    toggleListening() {
        if (this.speechRecognition.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    startListening() {
        if (!this.isProcessing && !this.speechRecognition.isListening) {
            this.updateStatus('Listening for wake word...');
            document.getElementById('micButton').classList.add('listening');
            document.getElementById('listeningIndicator').classList.add('active');
            this.speechRecognition.start();
        }
    }

    stopListening() {
        this.speechRecognition.stop();
        document.getElementById('micButton').classList.remove('listening');
        document.getElementById('listeningIndicator').classList.remove('active');
    }

    async processCommand(command) {
        this.isProcessing = true;
        this.updateStatus('Processing...');
        
        try {
            // Add user message to chat
            this.addMessageToChat(command, 'user');

            // Send to backend
            const response = await fetch('/core/api/process-command/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken'),
                },
                body: JSON.stringify({ text: command })
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const data = await response.json();
            
            // Add Jarvis response to chat
            this.addMessageToChat(data.response, 'jarvis');

            // Speak response
            await this.textToSpeech.speak(data.response, (event) => {
                if (event === 'end') {
                    this.updateStatus('Response complete');
                    if (this.autoListen) {
                        setTimeout(() => this.startListening(), 500);
                    }
                }
            });

            // Execute command if needed
            this.executeCommand(data.command_type, data.command_text);

        } catch (error) {
            console.error('Error processing command:', error);
            const errorMessage = 'Sorry, I encountered an error processing your request. Please try again.';
            this.addMessageToChat(errorMessage, 'jarvis');
            this.textToSpeech.speak(errorMessage);
            this.updateStatus('Ready');
        } finally {
            this.isProcessing = false;
        }
    }

    executeCommand(commandType, commandText) {
        switch (commandType) {
            case 'website':
                // Extract URL from command
                const websites = {
                    'youtube': 'https://www.youtube.com',
                    'google': 'https://www.google.com',
                    'github': 'https://www.github.com',
                    'linkedin': 'https://www.linkedin.com',
                    'twitter': 'https://www.twitter.com',
                    'facebook': 'https://www.facebook.com',
                };
                for (let [site, url] of Object.entries(websites)) {
                    if (commandText.toLowerCase().includes(site)) {
                        setTimeout(() => window.open(url, '_blank'), 500);
                        break;
                    }
                }
                break;
            case 'search':
                const match = commandText.match(/search[^a-z]*([a-z\s]+)/i);
                if (match) {
                    const query = encodeURIComponent(match[1].trim());
                    setTimeout(() => window.open(`https://www.google.com/search?q=${query}`, '_blank'), 500);
                }
                break;
            case 'music':
                // Open music player or streaming service
                setTimeout(() => window.open('https://www.spotify.com', '_blank'), 500);
                break;
        }
    }

    addMessageToChat(text, role) {
        const chatMessages = document.getElementById('chatMessages');
        
        // Remove welcome message if it exists
        const welcome = chatMessages.querySelector('.welcome-message');
        if (welcome) welcome.remove();

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div>${text}</div>
            <div class="message-time">${timeString}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    updateStatus(status) {
        document.getElementById('statusValue').textContent = status;
    }

    updateInterimTranscript(transcript) {
        // Optional: Show interim results in real-time
        console.log('Interim:', transcript);
    }

    toggleVolumeControl() {
        document.getElementById('volumeControl').classList.toggle('active');
    }

    clearChat() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <h2>Welcome to Jarvis</h2>
                <p>Your AI Voice Assistant</p>
                <p class="subtitle">Say "Jarvis" to activate, then give your command</p>
            </div>
        `;
        this.conversationHistory = [];
    }

    async clearAllHistory() {
        if (confirm('Are you sure you want to clear all conversation history?')) {
            try {
                const response = await fetch('/core/api/clear-history/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCookie('csrftoken'),
                    }
                });
                if (response.ok) {
                    alert('History cleared successfully');
                    this.loadHistory();
                }
            } catch (error) {
                console.error('Error clearing history:', error);
            }
        }
    }

    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.dashboard-section, .history-section, .settings-section').forEach(el => {
            el.classList.remove('active');
        });
        
        // Show selected section
        document.getElementById(sectionId).classList.add('active');

        // Special handling for history section
        if (sectionId === 'historySection') {
            this.loadHistory();
        }
    }

    async loadHistory() {
        const historyContainer = document.getElementById('historyContainer');
        historyContainer.innerHTML = '<p class="loading">Loading conversations...</p>';

        try {
            const response = await fetch('/core/api/conversation-history/', {
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                }
            });

            if (!response.ok) {
                historyContainer.innerHTML = '<p class="error">Failed to load history</p>';
                return;
            }

            const data = await response.json();
            const conversations = data.conversations;

            if (conversations.length === 0) {
                historyContainer.innerHTML = '<p class="loading">No conversations yet</p>';
                return;
            }

            historyContainer.innerHTML = '';
            conversations.forEach(conversation => {
                const messages = conversation.messages;
                const firstMessage = messages.find(m => m.role === 'user');
                const previewText = firstMessage ? firstMessage.content.substring(0, 50) : 'No message';
                const dateTime = new Date(conversation.created_at).toLocaleString();

                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                historyItem.innerHTML = `
                    <div class="history-time">${dateTime}</div>
                    <div class="history-preview">${previewText}...</div>
                    <div class="history-actions">
                        <button class="btn-small" onclick="jarvisApp.viewConversation(${conversation.id})">View</button>
                        <button class="btn-small" onclick="jarvisApp.deleteConversation(${conversation.id})">Delete</button>
                    </div>
                `;
                historyContainer.appendChild(historyItem);
            });
        } catch (error) {
            console.error('Error loading history:', error);
            historyContainer.innerHTML = '<p class="error">Error loading history</p>';
        }
    }

    async viewConversation(conversationId) {
        try {
            const response = await fetch(`/core/api/conversation/${conversationId}/`, {
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                }
            });

            if (!response.ok) {
                alert('Failed to load conversation');
                return;
            }

            const data = await response.json();
            this.clearChat();
            
            // Add all messages from conversation
            data.messages.forEach(message => {
                this.addMessageToChat(message.content, message.role);
            });

            this.showSection('dashboardSection');
        } catch (error) {
            console.error('Error viewing conversation:', error);
            alert('Error loading conversation');
        }
    }

    async deleteConversation(conversationId) {
        if (confirm('Delete this conversation?')) {
            try {
                await fetch(`/core/api/conversation/${conversationId}/delete/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': this.getCookie('csrftoken'),
                    }
                });
                this.loadHistory();
            } catch (error) {
                console.error('Error deleting conversation:', error);
            }
        }
    }

    saveSettings() {
        const voiceSelect = document.getElementById('voiceSelect').value;
        const autoListen = document.getElementById('autoListenCheck').checked;
        const darkMode = document.getElementById('darkModeCheck').checked;

        this.textToSpeech.setVoiceByType(voiceSelect);
        this.autoListen = autoListen;

        // Apply dark mode
        if (!darkMode) {
            document.body.style.filter = 'invert(1) hue-rotate(180deg)';
        } else {
            document.body.style.filter = 'none';
        }

        // Save to localStorage
        localStorage.setItem('jarvisSettings', JSON.stringify({
            voice: voiceSelect,
            autoListen: autoListen,
            darkMode: darkMode,
            volume: this.volume
        }));

        alert('Settings saved!');
    }

    loadSettings() {
        const settings = localStorage.getItem('jarvisSettings');
        if (settings) {
            const parsed = JSON.parse(settings);
            document.getElementById('voiceSelect').value = parsed.voice || 'female';
            document.getElementById('autoListenCheck').checked = parsed.autoListen !== false;
            document.getElementById('darkModeCheck').checked = parsed.darkMode !== false;
            document.getElementById('volumeSlider').value = parsed.volume || 70;
            
            this.autoListen = parsed.autoListen !== false;
            this.textToSpeech.setVoiceByType(parsed.voice || 'female');
            this.textToSpeech.setVolume(parsed.volume || 70);
        }
    }

    playAudio(type) {
        // Create a simple beep sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        if (type === 'beep') {
            oscillator.frequency.value = 800;
            oscillator.type = 'sine';
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
        }
    }

    startTime() {
        const updateTime = () => {
            const now = new Date();
            const timeString = now.toLocaleTimeString();
            document.getElementById('timeValue').textContent = timeString;
        };
        updateTime();
        setInterval(updateTime, 1000);
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize app when DOM is ready
let jarvisApp;
document.addEventListener('DOMContentLoaded', () => {
    jarvisApp = new JarvisApp();
    // Auto-start listening
    jarvisApp.startListening();
});
