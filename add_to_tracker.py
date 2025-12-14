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

# Import centralized utilities
sys.path.append(str(Path(__file__).parent))
from config.paths import VIDEO_TRACKER_FILE, LANGUAGES, ACTIVE_LANGUAGES, LANG_DIR_MAP
from lib.story_utils import find_story_files, extract_title, load_story

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
    with open(VIDEO_TRACKER_FILE, 'r', encoding='utf-8') as f:
        tracker_data = json.load(f)
    
    # Find story files
    print(f"\n🔍 Searching for story files...")
    story_files = find_story_files(story_number)
    
    if not story_files:
        print(f"❌ No story files found for {story_number}")
        sys.exit(1)
    
    print(f"✅ Found {len(story_files)} language versions")
    
    for file_lang, file_path in story_files.items():
        lang_code = LANG_DIR_MAP.get(file_lang, file_lang)
        video_id = f"{story_number}_{lang_code}"
        
        # Get title
        title = provided_title or extract_title(file_path)
        
        # Read story for metadata
        story_data = load_story(file_path)
        
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
        lang_name = LANGUAGES.get(lang_code, {}).get('name', lang_code)
        print(f"   {lang_name}: {title[:60]}...")
    
    # Save
    with open(VIDEO_TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(tracker_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"✅ Added {len(story_files)} videos to tracker")
    print(f"📁 All set to script_ready status")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
