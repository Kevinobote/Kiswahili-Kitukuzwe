from pydantic import BaseModel
from typing import Dict, Any, Optional

class ProcessingResponse(BaseModel):
    """Response model for audio processing results"""
    transcription: str
    sentiment: Dict[str, Any]
    summary: str
    processing_time: float
    chunks_processed: Optional[int] = None  # Number of chunks processed (for long audio)
    
class SentimentResult(BaseModel):
    """Sentiment analysis result model"""
    label: str
    score: float