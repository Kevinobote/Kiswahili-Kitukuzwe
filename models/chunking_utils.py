import librosa
import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class AudioChunker:
    """Handles audio segmentation for long files"""
    
    def __init__(self, chunk_duration: int = 30, overlap: float = 0.1):
        """
        Initialize audio chunker
        
        Args:
            chunk_duration: Duration of each chunk in seconds
            overlap: Overlap between chunks as fraction (0.1 = 10%)
        """
        self.chunk_duration = chunk_duration
        self.overlap = overlap
    
    def should_chunk_audio(self, audio_path: str) -> bool:
        """Check if audio file needs chunking"""
        try:
            audio, sr = librosa.load(audio_path, sr=None)
            duration = len(audio) / sr
            return duration > self.chunk_duration
        except Exception as e:
            logger.error(f"Error checking audio duration: {e}")
            return False
    
    def chunk_audio(self, audio_path: str) -> List[np.ndarray]:
        """Split audio into overlapping chunks"""
        try:
            audio, sr = librosa.load(audio_path, sr=16000)
            
            chunk_samples = int(self.chunk_duration * sr)
            overlap_samples = int(chunk_samples * self.overlap)
            step_size = chunk_samples - overlap_samples
            
            chunks = []
            start = 0
            
            while start < len(audio):
                end = min(start + chunk_samples, len(audio))
                chunk = audio[start:end]
                
                # Only add chunks with meaningful content
                if len(chunk) > sr:  # At least 1 second
                    chunks.append(chunk)
                
                start += step_size
                
                # Break if we've reached the end
                if end >= len(audio):
                    break
            
            logger.info(f"Split audio into {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error chunking audio: {e}")
            return []


class TextChunker:
    """Handles text segmentation for long transcriptions"""
    
    def __init__(self, max_tokens: int = 400):
        """
        Initialize text chunker
        
        Args:
            max_tokens: Maximum tokens per chunk (leave buffer for 512 limit)
        """
        self.max_tokens = max_tokens
    
    def should_chunk_text(self, text: str) -> bool:
        """Check if text needs chunking based on approximate token count"""
        # Rough approximation: 1 token ≈ 4 characters for most languages
        estimated_tokens = len(text) / 4
        return estimated_tokens > 512
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into smaller chunks preserving sentence boundaries"""
        if not self.should_chunk_text(text):
            return [text]
        
        # Split by sentences (handle multiple sentence endings)
        sentences = self._split_sentences(text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding this sentence would exceed limit
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            if self._estimate_tokens(test_chunk) <= self.max_tokens:
                current_chunk = test_chunk
            else:
                # Save current chunk and start new one
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Handle multiple sentence endings
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation"""
        return len(text) / 4


class ResultAggregator:
    """Aggregates results from multiple chunks"""
    
    @staticmethod
    def combine_transcriptions(transcriptions: List[str]) -> str:
        """Combine multiple transcriptions into one"""
        return " ".join(transcriptions).strip()
    
    @staticmethod
    def aggregate_sentiments(sentiments: List[dict]) -> dict:
        """Aggregate sentiment scores from multiple chunks"""
        if not sentiments:
            return {"label": "UNKNOWN", "score": 0.0}
        
        # Count labels and average scores
        label_counts = {}
        total_score = 0
        
        for sentiment in sentiments:
            label = sentiment["label"]
            score = sentiment["score"]
            
            if label not in label_counts:
                label_counts[label] = {"count": 0, "total_score": 0}
            
            label_counts[label]["count"] += 1
            label_counts[label]["total_score"] += score
            total_score += score
        
        # Find most common label
        most_common_label = max(label_counts.keys(), key=lambda x: label_counts[x]["count"])
        
        # Calculate weighted average score
        avg_score = total_score / len(sentiments)
        
        return {
            "label": most_common_label,
            "score": round(avg_score, 3)
        }
    
    @staticmethod
    def combine_summaries(summaries: List[str]) -> str:
        """Combine multiple summaries into one coherent summary"""
        # Filter out failed summaries
        valid_summaries = [s for s in summaries if s and "failed" not in s.lower()]
        
        if not valid_summaries:
            return "Summarization failed"
        
        # If only one valid summary, return it
        if len(valid_summaries) == 1:
            return valid_summaries[0]
        
        # Combine multiple summaries
        combined = ". ".join(valid_summaries)
        
        # Truncate if too long
        if len(combined) > 200:
            combined = combined[:197] + "..."
        
        return combined