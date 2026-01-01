class AudioProcessor {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.audioFileInput = document.getElementById('audioFile');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.recordBtn = document.getElementById('recordBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.audioPlayback = document.getElementById('audioPlayback');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
    }

    bindEvents() {
        this.audioFileInput.addEventListener('change', () => {
            this.uploadBtn.disabled = !this.audioFileInput.files.length;
        });

        this.uploadBtn.addEventListener('click', () => {
            this.processUploadedFile();
        });

        this.recordBtn.addEventListener('click', () => {
            this.startRecording();
        });

        this.stopBtn.addEventListener('click', () => {
            this.stopRecording();
        });
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                
                this.audioPlayback.src = audioUrl;
                this.audioPlayback.classList.remove('d-none');
                
                // Process recorded audio
                this.processAudioBlob(audioBlob);
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            
            this.recordBtn.disabled = true;
            this.stopBtn.disabled = false;
            this.recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Recording...';
            
        } catch (error) {
            console.error('Error accessing microphone:', error);
            this.showError('Could not access microphone. Please check permissions.');
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
            
            this.isRecording = false;
            this.recordBtn.disabled = false;
            this.stopBtn.disabled = true;
            this.recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
        }
    }

    async processUploadedFile() {
        const file = this.audioFileInput.files[0];
        if (!file) return;

        await this.processAudioFile(file);
    }

    async processAudioBlob(blob) {
        const file = new File([blob], 'recorded_audio.wav', { type: 'audio/wav' });
        await this.processAudioFile(file);
    }

    async processAudioFile(file) {
        this.showLoading();
        
        const formData = new FormData();
        formData.append('audio_file', file);

        try {
            const response = await fetch('/process-audio', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.displayResults(result);
            
        } catch (error) {
            console.error('Processing error:', error);
            this.showError('Error processing audio. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        this.loadingSection.classList.remove('d-none');
        this.resultsSection.classList.add('d-none');
    }

    hideLoading() {
        this.loadingSection.classList.add('d-none');
    }

    displayResults(result) {
        // Transcription
        document.getElementById('transcriptionText').textContent = result.transcription;

        // Sentiment
        const sentimentLabel = document.getElementById('sentimentLabel');
        sentimentLabel.textContent = result.sentiment.label;
        sentimentLabel.className = `badge ${this.getSentimentBadgeClass(result.sentiment.label)}`;
        
        document.getElementById('sentimentScore').textContent = `${(result.sentiment.score * 100).toFixed(1)}%`;

        // Summary
        document.getElementById('summaryText').textContent = result.summary;

        // Processing time
        document.getElementById('processingTime').textContent = result.processing_time;

        // Show results
        this.resultsSection.classList.remove('d-none');
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    getSentimentBadgeClass(sentiment) {
        const sentimentMap = {
            'POSITIVE': 'bg-success',
            'NEGATIVE': 'bg-danger',
            'NEUTRAL': 'bg-secondary',
            'ERROR': 'bg-warning',
            'UNKNOWN': 'bg-info'
        };
        return sentimentMap[sentiment] || 'bg-secondary';
    }

    showError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.querySelector('.container-fluid').insertBefore(
            alertDiv, 
            document.querySelector('.row')
        );
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new AudioProcessor();
});