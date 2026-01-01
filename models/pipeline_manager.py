import asyncio
import time
from transformers import pipeline
import librosa
import soundfile as sf
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessingPipeline:
    """Main pipeline for processing audio through ASR, sentiment analysis, and summarization"""
    
    def __init__(self):
        self.models_loaded = False
        self._load_models()
    
    def _load_models(self):
        """Load all required models"""
        try:
            logger.info("Loading ASR model...")
            self.asr_pipeline = pipeline(
                "automatic-speech-recognition", 
                model="RareElf/swahili-wav2vec2-asr"
            )
            
            logger.info("Loading sentiment analysis model...")
            self.sentiment_pipeline = pipeline(
                "text-classification", 
                model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
            )
            
            logger.info("Loading summarization model...")
            self.summarization_pipeline = pipeline(
                "summarization", 
                model="google-t5/t5-small"
            )
            
            self.models_loaded = True
            logger.info("All models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    async def process_audio(self, audio_path: str) -> Dict[str, Any]:
        """Process audio file through complete pipeline"""
        start_time = time.time()
        
        try:
            # Step 1: Speech Recognition
            transcription = await self._transcribe_audio(audio_path)
            
            # Step 2: Sentiment Analysis
            sentiment = await self._analyze_sentiment(transcription)
            
            # Step 3: Text Summarization
            summary = await self._summarize_text(transcription)
            
            processing_time = time.time() - start_time
            
            return {
                "transcription": transcription,
                "sentiment": sentiment,
                "summary": summary,
                "processing_time": round(processing_time, 2)
            }
            
        except Exception as e:
            logger.error(f"Pipeline processing error: {e}")
            raise
    
    async def _transcribe_audio(self, audio_path: str) -> str:
        """Convert audio to text using ASR model"""
        try:
            # Load and preprocess audio
            audio, sr = librosa.load(audio_path, sr=16000)
            
            # Run ASR in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: self.asr_pipeline(audio)
            )
            
            return result["text"]
            
        except Exception as e:
            logger.error(f"ASR error: {e}")
            return "Transcription failed"
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            if not text or text == "Transcription failed":
                return {"label": "UNKNOWN", "score": 0.0}
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.sentiment_pipeline(text)
            )
            
            return {
                "label": result[0]["label"],
                "score": round(result[0]["score"], 3)
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {"label": "ERROR", "score": 0.0}
    
    async def _summarize_text(self, text: str) -> str:
        """Generate summary of text"""
        try:
            if not text or text == "Transcription failed" or len(text.split()) < 10:
                return "Text too short for summarization"
            
            # Prepare text for T5 (add prefix for summarization task)
            input_text = f"summarize: {text}"
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.summarization_pipeline(
                    input_text,
                    max_length=100,
                    min_length=20,
                    do_sample=False
                )
            )
            
            return result[0]["summary_text"]
            
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return "Summarization failed"