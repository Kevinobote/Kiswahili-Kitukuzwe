from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import tempfile
import os
from pathlib import Path

from models.pipeline_manager import AudioProcessingPipeline
from schemas.response_models import ProcessingResponse

app = FastAPI(
    title="Kiswahili Audio Processing Pipeline",
    description="An integrated approach to speech recognition, sentiment analysis, and text summarization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the processing pipeline
pipeline = AudioProcessingPipeline()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
async def read_root():
    """Serve the main frontend page"""
    return FileResponse("frontend/index.html")

@app.post("/process-audio", response_model=ProcessingResponse)
async def process_audio(audio_file: UploadFile = File(...)):
    """
    Process audio file through the complete pipeline:
    1. Speech Recognition (ASR)
    2. Sentiment Analysis
    3. Text Summarization
    """
    if not audio_file.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Process through pipeline
        result = await pipeline.process_audio(temp_file_path)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        return result
        
    except Exception as e:
        # Clean up on error
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "models_loaded": pipeline.models_loaded}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)