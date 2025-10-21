#!/usr/bin/env python3
"""
TTS Manager and Voice Selection System
Unified interface for managing multiple TTS providers with intelligent voice selection
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# Import our TTS providers
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.providers.tts_api import (
    TTSProvider, TTSConfig, Voice, VoiceProfile, AudioFile,
    create_tts_provider, ElevenLabsProvider, GoogleTTSProvider, OpenAITTSProvider
)

class VoiceSelector:
    """Intelligent voice selection system for different audiences and content types."""
    
    def __init__(self):
        self.voice_mappings = self._initialize_voice_mappings()
        self.logger = logging.getLogger("voice_selector")
    
    def _initialize_voice_mappings(self) -> Dict[str, Dict]:
        """Initialize audience-specific voice selection criteria."""
        return {
            "universal": {
                "preferred_providers": ["openai", "google", "elevenlabs"],
                "voice_criteria": {
                    "gender": "neutral",  # Inclusive for all audiences
                    "age_range": "adult",
                    "tone": "warm",
                    "pace": "normal",
                    "accent": "neutral"
                },
                "fallback_voices": {
                    "openai": "alloy",
                    "google": "en-US-Wavenet-D", 
                    "elevenlabs": "21m00Tcm4TlvDq8ikWAM"
                }
            },
            "muslim_community": {
                "preferred_providers": ["google", "openai", "elevenlabs"],
                "voice_criteria": {
                    "gender": "neutral",
                    "age_range": "adult",
                    "tone": "respectful",
                    "pace": "thoughtful",
                    "accent": "international"
                },
                "fallback_voices": {
                    "google": "en-US-Wavenet-F",
                    "openai": "echo",
                    "elevenlabs": "21m00Tcm4TlvDq8ikWAM"
                }
            },
            "spiritual_seekers": {
                "preferred_providers": ["elevenlabs", "openai", "google"],
                "voice_criteria": {
                    "gender": "neutral",
                    "age_range": "mature",
                    "tone": "calm",
                    "pace": "slow",
                    "accent": "neutral"
                },
                "fallback_voices": {
                    "elevenlabs": "21m00Tcm4TlvDq8ikWAM",
                    "openai": "alloy",
                    "google": "en-US-Wavenet-D"
                }
            }
        }
    
    def select_voice(self, audience: str, provider: str, available_voices: List[Voice]) -> Optional[Voice]:
        """Select the best voice for the given audience and provider."""
        
        if audience not in self.voice_mappings:
            self.logger.warning(f"Unknown audience: {audience}, using universal")
            audience = "universal"
        
        criteria = self.voice_mappings[audience]["voice_criteria"]
        fallback_id = self.voice_mappings[audience]["fallback_voices"].get(provider)
        
        # Score voices based on criteria
        best_voice = None
        best_score = -1
        
        for voice in available_voices:
            if voice.provider != provider:
                continue
                
            score = self._score_voice(voice, criteria)
            
            if score > best_score:
                best_score = score
                best_voice = voice
        
        # If no good match found, use fallback
        if not best_voice and fallback_id:
            for voice in available_voices:
                if voice.id == fallback_id:
                    best_voice = voice
                    break
        
        if best_voice:
            self.logger.info(f"Selected voice '{best_voice.name}' for {audience} audience")
        else:
            self.logger.warning(f"No suitable voice found for {audience} on {provider}")
        
        return best_voice
    
    def _score_voice(self, voice: Voice, criteria: Dict) -> float:
        """Score a voice based on how well it matches the criteria."""
        score = 0.0
        
        # Gender matching (high weight)
        if criteria.get("gender") == "neutral" or voice.gender == criteria.get("gender"):
            score += 3.0
        elif voice.gender == "neutral":
            score += 2.0
        
        # Age range matching
        if voice.age_range == criteria.get("age_range"):
            score += 2.0
        
        # Accent matching
        accent_pref = criteria.get("accent", "neutral")
        if voice.accent == accent_pref or (accent_pref == "neutral" and voice.accent in ["neutral", "american"]):
            score += 2.0
        
        # Provider premium bonus
        if voice.premium:
            score += 1.0
        
        return score
    
    def get_recommended_providers(self, audience: str) -> List[str]:
        """Get recommended providers for an audience, in order of preference."""
        if audience in self.voice_mappings:
            return self.voice_mappings[audience]["preferred_providers"]
        return self.voice_mappings["universal"]["preferred_providers"]

class TTSManager:
    """High-level manager for TTS operations with multiple providers and intelligent voice selection."""
    
    def __init__(self, 
                 provider_configs: Optional[Dict[str, TTSConfig]] = None,
                 default_provider: str = "openai"):
        
        self.providers = {}
        self.voice_selector = VoiceSelector()
        self.default_provider = default_provider
        self.usage_stats = {
            'total_requests': 0,
            'total_cost': 0.0,
            'total_duration': 0.0,
            'provider_usage': {}
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("tts_manager")
        
        # Initialize providers
        self._initialize_providers(provider_configs or {})
    
    def _initialize_providers(self, configs: Dict[str, TTSConfig]):
        """Initialize available TTS providers."""
        
        # Default configurations
        default_configs = {
            "openai": TTSConfig(provider="openai", cost_limit_per_request=0.50),
            "google": TTSConfig(provider="google", cost_limit_per_request=0.10),
            "elevenlabs": TTSConfig(provider="elevenlabs", cost_limit_per_request=1.00)
        }
        
        # Merge with provided configs
        for provider_name, default_config in default_configs.items():
            config = configs.get(provider_name, default_config)
            
            try:
                provider = create_tts_provider(provider_name, config)
                self.providers[provider_name] = provider
                self.usage_stats['provider_usage'][provider_name] = {
                    'requests': 0, 'cost': 0.0, 'duration': 0.0
                }
                self.logger.info(f"Initialized {provider_name} TTS provider")
                
            except Exception as e:
                self.logger.warning(f"Failed to initialize {provider_name}: {e}")
    
    def generate_audio(self, story: Dict, audience: str = "universal", 
                      preferred_provider: Optional[str] = None) -> Optional[AudioFile]:
        """Generate audio from story with intelligent provider and voice selection."""
        
        story_id = story.get('id', 'unknown_story')
        content = story.get('content', '')
        
        if not content:
            self.logger.error(f"No content found in story {story_id}")
            return None
        
        # Clean content for TTS
        clean_content = self._clean_content_for_tts(content)
        
        # Determine provider preference order
        if preferred_provider and preferred_provider in self.providers:
            provider_order = [preferred_provider]
        else:
            provider_order = self.voice_selector.get_recommended_providers(audience)
            provider_order = [p for p in provider_order if p in self.providers]
        
        if not provider_order:
            provider_order = [self.default_provider] if self.default_provider in self.providers else list(self.providers.keys())
        
        # Try providers in order until one succeeds
        for provider_name in provider_order:
            try:
                provider = self.providers[provider_name]
                
                # Get available voices
                available_voices = provider.get_voices()
                
                # Select best voice for audience
                selected_voice = self.voice_selector.select_voice(audience, provider_name, available_voices)
                
                if not selected_voice:
                    self.logger.warning(f"No suitable voice found for {provider_name}")
                    continue
                
                # Check cost before generation
                estimated_cost = provider.estimate_cost(clean_content)
                
                self.logger.info(f"Generating audio with {provider_name}/{selected_voice.name} (${estimated_cost:.4f})")
                
                # Generate audio
                audio_file = provider.synthesize(
                    text=clean_content,
                    voice_id=selected_voice.id,
                    story_id=story_id
                )
                
                # Update usage statistics
                self._update_usage_stats(provider_name, audio_file)
                
                self.logger.info(f"Generated {audio_file.duration_seconds:.1f}s audio for story {story_id}")
                return audio_file
                
            except Exception as e:
                self.logger.error(f"Audio generation failed with {provider_name}: {e}")
                continue
        
        self.logger.error(f"All TTS providers failed for story {story_id}")
        return None
    
    def _clean_content_for_tts(self, content: str) -> str:
        """Clean story content for optimal TTS processing."""
        
        # Remove markdown formatting
        import re
        
        # Remove bold/italic markers
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
        content = re.sub(r'\*(.*?)\*', r'\1', content)
        
        # Remove section headers
        content = re.sub(r'\*\*[A-Z\s]+\*\*[:\s]*', '', content)
        
        # Clean up multiple spaces and newlines
        content = re.sub(r'\n+', '\n', content)
        content = re.sub(r'\s+', ' ', content)
        
        # Remove structural markers
        content = content.replace('**HOOK:**', '')
        content = content.replace('**TITLE:**', '')
        content = content.replace('**STORY CONTENT:**', '')
        content = content.replace('**DESCRIPTION:**', '')
        
        return content.strip()
    
    def _update_usage_stats(self, provider_name: str, audio_file: AudioFile):
        """Update usage statistics."""
        self.usage_stats['total_requests'] += 1
        self.usage_stats['total_cost'] += audio_file.generation_cost
        self.usage_stats['total_duration'] += audio_file.duration_seconds
        
        provider_stats = self.usage_stats['provider_usage'][provider_name]
        provider_stats['requests'] += 1
        provider_stats['cost'] += audio_file.generation_cost
        provider_stats['duration'] += audio_file.duration_seconds
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics."""
        return self.usage_stats.copy()
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names."""
        return list(self.providers.keys())
    
    def get_provider_info(self, provider_name: str) -> Optional[Dict]:
        """Get information about a specific provider."""
        if provider_name not in self.providers:
            return None
        
        provider = self.providers[provider_name]
        voices = provider.get_voices()
        
        return {
            "name": provider_name,
            "available_voices": len(voices),
            "voice_samples": [{"id": v.id, "name": v.name, "gender": v.gender} for v in voices[:3]],
            "supported_features": provider.get_supported_features(),
            "usage_stats": self.usage_stats['provider_usage'].get(provider_name, {})
        }
    
    def compare_providers(self, sample_text: str) -> Dict:
        """Compare cost and estimated quality across providers."""
        comparison = {}
        
        for provider_name, provider in self.providers.items():
            try:
                cost = provider.estimate_cost(sample_text)
                voices = provider.get_voices()
                
                comparison[provider_name] = {
                    "estimated_cost": cost,
                    "available_voices": len(voices),
                    "cost_per_minute": cost / (len(sample_text) / 150.0) if sample_text else 0,  # Assuming 150 WPM
                    "premium_voices": sum(1 for v in voices if getattr(v, 'premium', False))
                }
                
            except Exception as e:
                comparison[provider_name] = {"error": str(e)}
        
        return comparison

def create_default_tts_manager() -> TTSManager:
    """Create a TTS manager with default settings optimized for Guidora."""
    
    # Optimized configs for our use case
    configs = {
        "openai": TTSConfig(
            provider="openai",
            quality="high",
            cost_limit_per_request=0.25,  # Reasonable for 2-3 min stories
            sample_rate=44100
        ),
        "google": TTSConfig(
            provider="google", 
            quality="high",
            cost_limit_per_request=0.10,  # Budget-friendly option
            sample_rate=44100
        ),
        "elevenlabs": TTSConfig(
            provider="elevenlabs",
            quality="premium",
            cost_limit_per_request=0.50,  # Premium option
            sample_rate=44100
        )
    }
    
    return TTSManager(provider_configs=configs, default_provider="openai")

# Usage example and testing
if __name__ == "__main__":
    print("🎵 Testing TTS Manager System")
    print("=" * 50)
    
    # Create TTS manager
    manager = create_default_tts_manager()
    
    print(f"📊 Available providers: {manager.get_available_providers()}")
    
    # Test sample story
    sample_story = {
        "id": "test_story_001",
        "content": """Maya's alarm buzzed at 5:30 AM, same as every morning for the past five years. 
        Coffee, emails, meetings, deadlines—the cycle never stopped. But today felt different.
        
        She set down her phone and closed her eyes for just five minutes. No meditation app, 
        no special technique—just breathing and thinking about the day ahead with intention."""
    }
    
    # Test different audiences
    audiences = ["universal", "muslim_community", "spiritual_seekers"]
    
    for audience in audiences:
        print(f"\n🎯 Testing {audience} audience:")
        
        # Compare providers for this audience
        comparison = manager.compare_providers(sample_story["content"])
        print(f"   Provider comparison:")
        for provider, stats in comparison.items():
            if "error" not in stats:
                print(f"     {provider}: ${stats['estimated_cost']:.4f}, {stats['available_voices']} voices")
            else:
                print(f"     {provider}: {stats['error']}")
        
        # Generate audio (demo mode)
        try:
            audio = manager.generate_audio(sample_story, audience=audience)
            if audio:
                print(f"   ✅ Generated: {audio.duration_seconds:.1f}s, ${audio.generation_cost:.4f}")
                print(f"   Provider: {audio.provider}, Voice: {audio.voice_used}")
            else:
                print(f"   ❌ Audio generation failed")
        except Exception as e:
            print(f"   ⚠️ Demo mode: {e}")
    
    # Show usage statistics
    stats = manager.get_usage_stats()
    print(f"\n📊 Usage Statistics:")
    print(f"   Total requests: {stats['total_requests']}")
    print(f"   Total cost: ${stats['total_cost']:.4f}")
    print(f"   Total duration: {stats['total_duration']:.1f}s")
    
    print(f"\n✅ TTS Manager system ready!")
    print(f"💡 Add API keys to .env for real audio generation")