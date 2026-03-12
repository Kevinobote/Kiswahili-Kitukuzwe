# 🚀 Quick Reference Card

## Modal Deployment Commands

```bash
# Activate environment
conda activate audio_ml

# Deploy/Update app
modal deploy modal_app.py

# View logs
modal app logs kiswahili-audio-pipeline

# List apps
modal app list

# Check usage
modal profile current
```

## Local Development

```bash
# Setup environment
chmod +x setup_env.sh
./setup_env.sh

# Activate environment
source sema-deployed/bin/activate

# Run locally
python main.py

# Access at
http://localhost:8000
```

## Git Commands

```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest
git pull origin main
```

## Project URLs

- **GitHub**: https://github.com/Kevinobote/Kiswahili-Kitukuzwe
- **Modal Dashboard**: https://modal.com/apps/viviannyamoraa/main/deployed/kiswahili-audio-pipeline
- **Local Dev**: http://localhost:8000

## File Structure

```
Deployed/
├── main.py              # FastAPI backend
├── modal_app.py         # Modal deployment
├── deploy_modal.sh      # Deploy script
├── requirements.txt     # Dependencies
├── README.md            # Main docs
│
├── frontend/            # Web UI
│   ├── index.html
│   └── static/
│       ├── app.js
│       └── style.css
│
├── models/              # ML Pipeline
│   ├── pipeline_manager.py
│   └── chunking_utils.py
│
├── schemas/             # API Models
│   └── response_models.py
│
└── docs/                # Documentation
    ├── MODAL_DEPLOYMENT.md
    ├── QUICK_REFERENCE.md
    └── ...
```

## Common Tasks

### Update Code and Redeploy
```bash
# 1. Make changes to code
# 2. Test locally (optional)
python main.py

# 3. Commit to git
git add .
git commit -m "Update: description"
git push origin main

# 4. Redeploy to Modal
conda activate audio_ml
modal deploy modal_app.py
```

### Add New Dependencies
```bash
# 1. Add to requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# 2. Update modal_app.py pip_install section
# 3. Redeploy
modal deploy modal_app.py
```

### Debug Issues
```bash
# View live logs
modal app logs kiswahili-audio-pipeline --follow

# Check local logs
tail -f logs/app.log

# Test locally first
python main.py
```

## Support

- **Modal Docs**: https://modal.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **GitHub Issues**: https://github.com/Kevinobote/Kiswahili-Kitukuzwe/issues
