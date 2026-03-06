// UI Utilities
class UIUtilities {
    static showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        alertDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid var(--primary-color);
            border-radius: 10px;
            color: var(--primary-color);
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(alertDiv);
        setTimeout(() => alertDiv.remove(), 3000);
    }

    static showLoading(element) {
        element.innerHTML = '<p class="loading">Loading...</p>';
    }

    static showError(element, message) {
        element.innerHTML = `<p class="error">${message}</p>`;
    }

    static showSuccess(element, message) {
        element.innerHTML = `<p class="success">${message}</p>`;
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    static throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Check for browser support
function checkBrowserSupport() {
    const support = {
        speechRecognition: !!(window.SpeechRecognition || window.webkitSpeechRecognition),
        speechSynthesis: !!window.speechSynthesis,
        microphone: !!navigator.mediaDevices || !!navigator.getUserMedia,
    };

    if (!support.speechRecognition) {
        console.warn('Speech Recognition not supported in this browser');
    }
    if (!support.speechSynthesis) {
        console.warn('Speech Synthesis not supported in this browser');
    }

    return support;
}

// Initialize on page load
const browserSupport = checkBrowserSupport();
if (!browserSupport.speechRecognition || !browserSupport.speechSynthesis) {
    console.warn('Some features may not be available in your browser');
}
