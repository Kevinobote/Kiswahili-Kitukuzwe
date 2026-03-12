"""
Modal Deployment for Kiswahili Audio Processing Pipeline
PhD Research Project - Compatible with Modal 1.3.3
Reuses existing FastAPI backend from main.py
"""
import modal

app = modal.App("kiswahili-audio-pipeline")

# Build image with all dependencies and application code
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("libsndfile1", "ffmpeg", "portaudio19-dev")
    .pip_install(
        "fastapi==0.128.0",
        "uvicorn==0.40.0",
        "python-multipart==0.0.6",
        "transformers==4.57.3",
        "torch==2.9.1",
        "torchaudio==2.9.1",
        "librosa==0.11.0",
        "soundfile==0.13.1",
        "numpy==2.3.5",
    )
    .add_local_dir("models", "/root/models")
    .add_local_dir("schemas", "/root/schemas")
    .add_local_dir("frontend", "/root/frontend")
    .add_local_file("main.py", "/root/main.py")
)

# Persistent volume for model caching
model_cache = modal.Volume.from_name("kiswahili-models", create_if_missing=True)

@app.function(
    image=image,
    volumes={"/root/.cache/huggingface": model_cache},
    cpu=4.0,
    memory=8192,
    timeout=600,
)
@modal.asgi_app()
def fastapi_app():
    """Deploy existing FastAPI app from main.py"""
    import sys
    sys.path.insert(0, "/root")
    
    # Import your existing FastAPI app
    from main import app as web_app
    
    return web_app
