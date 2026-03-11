# Quick Reference Guide - Enhanced Frontend

## 🚀 Getting Started

### Start the Application
```bash
cd kiswahili-audio-pipeline
source sema-deployed/bin/activate
python main.py
```

### Access the Interface
```
http://localhost:8000
```

---

## 📤 Input Methods

### Method 1: Upload Audio File
1. **Drag & Drop**: Drag audio file onto upload zone
2. **Or Click**: Click upload zone to browse files
3. **View Info**: File name and size displayed
4. **Process**: Click "Process Audio" button

**Supported Formats**: WAV, MP3, M4A, FLAC

### Method 2: Record Audio
1. **Start**: Click "Start Recording" button
2. **Allow**: Grant microphone permissions
3. **Speak**: Record your Kiswahili audio
4. **Watch**: Timer shows recording duration
5. **Stop**: Click "Stop Recording"
6. **Preview**: Audio playback available
7. **Auto-Process**: Processing starts automatically

---

## 📊 Understanding Results

### Metrics Dashboard
```
┌─────────────────────────────────────────┐
│ ⏱️ Processing Time: 3.45s               │
│ 📝 Word Count: 127 words                │
│ 📊 Chunks Processed: 2 (for long audio) │
│ 📈 Confidence: 95.2%                    │
└─────────────────────────────────────────┘
```

### Speech Recognition
- **Transcription**: Full text from audio
- **Model**: Wav2Vec2 (Kiswahili-specific)
- **Copy**: Click copy button for clipboard

### Sentiment Analysis
- **Label**: POSITIVE/NEGATIVE/NEUTRAL
- **Icon**: Visual sentiment indicator
- **Chart**: Confidence distribution
- **Score**: Percentage confidence

### Text Summary
- **Summary**: Condensed version of transcription
- **Model**: T5-Small
- **Ratio**: Compression percentage
- **Copy**: Click copy button

---

## 💾 Exporting Results

### Export Options
```
JSON → For programmatic analysis
CSV  → For spreadsheet/statistical tools
TXT  → For documentation/reports
```

### Export Process
1. Process audio and view results
2. Scroll to "Export Results" section
3. Click desired format button
4. File downloads automatically

### File Naming
```
Format: kiswahili-results-YYYY-MM-DD-HH-MM-SS.ext
Example: kiswahili-results-2024-03-11-14-30-45.json
```

---

## 🎯 Quick Actions

### Copy to Clipboard
- **Transcription**: Click copy button in transcription card
- **Summary**: Click copy button in summary card
- **Feedback**: Toast notification confirms copy

### View Documentation
- **API Docs**: Click "API Documentation" in footer
- **About**: Click "About" in footer for modal
- **GitHub**: Click "GitHub" link in footer

---

## 📱 Mobile Usage

### Optimized for Mobile
```
✓ Responsive layout
✓ Touch-friendly buttons
✓ Stacked cards
✓ Full functionality
```

### Mobile Tips
- Use portrait orientation for best experience
- Recording works on mobile browsers
- Export works on mobile devices
- Charts are touch-interactive

---

## 🔍 Interpreting Metrics

### Processing Time
- **< 5s**: Short audio, normal processing
- **5-10s**: Medium audio or chunked processing
- **> 10s**: Long audio with multiple chunks

### Word Count
- **< 50**: Short transcription
- **50-200**: Medium transcription
- **> 200**: Long transcription (may be chunked)

### Chunks Processed
- **N/A**: Short audio, no chunking needed
- **2-3**: Medium audio, chunked for processing
- **> 3**: Long audio, multiple chunks

### Confidence Score
- **> 90%**: High confidence
- **70-90%**: Good confidence
- **< 70%**: Lower confidence (review results)

---

## 🎨 Visual Indicators

### Sentiment Colors
```
🟢 Green (POSITIVE)   → Positive sentiment detected
🔴 Red (NEGATIVE)     → Negative sentiment detected
⚪ Gray (NEUTRAL)     → Neutral sentiment detected
🟡 Yellow (ERROR)     → Processing error
🔵 Blue (UNKNOWN)    → Unknown sentiment
```

### Recording States
```
🔴 Red Pulse → Currently recording
⏹️ Gray Stop → Recording stopped
🎤 Green Mic → Ready to record
```

---

## ⚠️ Troubleshooting

### Upload Issues
**Problem**: File won't upload
**Solution**: 
- Check file format (WAV, MP3, M4A, FLAC)
- Ensure file size < 100MB
- Try different browser

### Recording Issues
**Problem**: Recording not working
**Solution**:
- Grant microphone permissions
- Check browser compatibility
- Use HTTPS or localhost
- Try different browser

### Processing Errors
**Problem**: Processing fails
**Solution**:
- Check internet connection (first run)
- Verify audio file is valid
- Try shorter audio file
- Check console for errors

### Chart Not Showing
**Problem**: Sentiment chart missing
**Solution**:
- Refresh page
- Check browser JavaScript enabled
- Clear browser cache
- Try different browser

---

## 💡 Pro Tips

### For Best Results
```
✓ Use clear audio with minimal background noise
✓ Speak clearly in Kiswahili
✓ Keep recordings under 2 minutes for optimal speed
✓ Use WAV format for best quality
✓ Export results immediately after processing
```

### For Research
```
✓ Export in JSON for data analysis
✓ Use CSV for statistical software
✓ Document processing parameters
✓ Save timestamps for reproducibility
✓ Screenshot results for presentations
```

### For Demonstrations
```
✓ Use live recording feature
✓ Show metrics dashboard
✓ Explain sentiment visualization
✓ Export results for audience
✓ Use about modal for context
```

---

## 🔗 Quick Links

### Documentation
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Files
- **README.md**: General overview
- **DEPLOYMENT_GUIDE.md**: Deployment instructions
- **ARCHITECTURE.md**: Technical architecture
- **FRONTEND_DOCUMENTATION.md**: Frontend details
- **ENVIRONMENT.md**: Environment setup

---

## 📞 Support

### Getting Help
1. Check this quick reference
2. Review documentation files
3. Check browser console for errors
4. Review terminal logs
5. Open GitHub issue

### Common Questions

**Q: How long does processing take?**
A: 2-5 seconds for short audio, 5-15 seconds for long audio

**Q: What audio formats are supported?**
A: WAV, MP3, M4A, FLAC

**Q: Can I process multiple files?**
A: Currently one at a time (batch processing planned)

**Q: Is my audio data saved?**
A: No, audio is processed and immediately deleted

**Q: Can I use this offline?**
A: After first run (models downloaded), yes

---

## ✅ Checklist for First Use

```
□ Environment activated
□ Application running (python main.py)
□ Browser opened to localhost:8000
□ Microphone permissions granted (for recording)
□ Test audio file ready (optional)
□ Internet connection available (first run)
□ Models loaded successfully (check terminal)
```

---

**Quick Reference Version**: 1.0  
**Last Updated**: [Current Date]  
**For**: PhD Research Platform