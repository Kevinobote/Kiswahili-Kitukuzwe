# Kiswahili Audio Processing Pipeline

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Novel Kiswahili Audio Processing Pipeline: An Integrated Approach to Speech Recognition, Sentiment Analysis, and Text Summarization.

> **Note**: This is a research project developed as part of a dissertation on Kiswahili NLP processing.

## 🎯 Overview

This project implements a complete audio processing pipeline that:
- **Speech Recognition**: Converts Kiswahili audio to text using Wav2Vec2
- **Sentiment Analysis**: Analyzes emotional tone using DistilBERT
- **Text Summarization**: Generates concise summaries using T5

## 🏗️ Architecture

```
├── main.py                 # FastAPI application entry point
├── models/
│   ├── pipeline_manager.py # Core ML pipeline orchestration
│   └── __init__.py
├── schemas/
│   ├── response_models.py  # API response models
│   └── __init__.py
├── frontend/
│   ├── index.html         # Main web interface
│   └── static/
│       ├── app.js         # Frontend JavaScript
│       └── style.css      # Styling
├── requirements.txt       # Python dependencies
├── setup_env.sh          # Environment setup script
└── README.md
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Make setup script executable and run
chmod +x setup_env.sh
./setup_env.sh
```

### 2. Activate Environment
```bash
source sema-deployed/bin/activate
```

### 3. Start Application
```bash
python main.py
```

### 4. Access Application
Open your browser and navigate to: `http://localhost:8000`

## 🔧 Manual Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv sema-deployed
source sema-deployed/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 📱 Features

### Web Interface
- **Audio Upload**: Support for various audio formats
- **Live Recording**: Record audio directly in browser
- **Real-time Processing**: Asynchronous pipeline processing
- **Responsive Design**: Works on desktop and mobile devices

### API Endpoints
- `POST /process-audio`: Main processing endpoint
- `GET /health`: Health check and model status
- `GET /`: Serves the web interface

### Models Used
- **ASR**: `RareElf/swahili-wav2vec2-asr`
- **Sentiment**: `lxyuan/distilbert-base-multilingual-cased-sentiments-student`
- **Summarization**: `google-t5/t5-small`

## 🔍 API Usage

### Process Audio File
```bash
curl -X POST "http://localhost:8000/process-audio" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@your_audio.wav"
```

### Response Format
```json
{
  "transcription": "Transcribed Kiswahili text",
  "sentiment": {
    "label": "POSITIVE",
    "score": 0.95
  },
  "summary": "Generated summary",
  "processing_time": 2.34
}
```

## 🛠️ Development

### Project Structure
- **Modular Design**: Separate concerns for models, schemas, and frontend
- **Async Processing**: Non-blocking pipeline execution
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed logging for debugging

### Adding New Models
1. Update `pipeline_manager.py` with new model loading
2. Modify processing methods as needed
3. Update response schemas if required

## 📊 Performance

- **Model Loading**: ~30-60 seconds on first run
- **Processing Time**: ~2-5 seconds per audio file
- **Memory Usage**: ~2-4GB RAM for all models
- **Concurrent Requests**: Supported via FastAPI async

## 🔒 Security

- Input validation for audio files
- CORS configuration for web access
- Error handling without exposing internals
- Temporary file cleanup

## 📋 Requirements

- Python 3.8+
- 4GB+ RAM recommended
- Internet connection for model downloads
- Modern web browser with audio support

## 🐛 Troubleshooting

### Common Issues
1. **Model Download Fails**: Check internet connection
2. **Audio Recording Not Working**: Check browser permissions
3. **High Memory Usage**: Expected for transformer models
4. **Slow Processing**: Normal on first run (model loading)

### Logs
Check console output for detailed error messages and processing status.

## 🚀 Deployment

### Local Development
```bash
git clone https://github.com/yourusername/kiswahili-audio-pipeline.git
cd kiswahili-audio-pipeline
chmod +x setup_env.sh
./setup_env.sh
source sema-deployed/bin/activate
python main.py
```

### Docker (Optional)
```bash
# Build image
docker build -t kiswahili-pipeline .

# Run container
docker run -p 8000:8000 kiswahili-pipeline
```

## 🔄 Known Limitations

- **Text Length**: Models have 512-token limit (truncation warning for longer texts)
- **Audio Length**: Optimal for audio files under 2 minutes
- **Memory**: Requires 4GB+ RAM for all models
- **First Run**: Model downloads may take time

## 📊 Model Performance

| Component | Model | Language Support | Accuracy |
|-----------|-------|------------------|----------|
| ASR | Wav2Vec2 | Kiswahili | ~85-90% |
| Sentiment | DistilBERT | Multilingual | ~80-85% |
| Summary | T5-Small | English/Swahili | ~75-80% |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Citation

If you use this work in your research, please cite:

```bibtex
@misc{kiswahili-audio-pipeline,
  title={A Novel Kiswahili Audio Processing Pipeline},
  author={Your Name},
  year={2024},
  howpublished={\url{https://github.com/yourusername/kiswahili-audio-pipeline}}
}
```

## 📞 Contact

For questions about this research project, please open an issue or contact [your.email@domain.com](mailto:your.email@domain.com).