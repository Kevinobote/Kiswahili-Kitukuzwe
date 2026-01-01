# Kiswahili Audio Pipeline - Testing Guide

## 🚀 Quick Start

### 1. Setup & Run
```bash
# Clone and setup
git clone https://github.com/yourusername/kiswahili-audio-pipeline.git
cd kiswahili-audio-pipeline
chmod +x setup_env.sh
./setup_env.sh

# Activate environment
source sema-deployed/bin/activate

# Start server
python main.py
```

### 2. Access Points
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🧪 Testing Methods

### Web Interface Testing
1. Open http://localhost:8000
2. **Upload Audio**: Click "Choose File" → Select .wav/.mp3 file
3. **Record Audio**: Click "Start Recording" → Speak in Kiswahili → Stop
4. **Process**: Click "Process Audio"
5. **Results**: View transcription, sentiment, and summary

### API Testing (via /docs)
1. Go to http://localhost:8000/docs
2. Click "POST /process-audio"
3. Click "Try it out"
4. Upload audio file
5. Execute and view JSON response

### Command Line Testing
```bash
# Test with curl
curl -X POST "http://localhost:8000/process-audio" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@test_audio.wav"

# Health check
curl http://localhost:8000/health
```

## 📊 Expected Results

### Sample Response Format (Short Audio)
```json
{
  "transcription": "Habari za asubuhi, hali ya hewa ni nzuri leo",
  "sentiment": {
    "label": "POSITIVE",
    "score": 0.89
  },
  "summary": "Mazungumzo kuhusu hali ya hewa nzuri",
  "processing_time": 3.45
}
```

### Sample Response Format (Long Audio)
```json
{
  "transcription": "Full transcription from all chunks combined...",
  "sentiment": {
    "label": "POSITIVE",
    "score": 0.85
  },
  "summary": "Aggregated summary from multiple chunks",
  "processing_time": 12.34,
  "chunks_processed": 4
}
```

### Performance Expectations
- **First Run**: 30-60 seconds (model loading)
- **Short Audio (< 30s)**: 2-5 seconds
- **Long Audio (> 30s)**: 5-15 seconds (chunked processing)
- **Memory Usage**: 2-4GB RAM
- **Audio Length**: Now supports any length with chunking

## ⚠️ Common Issues & Solutions

### Model Loading
```
INFO: Loading ASR model...
INFO: Loading sentiment analysis model...
INFO: Loading summarization model...
INFO: All models loaded successfully
```

### Text Truncation Warning
```
Token indices sequence length is longer than the specified maximum sequence length for this model (527 > 512)
```
**Solution**: Normal for long audio - text gets truncated but still processes

### Invalid HTTP Requests
```
WARNING: Invalid HTTP request received.
```
**Solution**: Harmless browser pre-flight requests - ignore

### Audio Recording Issues
- **Chrome**: Requires HTTPS or localhost
- **Firefox**: May need microphone permissions
- **Safari**: Check browser audio settings

## 🔧 Testing Scenarios

### 1. Short Audio (< 30 seconds)
- Expected: Fast processing, complete transcription, no chunking
- Test with: Greetings, short phrases
- Response: Standard format without `chunks_processed`

### 2. Medium Audio (30 seconds - 2 minutes)
- Expected: Chunked processing, complete transcription, no truncation
- Test with: Conversations, stories
- Response: Includes `chunks_processed` field

### 3. Long Audio (> 2 minutes)
- Expected: Multiple chunks, full transcription, aggregated results
- Test with: Speeches, long recordings
- Response: Higher `chunks_processed` count, longer processing time

### 4. Very Long Text (> 512 tokens)
- Expected: Text chunking for sentiment/summary, no truncation warnings
- Test with: Long speeches, detailed conversations
- Response: Aggregated sentiment and combined summaries

### 4. Different Audio Formats
- **Supported**: .wav, .mp3, .m4a, .flac
- **Recommended**: .wav (16kHz, mono)

## 📝 Test Cases

### Positive Sentiment
- "Nimefurahi sana leo" (I'm very happy today)
- "Hali ya hewa ni nzuri" (The weather is good)

### Negative Sentiment  
- "Nimehuzunika" (I'm sad)
- "Hali mbaya" (Bad situation)

### Neutral Sentiment
- "Jina langu ni..." (My name is...)
- "Saa ni ngapi?" (What time is it?)

## 🐛 Debugging

### Check Logs
```bash
# Terminal output shows:
# - Model loading status
# - HTTP requests
# - Processing warnings
# - Error messages
```

### Memory Issues
```bash
# Check memory usage
htop
# or
free -h
```

### Port Conflicts
```bash
# If port 8000 is busy
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

## 🔧 New Chunking Features

### Audio Chunking
- **Automatic Detection**: Files > 30 seconds are automatically chunked
- **Overlap Processing**: 10% overlap between chunks for continuity
- **Seamless Combination**: Transcriptions are intelligently merged

### Text Chunking  
- **Token Limit Handling**: Texts > 512 tokens are automatically chunked
- **Sentence Preservation**: Chunks respect sentence boundaries
- **Result Aggregation**: Sentiments averaged, summaries combined

### Processing Indicators
```bash
# Look for these log messages:
INFO: Processing long audio with chunking
INFO: Processing audio chunk 1/3
INFO: Processing long text with chunking
INFO: Processing text chunk 1/2
```

## 🔄 Development Testing

### Code Changes
1. Stop server (Ctrl+C)
2. Make changes
3. Restart: `python main.py`
4. Test changes

### Model Updates
- Clear cache: `rm -rf ~/.cache/huggingface/`
- Restart application
- Models will re-download

## 📊 Performance Monitoring

### Success Indicators
- ✅ All models load without errors
- ✅ Web interface loads properly
- ✅ Audio processing returns results
- ✅ No critical errors in logs

### Warning Signs
- ❌ Model loading failures
- ❌ Memory errors
- ❌ Timeout errors
- ❌ Audio format errors

## 🚀 Next Steps

After successful testing:
1. Test with various Kiswahili audio samples
2. Experiment with different audio lengths
3. Try different audio qualities
4. Test concurrent requests
5. Monitor resource usage

## 📞 Support

- Check logs for detailed error messages
- Verify audio file formats and sizes
- Ensure sufficient RAM (4GB+)
- Test with different browsers for web interface