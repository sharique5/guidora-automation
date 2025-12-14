#!/usr/bin/env python3
"""
Universal Video Tracker Script - Works for ANY story
Adds story to video tracker for all languages

Usage:
    python add_to_tracker.py <story_number> <story_title>
    python add_to_tracker.py 004 "The Mistake That Destroys Your Peace Daily"
    
    # Auto-detect from EN file
    python add_to_tracker.py 004
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def find_story_files(story_number):
    """Find all language versions of a story."""
    stories_dir = Path("data/stories")
    files = {}
    
    # Search for files containing the story number or recent files
    for lang in ['en', 'es', 'fr', 'hi', 'ur', 'youtube_optimized']:
        lang_dir = stories_dir / lang
        if not lang_dir.exists():
            continue
        
        # Get most recent JSON file
        json_files = sorted(lang_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        if json_files:
            files[lang] = json_files[0]
    
    return files

def extract_title(file_path):
    """Extract title from story file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Try different title fields
    title = data.get('title')
    if not title:
        # Try extracting from content
        content = data.get('story_content') or data.get('content', '')
        if '**Title**:' in content:
            title = content.split('**Title**:')[1].split('\n')[0].strip().strip('"')
    
    return title or "Untitled"

def main():
    if len(sys.argv) < 2:
        print("❌ Error: Please provide story number")
        print("\nUsage:")
        print("  python add_to_tracker.py <number> [title]")
        print("\nExamples:")
        print("  python add_to_tracker.py 004")
        print("  python add_to_tracker.py 005 'Story Title'")
        sys.exit(1)
    
    story_number = sys.argv[1]
    provided_title = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("📺 UNIVERSAL VIDEO TRACKER")
    print(f"Story Number: {story_number}")
    print("=" * 70)
    
    # Load tracker
    tracker_file = Path("data/video_tracker.json")
    with open(tracker_file, 'r', encoding='utf-8') as f:
        tracker_data = json.load(f)
    
    # Find story files
    print(f"\n🔍 Searching for story files...")
    story_files = find_story_files(story_number)
    
    if not story_files:
        print(f"❌ No story files found for {story_number}")
        sys.exit(1)
    
    print(f"✅ Found {len(story_files)} language versions")
    
    # Map language codes
    lang_map = {
        'en': 'en',
        'es': 'es',
        'fr': 'fr',
        'hi': 'hi',
        'ur': 'ur',
        'youtube_optimized': 'en'
    }
    
    lang_names = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'hi': 'Hinglish',
        'ur': 'Urdu'
    }
    
    for file_lang, file_path in story_files.items():
        lang_code = lang_map.get(file_lang, file_lang)
        video_id = f"{story_number}_{lang_code}"
        
        # Get title
        title = provided_title or extract_title(file_path)
        
        # Read story for metadata
        with open(file_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
        
        tracker_data[video_id] = {
            "video_id": video_id,
            "title": title,
            "language": lang_code,
            "source_learning_id": story_data.get('source_learning_id', 'unknown'),
            "story_file": str(file_path).replace('/', '\\'),
            "status": "script_ready",
            "created_at": datetime.now().isoformat(),
            "estimated_duration": story_data.get('estimated_duration', 208),
            "updated_at": datetime.now().isoformat()
        }
        
        print(f"\n✅ {video_id}:")
        print(f"   {lang_names.get(lang_code, lang_code)}: {title[:60]}...")
    
    # Save
    with open(tracker_file, 'w', encoding='utf-8') as f:
        json.dump(tracker_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"✅ Added {len(story_files)} videos to tracker")
    print(f"📁 All set to script_ready status")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
