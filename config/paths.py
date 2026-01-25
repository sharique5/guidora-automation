#!/usr/bin/env python3
"""
Centralized configuration for paths, languages, and models.
Single source of truth for all constants used across the codebase.
"""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
PROMPTS_DIR = BASE_DIR / "prompts"
LIB_DIR = BASE_DIR / "lib"

# Data subdirectories
STORIES_DIR = DATA_DIR / "stories"
LEARNINGS_DIR = DATA_DIR / "learnings"
VIDEOS_DIR = DATA_DIR / "videos"
TAFSIR_DIR = DATA_DIR / "tafsir"

# Story language directories
STORY_DIRS = {
    'en': STORIES_DIR / "en",
    'es': STORIES_DIR / "es",
    'fr': STORIES_DIR / "fr",
    'hi': STORIES_DIR / "hi",
    'ur': STORIES_DIR / "ur",
    'youtube_optimized': STORIES_DIR / "youtube_optimized"
}

# Files
VIDEO_TRACKER_FILE = DATA_DIR / "video_tracker.json"
LEARNINGS_FILE = LEARNINGS_DIR / "learnings.jsonl"

# Language configuration
LANGUAGES = {
    'en': {'name': 'English', 'native': 'English'},
    'es': {'name': 'Spanish', 'native': 'Español'},
    'fr': {'name': 'French', 'native': 'Français'},
    'hi': {'name': 'Hinglish', 'native': 'Hinglish', 'note': 'Hindi in Roman script'},
    'ur': {'name': 'Urdu', 'native': 'اردو'}
}

ACTIVE_LANGUAGES = ['en', 'es', 'fr', 'hi']  # Languages we're currently using
ALL_LANGUAGES = list(LANGUAGES.keys())

# Language codes for directory mapping
LANG_DIR_MAP = {
    'en': 'en',
    'es': 'es',
    'fr': 'fr',
    'hi': 'hi',
    'ur': 'ur',
    'youtube_optimized': 'en'  # YouTube optimized stories are in English
}

# LLM Model configuration
DEFAULT_MODELS = {
    'story_generation': 'gpt-4-turbo',
    'translation': 'gpt-4-turbo',
    'metadata': 'gpt-4-turbo',
    'short_script': 'gpt-4-turbo'
}

MODEL_SETTINGS = {
    'story_generation': {
        'temperature': 0.8,
        'max_tokens': 2500
    },
    'translation': {
        'temperature': 0.7,
        'max_tokens': 2500
    },
    'metadata': {
        'temperature': 0.7,
        'max_tokens': 1500
    }
}

# Cost limits (USD)
COST_LIMITS = {
    'per_request': 0.10,
    'per_story': 0.50,
    'per_translation': 0.15
}

# Prompt templates
PROMPTS = {
    'story_youtube_optimized': PROMPTS_DIR / "story_universal_youtube_v2.txt",
    'metadata_youtube_optimized': PROMPTS_DIR / "youtube_metadata_youtube_optimized.txt",
    'title_en': PROMPTS_DIR / "title_en.txt",
    'description_en': PROMPTS_DIR / "description_en.txt",
    'learning_en': PROMPTS_DIR / "learning_en.txt",
    'story_en': PROMPTS_DIR / "story_en.txt"
}

# Video settings
VIDEO_SETTINGS = {
    'default_duration': 208,  # seconds
    'aspect_ratio': '16:9',
    'fps': 30,
    'resolution': (1920, 1080)
}

# YouTube optimization features
OPTIMIZATION_FEATURES = [
    "pattern_interruption_hook",
    "curiosity_driven_title",
    "diverse_characters",
    "crisis_point_tension",
    "retention_hooks",
    "ctr_optimized_thumbnail"
]

# Status workflow
VIDEO_STATUSES = [
    'script_ready',      # Story written and translated
    'video_ready',       # Video generated
    'published',         # Published to YouTube
    'archived'           # Archived/deleted
]

def ensure_directories():
    """Create all necessary directories if they don't exist."""
    dirs_to_create = [
        DATA_DIR, STORIES_DIR, LEARNINGS_DIR, VIDEOS_DIR, TAFSIR_DIR,
        *STORY_DIRS.values()
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # Test configuration
    print("📁 Configuration Paths:")
    print(f"  Base: {BASE_DIR}")
    print(f"  Data: {DATA_DIR}")
    print(f"  Stories: {STORIES_DIR}")
    print(f"\n🌍 Languages: {', '.join(ACTIVE_LANGUAGES)}")
    print(f"\n🤖 Models: {DEFAULT_MODELS['story_generation']}")
    print(f"\n✅ All paths valid")
