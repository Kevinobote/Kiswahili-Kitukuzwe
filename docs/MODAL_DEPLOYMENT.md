# Modal Deployment Guide

## 🚀 Deploy Kiswahili Audio Pipeline on Modal

Modal is a serverless platform perfect for ML applications. It handles infrastructure, scaling, and GPU/CPU resources automatically.

---

## 📋 Why Modal?

### Advantages
✅ **Serverless** - No server management  
✅ **Auto-scaling** - Handles traffic spikes automatically  
✅ **Cost-effective** - Pay only for compute time used  
✅ **Fast deployment** - Deploy in minutes  
✅ **GPU support** - Easy GPU access if needed  
✅ **Model caching** - Models cached between runs  
✅ **Perfect for research** - Great for PhD projects  

### Pricing (as of 2024)
- **Free tier**: $30/month credits
- **CPU**: ~$0.0001/second
- **Memory**: ~$0.000012/GB/second
- **Storage**: $0.10/GB/month

**Estimated cost for your app**: $10-30/month for moderate usage

---

## 🔧 Setup Instructions

### Step 1: Install Modal
```bash
# Install Modal CLI
pip install modal

# Or in your virtual environment
source sema-deployed/bin/activate
pip install modal
```

### Step 2: Create Modal Account
```bash
# Sign up and authenticate
modal setup

# This will:
# 1. Open browser for signup/login
# 2. Create API token
# 3. Save credentials locally
```

### Step 3: Verify Installation
```bash
# Test Modal
modal --help

# Check authentication
modal token list
```

---

## 📦 Deployment Files

### File 1: modal_app.py (Already Created)
This is your main Modal deployment file with:
- Model loading and caching
- FastAPI web interface
- Audio processing endpoint
- Health check endpoint

### File 2: Update Requirements (Optional)
```bash
# Add Modal to requirements
echo "modal>=0.63.0" >> requirements.txt
```

---

## 🚀 Deploy to Modal

### Quick Deploy (Development)
```bash
cd /home/obote/Documents/NLP/dissertation/Deployed

# Deploy the app
modal deploy modal_app.py

# You'll see output like:
# ✓ Created web function fastapi_app
# ✓ App deployed!
# 
# View your app at: https://your-username--kiswahili-audio-pipeline-fastapi-app.modal.run
```

### Production Deploy
```bash
# Deploy with production settings
modal deploy modal_app.py --name kiswahili-pipeline-prod
```

---

## 🌐 Access Your Deployed App

After deployment, Modal provides:

### Web Interface
```
https://your-username--kiswahili-audio-pipeline-fastapi-app.modal.run
```

### API Endpoints
```
# Health check
https://your-username--kiswahili-audio-pipeline-fastapi-app.modal.run/health

# Process audio
POST https://your-username--kiswahili-audio-pipeline-fastapi-app.modal.run/process-audio

# API docs
https://your-username--kiswahili-audio-pipeline-fastapi-app.modal.run/docs
```

---

## 🔧 Configuration Options

### Adjust Resources (in modal_app.py)

#### CPU and Memory
```python
@app.cls(
    cpu=4.0,      # 2.0, 4.0, 8.0 cores
    memory=8192,  # MB (4096, 8192, 16384)
)
```

#### Add GPU (if needed for faster processing)
```python
@app.cls(
    gpu="T4",     # T4, A10G, A100
    cpu=4.0,
    memory=16384,
)
```

#### Timeout Settings
```python
@app.cls(
    timeout=600,  # 10 minutes (adjust as needed)
)
```

#### Concurrent Requests
```python
@app.cls(
    allow_concurrent_inputs=10,  # Handle 10 requests simultaneously
)
```

---

## 📊 Monitoring & Management

### View Logs
```bash
# Real-time logs
modal app logs kiswahili-audio-pipeline

# Follow logs
modal app logs kiswahili-audio-pipeline --follow
```

### Check App Status
```bash
# List deployed apps
modal app list

# Get app details
modal app show kiswahili-audio-pipeline
```

### View Usage & Costs
```bash
# Check usage
modal profile current

# View in dashboard
# Go to: https://modal.com/dashboard
```

---

## 🔄 Update Deployment

### Update Code
```bash
# Make changes to your code
# Then redeploy
modal deploy modal_app.py

# Modal will:
# 1. Build new image
# 2. Deploy updated code
# 3. Keep models cached
# 4. Zero downtime deployment
```

### Force Rebuild
```bash
# Force rebuild image (if dependencies changed)
modal deploy modal_app.py --force-build
```

---

## 🎯 Custom Domain (Optional)

### Step 1: Get Custom Domain
Purchase domain from Namecheap, GoDaddy, etc.

### Step 2: Configure DNS
Add CNAME record:
```
Type: CNAME
Name: api (or your subdomain)
Value: your-username--kiswahili-audio-pipeline-fastapi-app.modal.run
```

### Step 3: Access via Custom Domain
```
https://api.yourdomain.com
```

---

## 💰 Cost Optimization

### 1. Use Smaller Resources for Testing
```python
@app.cls(
    cpu=2.0,      # Reduce CPU
    memory=4096,  # Reduce memory
)
```

### 2. Set Idle Timeout
```python
@app.cls(
    container_idle_timeout=300,  # 5 minutes
)
```

### 3. Use Scheduled Deployments
```python
# Only run during specific hours
@app.function(
    schedule=modal.Cron("0 9-17 * * 1-5")  # 9 AM - 5 PM, Mon-Fri
)
```

### 4. Monitor Usage
```bash
# Check daily usage
modal profile current

# Set budget alerts in Modal dashboard
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
```python
# Store secrets
@app.function(
    secrets=[modal.Secret.from_name("my-secret")]
)
def my_function():
    import os
    api_key = os.environ["API_KEY"]
```

### 2. Rate Limiting
```python
from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@web_app.post("/process-audio")
@limiter.limit("10/minute")  # 10 requests per minute
async def process_audio():
    pass
```

### 3. Authentication (Optional)
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@web_app.post("/process-audio")
async def process_audio(credentials = Depends(security)):
    # Verify token
    pass
```

---

## 🧪 Testing

### Local Testing
```bash
# Run locally (uses Modal infrastructure)
modal run modal_app.py

# Test specific function
modal run modal_app.py::KiswahiliPipeline.process_audio
```

### Test Deployed App
```bash
# Test health endpoint
curl https://your-app.modal.run/health

# Test with audio file
curl -X POST "https://your-app.modal.run/process-audio" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@test_audio.wav"
```

---

## 📱 Integration Examples

### Python Client
```python
import requests

url = "https://your-app.modal.run/process-audio"

with open("audio.wav", "rb") as f:
    files = {"audio_file": f}
    response = requests.post(url, files=files)
    result = response.json()
    print(result)
```

### JavaScript/Frontend
```javascript
const formData = new FormData();
formData.append('audio_file', audioFile);

const response = await fetch('https://your-app.modal.run/process-audio', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log(result);
```

### cURL
```bash
curl -X POST "https://your-app.modal.run/process-audio" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@audio.wav"
```

---

## 🐛 Troubleshooting

### Issue: Deployment Fails
```bash
# Check logs
modal app logs kiswahili-audio-pipeline

# Verify dependencies
modal run modal_app.py --debug
```

### Issue: Models Not Loading
```bash
# Clear cache and redeploy
modal volume delete kiswahili-models
modal deploy modal_app.py --force-build
```

### Issue: Timeout Errors
```python
# Increase timeout in modal_app.py
@app.cls(
    timeout=900,  # 15 minutes
)
```

### Issue: Out of Memory
```python
# Increase memory
@app.cls(
    memory=16384,  # 16GB
)
```

---

## 📊 Comparison: Modal vs Traditional Server

| Feature | Modal | Traditional Server |
|---------|-------|-------------------|
| Setup Time | 5 minutes | 1-2 hours |
| Scaling | Automatic | Manual |
| Maintenance | None | Regular |
| Cost (low traffic) | $10-30/month | $40-100/month |
| Cost (high traffic) | Scales with usage | Fixed |
| GPU Access | Easy | Complex |
| Deployment | One command | Multiple steps |
| Monitoring | Built-in | Setup required |

---

## ✅ Deployment Checklist

```
□ Modal account created
□ Modal CLI installed and authenticated
□ modal_app.py created
□ Dependencies verified
□ Local testing completed
□ Deployed to Modal
□ Web interface accessible
□ API endpoints tested
□ Logs checked
□ Usage monitored
□ Documentation updated with Modal URL
□ Shared with committee/peers
```

---

## 🎓 PhD Research Benefits

### Why Modal is Perfect for PhD Research:

1. **Quick Demonstrations**
   - Deploy in minutes for committee meetings
   - Share live URL with supervisors
   - No server maintenance during research

2. **Cost-Effective**
   - Free tier for development
   - Pay only for actual usage
   - No idle server costs

3. **Reproducibility**
   - Code + deployment config in one file
   - Easy to share with other researchers
   - Version control friendly

4. **Scalability**
   - Handle demo traffic spikes
   - Scale for user studies
   - No performance worries

5. **Focus on Research**
   - No DevOps required
   - More time for actual research
   - Professional deployment

---

## 📞 Quick Commands Reference

```bash
# Deploy
modal deploy modal_app.py

# View logs
modal app logs kiswahili-audio-pipeline --follow

# List apps
modal app list

# Stop app
modal app stop kiswahili-audio-pipeline

# Delete app
modal app delete kiswahili-audio-pipeline

# Check usage
modal profile current

# Update deployment
git pull
modal deploy modal_app.py
```

---

## 🌟 Next Steps

1. **Deploy Now**:
   ```bash
   modal deploy modal_app.py
   ```

2. **Test Your App**:
   Visit the provided URL

3. **Share with Committee**:
   Send them the Modal URL

4. **Monitor Usage**:
   Check Modal dashboard regularly

5. **Update as Needed**:
   Make changes and redeploy instantly

---

## 📚 Additional Resources

- **Modal Docs**: https://modal.com/docs
- **Modal Examples**: https://modal.com/docs/examples
- **Modal Discord**: https://discord.gg/modal
- **Pricing**: https://modal.com/pricing

---

**Your PhD research app is now serverless! 🎉**

Access at: `https://your-username--kiswahili-audio-pipeline-fastapi-app.modal.run`

**Estimated deployment time**: 5-10 minutes  
**Estimated monthly cost**: $10-30 (with free tier credits)