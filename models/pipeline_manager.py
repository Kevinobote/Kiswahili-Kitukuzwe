import asyncio
import time
from transformers import pipeline
import librosa
import soundfile as sf
from typing import Dict, Any, List
import logging
from .chunking_utils import AudioChunker, TextChunker, ResultAggregator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessingPipeline:
    """Main pipeline for processing audio through ASR, sentiment analysis, and summarization"""
    
    def __init__(self):
        self.models_loaded = False
        self.audio_chunker = AudioChunker(chunk_duration=30, overlap=0.1)
        self.text_chunker = TextChunker(max_tokens=400)
        self.aggregator = ResultAggregator()
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
        """Process audio file through complete pipeline with chunking support"""
        start_time = time.time()
        
        try:
            # Check if audio needs chunking
            if self.audio_chunker.should_chunk_audio(audio_path):
                logger.info("Processing long audio with chunking")
                return await self._process_long_audio(audio_path, start_time)
            else:
                logger.info("Processing short audio normally")
                return await self._process_short_audio(audio_path, start_time)
            
        except Exception as e:
            logger.error(f"Pipeline processing error: {e}")
            raise
    
    async def _process_short_audio(self, audio_path: str, start_time: float) -> Dict[str, Any]:
        """Process short audio using original method"""
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
    
    async def _process_long_audio(self, audio_path: str, start_time: float) -> Dict[str, Any]:
        """Process long audio using chunking strategy"""
        # Step 1: Chunk audio and transcribe each chunk
        audio_chunks = self.audio_chunker.chunk_audio(audio_path)
        transcriptions = []
        
        for i, chunk in enumerate(audio_chunks):
            logger.info(f"Processing audio chunk {i+1}/{len(audio_chunks)}")
            transcription = await self._transcribe_audio_chunk(chunk)
            transcriptions.append(transcription)
        
        # Combine transcriptions
        full_transcription = self.aggregator.combine_transcriptions(transcriptions)
        
        # Step 2: Process text with chunking if needed
        if self.text_chunker.should_chunk_text(full_transcription):
            logger.info("Processing long text with chunking")
            sentiment, summary = await self._process_long_text(full_transcription)
        else:
            sentiment = await self._analyze_sentiment(full_transcription)
            summary = await self._summarize_text(full_transcription)
        
        processing_time = time.time() - start_time
        
        return {
            "transcription": full_transcription,
            "sentiment": sentiment,
            "summary": summary,
            "processing_time": round(processing_time, 2),
            "chunks_processed": len(audio_chunks)
        }
    
    async def _process_long_text(self, text: str) -> tuple:
        """Process long text using chunking for sentiment and summarization"""
        text_chunks = self.text_chunker.chunk_text(text)
        
        # Process each chunk
        sentiments = []
        summaries = []
        
        for i, chunk in enumerate(text_chunks):
            logger.info(f"Processing text chunk {i+1}/{len(text_chunks)}")
            
            # Analyze sentiment for each chunk
            sentiment = await self._analyze_sentiment(chunk)
            sentiments.append(sentiment)
            
            # Summarize each chunk
            summary = await self._summarize_text(chunk)
            summaries.append(summary)
        
        # Aggregate results
        final_sentiment = self.aggregator.aggregate_sentiments(sentiments)
        final_summary = self.aggregator.combine_summaries(summaries)
        
        return final_sentiment, final_summary
    
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
    
    async def _transcribe_audio_chunk(self, audio_chunk) -> str:
        """Convert audio chunk to text using ASR model"""
        try:
            # Run ASR in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: self.asr_pipeline(audio_chunk)
            )
            
            return result["text"]
            
        except Exception as e:
            logger.error(f"ASR chunk error: {e}")
            return ""
    
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
                    max_new_tokens=256,
                    min_length=20,
                    do_sample=False
                )
            )
            
            return result[0]["summary_text"]
            
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return "Summarization failed"