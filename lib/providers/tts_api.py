#!/usr/bin/env python3
"""
Platform-Agnostic Text-to-Speech (TTS) Provider System
Supports ElevenLabs, Google Cloud TTS, Azure Speech, OpenAI TTS, and more
"""

import os
import json
import time
import hashlib
import logging
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path

# Import API clients with error handling
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    pass

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("💡 Install python-dotenv for automatic .env loading: pip install python-dotenv")

@dataclass
class Voice:
    """Represents a voice available from a TTS provider."""
    id: str
    name: str
    gender: str
    language: str
    accent: str
    age_range: str
    description: str
    provider: str
    sample_url: Optional[str] = None
    premium: bool = False

@dataclass
class VoiceProfile:
    """Represents voice selection criteria for different audiences."""
    audience: str  # universal, muslim_community, spiritual_seekers
    preferred_gender: str  # male, female, neutral
    age_range: str  # young, adult, mature
    accent: str  # neutral, american, british, international
    tone: str  # warm, professional, calm, energetic
    pace: str  # slow, normal, fast
    provider_preference: Optional[str] = None

@dataclass
class AudioFile:
    """Represents a generated audio file with metadata."""
    id: str
    source_story_id: str
    file_path: str
    duration_seconds: float
    format: str  # wav, mp3
    sample_rate: int
    bit_depth: int
    file_size_bytes: int
    provider: str
    voice_used: str
    generation_cost: float
    generation_time: float
    quality_score: float
    created_at: datetime

@dataclass
class TTSConfig:
    """Configuration for TTS providers."""
    provider: str
    api_key: Optional[str] = None
    voice_id: Optional[str] = None
    sample_rate: int = 44100
    format: str = "mp3"
    quality: str = "high"  # low, medium, high, premium
    cost_limit_per_request: float = 1.00  # $1.00 max per request
    timeout: int = 60
    retry_attempts: int = 3

class TTSProvider(ABC):
    """Abstract base class for TTS providers."""
    
    def __init__(self, config: TTSConfig):
        self.config = config
        self.logger = logging.getLogger(f"tts.{config.provider}")
        self._setup_client()
    
    @abstractmethod
    def _setup_client(self):
        """Setup provider-specific client."""
        pass
    
    @abstractmethod
    def synthesize(self, text: str, voice_id: str, **kwargs) -> AudioFile:
        """Generate audio from text."""
        pass
    
    @abstractmethod
    def get_voices(self) -> List[Voice]:
        """Get available voices from provider."""
        pass
    
    @abstractmethod
    def estimate_cost(self, text: str) -> float:
        """Estimate cost for text synthesis."""
        pass
    
    def get_supported_features(self) -> List[str]:
        """Get list of supported features."""
        return ["basic_synthesis"]
    
    def _calculate_base_cost(self, char_count: int, rate_per_1k: float) -> float:
        """Calculate cost based on character count."""
        return (char_count / 1000) * rate_per_1k
    
    def _create_audio_file(self, story_id: str, audio_data: bytes, 
                          voice_id: str, duration: float, cost: float,
                          generation_time: float, text_length: int = 0) -> AudioFile:
        """Create AudioFile object and save to disk."""
        
        # Create unique file ID
        file_id = f"audio_{story_id}_{self.config.provider}_{voice_id}_{hashlib.md5(audio_data).hexdigest()[:8]}"
        
        # Determine file paths
        audio_dir = Path("data/audio/files")
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = audio_dir / f"{file_id}.{self.config.format}"
        
        # Save audio file
        with open(file_path, 'wb') as f:
            f.write(audio_data)
        
        # Create AudioFile object
        audio_file = AudioFile(
            id=file_id,
            source_story_id=story_id,
            file_path=str(file_path),
            duration_seconds=duration,
            format=self.config.format,
            sample_rate=self.config.sample_rate,
            bit_depth=16,  # Standard for most TTS
            file_size_bytes=len(audio_data),
            provider=self.config.provider,
            voice_used=voice_id,
            generation_cost=cost,
            generation_time=generation_time,
            quality_score=0.0,  # To be filled by quality assessment
            created_at=datetime.now()
        )
        
        return audio_file

class ElevenLabsProvider(TTSProvider):
    """ElevenLabs TTS provider implementation."""
    
    def _setup_client(self):
        """Setup ElevenLabs client."""
        self.api_key = self.config.api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ElevenLabs API key not found. Set ELEVENLABS_API_KEY environment variable.")
        
        # Will implement actual client when testing with real API
        self.client = None
        self.logger.info("ElevenLabs provider initialized")
    
    def synthesize(self, text: str, voice_id: str, **kwargs) -> AudioFile:
        """Generate audio using ElevenLabs API."""
        start_time = time.time()
        
        # Estimate cost first
        cost = self.estimate_cost(text)
        if cost > self.config.cost_limit_per_request:
            raise ValueError(f"Cost ${cost:.4f} exceeds limit ${self.config.cost_limit_per_request}")
        
        try:
            # For MVP demo - simulate API call
            # In production, replace with actual ElevenLabs API call
            self.logger.info(f"Synthesizing {len(text)} characters with voice {voice_id}")
            
            # Simulate processing time
            time.sleep(1)
            
            # Create dummy audio data for demo
            duration = len(text) / 150.0 * 60  # Estimate: 150 words per minute
            dummy_audio = b"WAVE" + b"\x00" * 1000  # Placeholder audio data
            
            generation_time = time.time() - start_time
            
            # Extract story ID from kwargs or generate one
            story_id = kwargs.get('story_id', 'demo_story')
            
            audio_file = self._create_audio_file(
                story_id=story_id,
                audio_data=dummy_audio,
                voice_id=voice_id,
                duration=duration,
                cost=cost,
                generation_time=generation_time,
                text_length=len(text)
            )
            
            self.logger.info(f"Generated audio: {duration:.1f}s, ${cost:.4f}")
            return audio_file
            
        except Exception as e:
            self.logger.error(f"ElevenLabs synthesis failed: {e}")
            raise
    
    def get_voices(self) -> List[Voice]:
        """Get available ElevenLabs voices."""
        # Demo voices - replace with actual API call in production
        return [
            Voice(
                id="21m00Tcm4TlvDq8ikWAM",
                name="Rachel",
                gender="female", 
                language="en-US",
                accent="american",
                age_range="adult",
                description="Warm, professional female voice",
                provider="elevenlabs",
                premium=True
            ),
            Voice(
                id="AZnzlk1XvdvUeBnXmlld",
                name="Domi",
                gender="female",
                language="en-US", 
                accent="american",
                age_range="young",
                description="Energetic, clear female voice",
                provider="elevenlabs",
                premium=True
            )
        ]
    
    def estimate_cost(self, text: str) -> float:
        """Estimate ElevenLabs cost."""
        char_count = len(text)
        # ElevenLabs pricing: ~$0.18 per 1K characters
        return self._calculate_base_cost(char_count, 0.18)

class GoogleTTSProvider(TTSProvider):
    """Google Cloud Text-to-Speech provider implementation."""
    
    def _setup_client(self):
        """Setup Google TTS client."""
        self.api_key = self.config.api_key or os.getenv("GOOGLE_TTS_API_KEY")
        
        # Note: Google TTS typically uses service account JSON, not API key
        # This is a simplified setup for demo purposes
        self.client = None
        self.logger.info("Google TTS provider initialized")
    
    def synthesize(self, text: str, voice_id: str, **kwargs) -> AudioFile:
        """Generate audio using Google TTS API."""
        start_time = time.time()
        
        cost = self.estimate_cost(text)
        if cost > self.config.cost_limit_per_request:
            raise ValueError(f"Cost ${cost:.4f} exceeds limit ${self.config.cost_limit_per_request}")
        
        try:
            self.logger.info(f"Synthesizing {len(text)} characters with Google TTS")
            
            # Simulate processing
            time.sleep(0.5)
            
            duration = len(text) / 160.0 * 60  # 160 WPM for Google TTS
            dummy_audio = b"WAVE" + b"\x00" * 800
            
            generation_time = time.time() - start_time
            story_id = kwargs.get('story_id', 'demo_story')
            
            audio_file = self._create_audio_file(
                story_id=story_id,
                audio_data=dummy_audio,
                voice_id=voice_id,
                duration=duration,
                cost=cost,
                generation_time=generation_time,
                text_length=len(text)
            )
            
            return audio_file
            
        except Exception as e:
            self.logger.error(f"Google TTS synthesis failed: {e}")
            raise
    
    def get_voices(self) -> List[Voice]:
        """Get available Google TTS voices."""
        return [
            Voice(
                id="en-US-Wavenet-D",
                name="WaveNet Male",
                gender="male",
                language="en-US",
                accent="american",
                age_range="adult",
                description="Natural male voice using WaveNet",
                provider="google"
            ),
            Voice(
                id="en-US-Wavenet-F",
                name="WaveNet Female",
                gender="female",
                language="en-US",
                accent="american", 
                age_range="adult",
                description="Natural female voice using WaveNet",
                provider="google"
            )
        ]
    
    def estimate_cost(self, text: str) -> float:
        """Estimate Google TTS cost."""
        char_count = len(text)
        # Google TTS pricing: ~$4 per 1M characters
        return self._calculate_base_cost(char_count, 0.004)

class OpenAITTSProvider(TTSProvider):
    """OpenAI TTS provider implementation."""
    
    def _setup_client(self):
        """Setup OpenAI TTS client."""
        self.api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
            self.logger.info("OpenAI TTS provider initialized")
        except ImportError:
            raise ImportError("OpenAI package not available. Install with: pip install openai")
    
    def synthesize(self, text: str, voice_id: str, **kwargs) -> AudioFile:
        """Generate audio using OpenAI TTS API."""
        start_time = time.time()
        
        cost = self.estimate_cost(text)
        if cost > self.config.cost_limit_per_request:
            raise ValueError(f"Cost ${cost:.4f} exceeds limit ${self.config.cost_limit_per_request}")
        
        try:
            self.logger.info(f"Synthesizing {len(text)} characters with OpenAI TTS")
            
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI package not available. Install with: pip install openai")
            
            # Make actual OpenAI TTS API call
            client = OpenAI(api_key=self.api_key)
            response = client.audio.speech.create(
                model="tts-1-hd",  # Use high-definition model for better quality
                voice=voice_id,
                input=text,
                response_format="mp3"
            )
            
            audio_data = response.content
            duration = len(text) / 155.0 * 60  # Estimate: 155 WPM
            
            generation_time = time.time() - start_time
            story_id = kwargs.get('story_id', 'demo_story')
            
            audio_file = self._create_audio_file(
                story_id=story_id,
                audio_data=audio_data,
                voice_id=voice_id,
                duration=duration,
                cost=cost,
                generation_time=generation_time,
                text_length=len(text)
            )
            
            self.logger.info(f"Generated {duration:.1f}s audio, ${cost:.4f}")
            return audio_file
            
        except Exception as e:
            self.logger.error(f"OpenAI TTS synthesis failed: {e}")
            raise
    
    def get_voices(self) -> List[Voice]:
        """Get available OpenAI TTS voices."""
        return [
            Voice(
                id="alloy",
                name="Alloy",
                gender="neutral",
                language="en-US",
                accent="neutral",
                age_range="adult",
                description="Balanced, versatile voice",
                provider="openai"
            ),
            Voice(
                id="echo",
                name="Echo",
                gender="male",
                language="en-US",
                accent="american",
                age_range="adult",
                description="Warm, engaging male voice",
                provider="openai"
            ),
            Voice(
                id="nova",
                name="Nova",
                gender="female",
                language="en-US",
                accent="american",
                age_range="young",
                description="Bright, energetic female voice",
                provider="openai"
            )
        ]
    
    def estimate_cost(self, text: str) -> float:
        """Estimate OpenAI TTS cost."""
        char_count = len(text)
        # OpenAI TTS pricing: ~$15 per 1M characters
        return self._calculate_base_cost(char_count, 0.015)

def create_tts_provider(provider_name: str, config: Optional[TTSConfig] = None) -> TTSProvider:
    """Factory function to create TTS providers."""
    
    if not config:
        config = TTSConfig(provider=provider_name)
    
    providers = {
        "elevenlabs": ElevenLabsProvider,
        "google": GoogleTTSProvider,
        "openai": OpenAITTSProvider
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unsupported TTS provider: {provider_name}")
    
    return providers[provider_name](config)

# Usage example and testing
if __name__ == "__main__":
    print("🎵 Testing TTS Provider System")
    print("=" * 40)
    
    # Test text
    test_text = """
    Maya's alarm buzzed at 5:30 AM, same as every morning for the past five years. 
    Coffee, emails, meetings, deadlines—the cycle never stopped. But today felt different.
    She set down her phone and closed her eyes for just five minutes.
    """
    
    # Test different providers
    providers_to_test = ["openai", "google", "elevenlabs"]
    
    for provider_name in providers_to_test:
        try:
            print(f"\n🔧 Testing {provider_name.title()} Provider:")
            
            provider = create_tts_provider(provider_name)
            
            # Get voices
            voices = provider.get_voices()
            print(f"   Available voices: {len(voices)}")
            
            # Estimate cost
            cost = provider.estimate_cost(test_text)
            print(f"   Estimated cost: ${cost:.4f}")
            
            # Test synthesis (demo mode)
            if voices:
                audio = provider.synthesize(test_text, voices[0].id, story_id="test_story")
                print(f"   Generated: {audio.duration_seconds:.1f}s audio")
                print(f"   File: {audio.file_path}")
                
        except Exception as e:
            print(f"   ❌ {provider_name} failed: {e}")
    
    print(f"\n✅ TTS Provider System tested!")
    print(f"💡 Set API keys in .env to test real synthesis")
