# Quick Modal Deployment - Using audio_ml Environment

## 🚀 Super Quick Deploy (3 Steps)

You already have Modal configured in your `audio_ml` conda environment!

### Step 1: Activate Environment
```bash
conda activate audio_ml
```

### Step 2: Navigate to Project
```bash
cd ~/Documents/NLP/dissertation/Deployed
```

### Step 3: Deploy
```bash
# Option A: Use the script
./deploy_modal.sh

# Option B: Deploy directly
modal deploy modal_app.py
```

**That's it!** Your app will be live in ~2-3 minutes! 🎉

---

## 📱 Access Your App

After deployment, you'll see output like:
```
✓ Created web function fastapi_app
✓ App deployed!

View your app at: https://obote--kiswahili-audio-pipeline-fastapi-app.modal.run
```

### Your URLs:
- **Web Interface**: `https://obote--kiswahili-audio-pipeline-fastapi-app.modal.run`
- **API Docs**: `https://obote--kiswahili-audio-pipeline-fastapi-app.modal.run/docs`
- **Health Check**: `https://obote--kiswahili-audio-pipeline-fastapi-app.modal.run/health`

---

## 🔧 Common Commands

### View Your Apps
```bash
conda activate audio_ml
modal app list
```

### View Logs (Real-time)
```bash
conda activate audio_ml
modal app logs kiswahili-audio-pipeline --follow
```

### Check Usage & Costs
```bash
conda activate audio_ml
modal profile current
```

### Update Deployment
```bash
conda activate audio_ml
cd ~/Documents/NLP/dissertation/Deployed
modal deploy modal_app.py
```

### Stop App
```bash
conda activate audio_ml
modal app stop kiswahili-audio-pipeline
```

### Delete App
```bash
conda activate audio_ml
modal app delete kiswahili-audio-pipeline
```

---

## 🎯 Quick Test

After deployment, test your app:

```bash
# Test health endpoint
curl https://obote--kiswahili-audio-pipeline-fastapi-app.modal.run/health

# Test with audio file
curl -X POST "https://obote--kiswahili-audio-pipeline-fastapi-app.modal.run/process-audio" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@test_audio.wav"
```

---

## 📊 Monitor Your Deployment

### Dashboard
Visit: https://modal.com/dashboard

You can see:
- Active apps
- Usage statistics
- Costs
- Logs
- Performance metrics

### Command Line
```bash
# Check status
conda activate audio_ml
modal app show kiswahili-audio-pipeline

# View recent logs
modal app logs kiswahili-audio-pipeline --tail 100

# Follow logs in real-time
modal app logs kiswahili-audio-pipeline --follow
```

---

## 🔄 Development Workflow

### Make Changes and Redeploy
```bash
# 1. Make your code changes
nano modal_app.py  # or any file

# 2. Activate environment
conda activate audio_ml

# 3. Redeploy
modal deploy modal_app.py

# That's it! Zero downtime deployment
```

### Test Locally First
```bash
conda activate audio_ml
modal run modal_app.py
```

---

## 💰 Cost Tracking

### Check Current Usage
```bash
conda activate audio_ml
modal profile current
```

### Expected Costs
```
Free tier: $30/month credits
Light usage: $5-15/month
Moderate usage: $15-30/month
Heavy usage: $30-50/month
```

### Cost Optimization Tips
1. Models are cached (no re-download costs)
2. Container stays warm for frequent requests
3. Only pay for actual compute time
4. No idle server costs

---

## 🐛 Troubleshooting

### Issue: "modal: command not found"
```bash
# Make sure you're in the right environment
conda activate audio_ml

# Verify Modal is installed
pip list | grep modal

# If not installed
pip install modal
```

### Issue: "Authentication failed"
```bash
conda activate audio_ml
modal token list

# If no tokens, re-authenticate
modal setup
```

### Issue: "Deployment failed"
```bash
# Check logs for errors
modal app logs kiswahili-audio-pipeline

# Try force rebuild
modal deploy modal_app.py --force-build
```

### Issue: "Models not loading"
```bash
# Clear model cache
modal volume delete kiswahili-models

# Redeploy
modal deploy modal_app.py
```

---

## 📝 Quick Reference Card

```bash
# ACTIVATE ENVIRONMENT
conda activate audio_ml

# DEPLOY
modal deploy modal_app.py

# VIEW LOGS
modal app logs kiswahili-audio-pipeline --follow

# CHECK STATUS
modal app list

# CHECK COSTS
modal profile current

# UPDATE
modal deploy modal_app.py

# STOP
modal app stop kiswahili-audio-pipeline
```

---

## 🎓 Share with Committee

After deployment, share this with your committee:

```
Dear Committee,

I've deployed the Kiswahili Audio Processing Pipeline for your review:

🌐 Web Interface:
https://obote--kiswahili-audio-pipeline-fastapi-app.modal.run

📚 API Documentation:
https://obote--kiswahili-audio-pipeline-fastapi-app.modal.run/docs

Features:
- Upload audio files or record directly
- Real-time speech recognition
- Sentiment analysis
- Text summarization
- Export results (JSON, CSV, TXT)

Please feel free to test with Kiswahili audio samples.

Best regards,
[Your Name]
```

---

## ✅ Deployment Checklist

```
□ Conda environment activated (audio_ml)
□ In project directory
□ Deployed with: modal deploy modal_app.py
□ Verified deployment successful
□ Tested web interface
□ Tested API endpoints
□ Checked logs for errors
□ Shared URL with committee
□ Monitoring usage/costs
```

---

## 🚀 You're All Set!

Your deployment is now:
- ✅ Live and accessible
- ✅ Auto-scaling
- ✅ Monitored
- ✅ Cost-effective
- ✅ Zero maintenance

**Focus on your research, Modal handles the rest!** 🎓✨

---

**Need help?**
- Modal Docs: https://modal.com/docs
- Modal Discord: https://discord.gg/modal
- Check logs: `modal app logs kiswahili-audio-pipeline --follow`