# Server Deployment Guide

## 🚀 Complete Server Deployment Guide

This guide covers deploying the Kiswahili Audio Processing Pipeline to a production server.

---

## 📋 Prerequisites

### Server Requirements
```
OS: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
RAM: 8GB minimum (16GB recommended)
CPU: 4+ cores
Storage: 20GB+ free space
Network: Public IP address
Ports: 80 (HTTP), 443 (HTTPS), 8000 (application)
```

### Domain Setup (Optional but Recommended)
- Domain name pointing to your server IP
- SSL certificate (Let's Encrypt recommended)

---

## 🔧 Deployment Options

### Option 1: Direct Deployment (Simple)
### Option 2: Docker Deployment (Recommended)
### Option 3: Production Deployment with Nginx + Gunicorn

---

## 📦 Option 1: Direct Deployment (Simple)

### Step 1: Connect to Your Server
```bash
ssh username@your-server-ip
# or
ssh username@yourdomain.com
```

### Step 2: Update System
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### Step 3: Install Dependencies
```bash
# Install Python and system dependencies
sudo apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    libsndfile1 \
    ffmpeg \
    portaudio19-dev \
    python3-dev \
    build-essential \
    git \
    nginx \
    supervisor
```

### Step 4: Clone Repository
```bash
cd /opt
sudo git clone https://github.com/yourusername/kiswahili-audio-pipeline.git
sudo chown -R $USER:$USER kiswahili-audio-pipeline
cd kiswahili-audio-pipeline
```

### Step 5: Setup Environment
```bash
# Create virtual environment
python3.12 -m venv sema-deployed

# Activate environment
source sema-deployed/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Test Application
```bash
# Test run
python main.py

# Should see:
# INFO: All models loaded successfully
# INFO: Uvicorn running on http://0.0.0.0:8000
```

Press `Ctrl+C` to stop.

### Step 7: Create Systemd Service
```bash
sudo nano /etc/systemd/system/kiswahili-pipeline.service
```

Add this content:
```ini
[Unit]
Description=Kiswahili Audio Processing Pipeline
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/opt/kiswahili-audio-pipeline
Environment="PATH=/opt/kiswahili-audio-pipeline/sema-deployed/bin"
ExecStart=/opt/kiswahili-audio-pipeline/sema-deployed/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Replace `your-username` with your actual username.

### Step 8: Start Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable kiswahili-pipeline

# Start service
sudo systemctl start kiswahili-pipeline

# Check status
sudo systemctl status kiswahili-pipeline
```

### Step 9: Configure Firewall
```bash
# Allow port 8000
sudo ufw allow 8000/tcp

# Or if using firewalld
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### Step 10: Access Application
```
http://your-server-ip:8000
```

---

## 🐳 Option 2: Docker Deployment (Recommended)

### Step 1: Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, then verify
docker --version
```

### Step 2: Create Dockerfile
```bash
cd /opt/kiswahili-audio-pipeline
nano Dockerfile
```

Add this content:
```dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    portaudio19-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Pre-download models (optional, increases image size but faster startup)
# RUN python -c "from models.pipeline_manager import AudioProcessingPipeline; AudioProcessingPipeline()"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "main.py"]
```

### Step 3: Create docker-compose.yml
```bash
nano docker-compose.yml
```

Add this content:
```yaml
version: '3.8'

services:
  kiswahili-pipeline:
    build: .
    container_name: kiswahili-pipeline
    ports:
      - "8000:8000"
    volumes:
      - model-cache:/root/.cache/huggingface
    restart: unless-stopped
    environment:
      - TRANSFORMERS_CACHE=/root/.cache/huggingface
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  model-cache:
```

### Step 4: Build and Run
```bash
# Build image
docker-compose build

# Start container
docker-compose up -d

# Check logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Step 5: Access Application
```
http://your-server-ip:8000
```

### Docker Management Commands
```bash
# Stop container
docker-compose down

# Restart container
docker-compose restart

# View logs
docker-compose logs -f

# Update and restart
git pull
docker-compose build
docker-compose up -d
```

---

## 🌐 Option 3: Production Deployment with Nginx + Gunicorn

### Step 1: Install Gunicorn
```bash
cd /opt/kiswahili-audio-pipeline
source sema-deployed/bin/activate
pip install gunicorn uvicorn[standard]
```

### Step 2: Create Gunicorn Configuration
```bash
nano gunicorn_config.py
```

Add this content:
```python
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = 2  # Adjust based on CPU cores (2-4 for ML models)
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 300  # Increased for model loading
keepalive = 2

# Logging
accesslog = "/var/log/kiswahili-pipeline/access.log"
errorlog = "/var/log/kiswahili-pipeline/error.log"
loglevel = "info"

# Process naming
proc_name = "kiswahili-pipeline"

# Server mechanics
daemon = False
pidfile = "/var/run/kiswahili-pipeline.pid"
```

### Step 3: Create Log Directory
```bash
sudo mkdir -p /var/log/kiswahili-pipeline
sudo chown -R $USER:$USER /var/log/kiswahili-pipeline
```

### Step 4: Update Systemd Service
```bash
sudo nano /etc/systemd/system/kiswahili-pipeline.service
```

Update ExecStart line:
```ini
ExecStart=/opt/kiswahili-audio-pipeline/sema-deployed/bin/gunicorn -c gunicorn_config.py main:app
```

### Step 5: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/kiswahili-pipeline
```

Add this content:
```nginx
upstream kiswahili_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 100M;  # Allow large audio files

    location / {
        proxy_pass http://kiswahili_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    location /static {
        alias /opt/kiswahili-audio-pipeline/frontend/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Step 6: Enable Nginx Site
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/kiswahili-pipeline /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### Step 7: Setup SSL with Let's Encrypt (Recommended)
```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

### Step 8: Restart Services
```bash
sudo systemctl daemon-reload
sudo systemctl restart kiswahili-pipeline
sudo systemctl restart nginx
```

### Step 9: Access Application
```
https://your-domain.com
```

---

## 🔒 Security Hardening

### 1. Firewall Configuration
```bash
# UFW (Ubuntu/Debian)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Check status
sudo ufw status
```

### 2. Fail2Ban (Prevent Brute Force)
```bash
# Install
sudo apt-get install -y fail2ban

# Configure
sudo nano /etc/fail2ban/jail.local
```

Add:
```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true
```

```bash
# Start service
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Disable Root Login
```bash
sudo nano /etc/ssh/sshd_config
```

Set:
```
PermitRootLogin no
PasswordAuthentication no  # Use SSH keys only
```

```bash
sudo systemctl restart sshd
```

### 4. Regular Updates
```bash
# Setup automatic security updates
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## 📊 Monitoring & Maintenance

### 1. Check Application Status
```bash
# Systemd service
sudo systemctl status kiswahili-pipeline

# Docker
docker-compose ps
docker-compose logs -f

# Check if running
curl http://localhost:8000/health
```

### 2. View Logs
```bash
# Systemd service logs
sudo journalctl -u kiswahili-pipeline -f

# Application logs
tail -f /var/log/kiswahili-pipeline/error.log
tail -f /var/log/kiswahili-pipeline/access.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 3. Monitor Resources
```bash
# CPU and Memory
htop

# Disk usage
df -h

# Check specific process
ps aux | grep python
```

### 4. Setup Monitoring (Optional)
```bash
# Install Prometheus Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz
sudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter

# Create systemd service
sudo nano /etc/systemd/system/node_exporter.service
```

---

## 🔄 Updates & Maintenance

### Update Application
```bash
# Direct deployment
cd /opt/kiswahili-audio-pipeline
git pull
source sema-deployed/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart kiswahili-pipeline

# Docker deployment
cd /opt/kiswahili-audio-pipeline
git pull
docker-compose build
docker-compose up -d
```

### Backup Strategy
```bash
# Backup script
nano /opt/backup-pipeline.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup application
tar -czf $BACKUP_DIR/kiswahili-pipeline-$DATE.tar.gz \
    /opt/kiswahili-audio-pipeline \
    --exclude='sema-deployed' \
    --exclude='.git'

# Keep only last 7 backups
ls -t $BACKUP_DIR/kiswahili-pipeline-*.tar.gz | tail -n +8 | xargs rm -f

echo "Backup completed: $BACKUP_DIR/kiswahili-pipeline-$DATE.tar.gz"
```

```bash
chmod +x /opt/backup-pipeline.sh

# Add to crontab (daily at 2 AM)
crontab -e
```

Add:
```
0 2 * * * /opt/backup-pipeline.sh
```

---

## 🐛 Troubleshooting

### Issue: Service won't start
```bash
# Check logs
sudo journalctl -u kiswahili-pipeline -n 50

# Check if port is in use
sudo lsof -i :8000

# Check permissions
ls -la /opt/kiswahili-audio-pipeline
```

### Issue: Out of memory
```bash
# Check memory
free -h

# Reduce workers in gunicorn_config.py
workers = 1

# Add swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Issue: Models not loading
```bash
# Check disk space
df -h

# Clear cache and re-download
rm -rf ~/.cache/huggingface/
python -c "from models.pipeline_manager import AudioProcessingPipeline; AudioProcessingPipeline()"
```

### Issue: Nginx 502 Bad Gateway
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check Nginx error log
sudo tail -f /var/log/nginx/error.log

# Restart services
sudo systemctl restart kiswahili-pipeline
sudo systemctl restart nginx
```

---

## 📞 Quick Reference

### Service Management
```bash
# Start
sudo systemctl start kiswahili-pipeline

# Stop
sudo systemctl stop kiswahili-pipeline

# Restart
sudo systemctl restart kiswahili-pipeline

# Status
sudo systemctl status kiswahili-pipeline

# Logs
sudo journalctl -u kiswahili-pipeline -f
```

### Docker Management
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Logs
docker-compose logs -f

# Rebuild
docker-compose build && docker-compose up -d
```

---

## ✅ Deployment Checklist

```
□ Server meets minimum requirements
□ Domain name configured (if using)
□ Dependencies installed
□ Application cloned and configured
□ Virtual environment created
□ Models downloaded successfully
□ Service configured and running
□ Nginx configured (if using)
□ SSL certificate installed (if using)
□ Firewall configured
□ Monitoring setup
□ Backup strategy implemented
□ Documentation updated with server details
□ Tested from external network
```

---

**Your application is now deployed! 🎉**

Access it at: `http://your-server-ip:8000` or `https://your-domain.com`