from pydantic import BaseModel
from typing import Dict, Any

class ProcessingResponse(BaseModel):
    """Response model for audio processing results"""
    transcription: str
    sentiment: Dict[str, Any]
    summary: str
    processing_time: float
    
class SentimentResult(BaseModel):
    """Sentiment analysis result model"""
    label: str
    score: float