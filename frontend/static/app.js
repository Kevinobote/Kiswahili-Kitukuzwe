class AudioProcessor {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.recordingStartTime = null;
        this.recordingInterval = null;
        this.currentResults = null;
        this.sentimentChart = null;
        this.initializeElements();
        this.bindEvents();
        this.setupDragAndDrop();
    }

    initializeElements() {
        this.audioFileInput = document.getElementById('audioFile');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.recordBtn = document.getElementById('recordBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.audioPlayback = document.getElementById('audioPlayback');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.uploadZone = document.getElementById('uploadZone');
        this.fileInfo = document.getElementById('fileInfo');
        this.recordingIndicator = document.getElementById('recordingIndicator');
    }

    bindEvents() {
        this.audioFileInput.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
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

        // Make upload zone clickable
        this.uploadZone.addEventListener('click', () => {
            this.audioFileInput.click();
        });
    }

    setupDragAndDrop() {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.uploadZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            this.uploadZone.addEventListener(eventName, () => {
                this.uploadZone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            this.uploadZone.addEventListener(eventName, () => {
                this.uploadZone.classList.remove('dragover');
            });
        });

        this.uploadZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });
    }

    handleFileSelect(file) {
        if (!file) return;

        // Display file info
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        
        fileName.textContent = file.name;
        fileSize.textContent = this.formatFileSize(file.size);
        this.fileInfo.classList.remove('d-none');
        
        this.uploadBtn.disabled = false;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            this.recordingStartTime = Date.now();

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
            this.recordingIndicator.classList.remove('d-none');
            
            // Start recording timer
            this.startRecordingTimer();
            
        } catch (error) {
            console.error('Error accessing microphone:', error);
            this.showError('Could not access microphone. Please check permissions.');
        }
    }

    startRecordingTimer() {
        this.recordingInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.recordingStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
            const seconds = (elapsed % 60).toString().padStart(2, '0');
            document.getElementById('recordingTime').textContent = `${minutes}:${seconds}`;
        }, 1000);
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
            
            this.isRecording = false;
            this.recordBtn.disabled = false;
            this.stopBtn.disabled = true;
            this.recordingIndicator.classList.add('d-none');
            
            // Stop recording timer
            if (this.recordingInterval) {
                clearInterval(this.recordingInterval);
                this.recordingInterval = null;
            }
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
            console.log('Sending request to /process-audio...');
            const response = await fetch('/process-audio', {
                method: 'POST',
                body: formData
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.detail || `HTTP error! status: ${response.status}`;
                throw new Error(errorMessage);
            }

            const result = await response.json();
            console.log('Received result:', result);
            
            this.currentResults = result;
            this.displayResults(result);
            
        } catch (error) {
            console.error('Processing error:', error);
            this.showError(`Error processing audio: ${error.message}`);
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
        console.log('Displaying results:', result);
        
        try {
            // Processing Metrics
            document.getElementById('processingTime').textContent = result.processing_time + 's';
            
            const wordCount = result.transcription.split(/\s+/).filter(w => w.length > 0).length;
            document.getElementById('wordCount').textContent = wordCount;
            
            const chunksProcessed = result.chunks_processed || 'N/A';
            document.getElementById('chunksProcessed').textContent = chunksProcessed;
            
            const confidenceScore = (result.sentiment.score * 100).toFixed(1);
            document.getElementById('confidenceScore').textContent = confidenceScore + '%';

            // Transcription
            document.getElementById('transcriptionText').textContent = result.transcription;

            // Sentiment Analysis
            this.displaySentiment(result.sentiment);

            // Summary
            document.getElementById('summaryText').textContent = result.summary;
            
            // Compression Ratio
            const summaryWords = result.summary.split(/\s+/).filter(w => w.length > 0).length;
            const compressionRatio = ((summaryWords / wordCount) * 100).toFixed(1);
            document.getElementById('compressionRatio').textContent = compressionRatio + '%';

            // Show results
            this.resultsSection.classList.remove('d-none');
            
            console.log('Results displayed successfully');
            
            // Scroll to results
            this.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } catch (error) {
            console.error('Error displaying results:', error);
            this.showError('Error displaying results: ' + error.message);
        }
    }

    displaySentiment(sentiment) {
        const sentimentLabel = document.getElementById('sentimentLabel');
        const sentimentIcon = document.getElementById('sentimentIcon');
        
        // Update label
        sentimentLabel.textContent = sentiment.label;
        sentimentLabel.className = `badge ${this.getSentimentBadgeClass(sentiment.label)}`;
        
        // Update icon
        const iconClass = this.getSentimentIconClass(sentiment.label);
        sentimentIcon.innerHTML = `<i class="${iconClass} fa-4x"></i>`;
        sentimentIcon.className = `sentiment-icon mb-3 ${sentiment.label.toLowerCase()}`;
        
        // Create sentiment chart
        this.createSentimentChart(sentiment);
    }

    createSentimentChart(sentiment) {
        const ctx = document.getElementById('sentimentChart');
        
        // Destroy existing chart if any
        if (this.sentimentChart) {
            this.sentimentChart.destroy();
        }
        
        const score = sentiment.score * 100;
        const remaining = 100 - score;
        
        this.sentimentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Confidence', 'Uncertainty'],
                datasets: [{
                    data: [score, remaining],
                    backgroundColor: [
                        this.getSentimentColor(sentiment.label),
                        '#e9ecef'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed.toFixed(1) + '%';
                            }
                        }
                    }
                },
                cutout: '70%'
            }
        });
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

    getSentimentIconClass(sentiment) {
        const iconMap = {
            'POSITIVE': 'fas fa-smile',
            'NEGATIVE': 'fas fa-frown',
            'NEUTRAL': 'fas fa-meh',
            'ERROR': 'fas fa-exclamation-triangle',
            'UNKNOWN': 'fas fa-question-circle'
        };
        return iconMap[sentiment] || 'fas fa-meh';
    }

    getSentimentColor(sentiment) {
        const colorMap = {
            'POSITIVE': '#28a745',
            'NEGATIVE': '#dc3545',
            'NEUTRAL': '#6c757d',
            'ERROR': '#ffc107',
            'UNKNOWN': '#17a2b8'
        };
        return colorMap[sentiment] || '#6c757d';
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

// Global functions for export and copy
function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

function exportResults(format) {
    const processor = window.audioProcessorInstance;
    if (!processor || !processor.currentResults) {
        showToast('No results to export', 'warning');
        return;
    }

    const results = processor.currentResults;
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    
    switch(format) {
        case 'json':
            exportJSON(results, `kiswahili-results-${timestamp}.json`);
            break;
        case 'csv':
            exportCSV(results, `kiswahili-results-${timestamp}.csv`);
            break;
        case 'txt':
            exportTXT(results, `kiswahili-results-${timestamp}.txt`);
            break;
    }
    
    showToast(`Results exported as ${format.toUpperCase()}`, 'success');
}

function exportJSON(data, filename) {
    const json = JSON.stringify(data, null, 2);
    downloadFile(json, filename, 'application/json');
}

function exportCSV(data, filename) {
    const csv = [
        ['Metric', 'Value'],
        ['Transcription', data.transcription],
        ['Sentiment Label', data.sentiment.label],
        ['Sentiment Score', data.sentiment.score],
        ['Summary', data.summary],
        ['Processing Time (s)', data.processing_time],
        ['Chunks Processed', data.chunks_processed || 'N/A']
    ].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');
    
    downloadFile(csv, filename, 'text/csv');
}

function exportTXT(data, filename) {
    const txt = `
KISWAHILI AUDIO PROCESSING RESULTS
===================================

TRANSCRIPTION:
${data.transcription}

SENTIMENT ANALYSIS:
Label: ${data.sentiment.label}
Confidence: ${(data.sentiment.score * 100).toFixed(2)}%

SUMMARY:
${data.summary}

PROCESSING METRICS:
Processing Time: ${data.processing_time}s
Chunks Processed: ${data.chunks_processed || 'N/A'}

Generated: ${new Date().toLocaleString()}
    `.trim();
    
    downloadFile(txt, filename, 'text/plain');
}

function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i> ${message}
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.audioProcessorInstance = new AudioProcessor();
});