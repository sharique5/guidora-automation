#!/usr/bin/env python3
"""
Clean up Arabic entries from video tracker for Phase 1 focus
"""

import json
from pathlib import Path

def cleanup_arabic_entries():
    """Remove Arabic video entries from the tracking system."""
    tracker_file = Path("data/video_tracker.json")
    
    if not tracker_file.exists():
        print("No video tracker file found")
        return
    
    # Load current data
    with open(tracker_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find Arabic entries
    keys_to_remove = [k for k in data.keys() if '_ar' in k or k.endswith('_ar')]
    
    print(f"Found {len(keys_to_remove)} Arabic entries to remove:")
    for key in keys_to_remove:
        print(f"  - {key}")
    
    # Remove Arabic entries
    for key in keys_to_remove:
        del data[key]
    
    # Save cleaned data
    with open(tracker_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Cleaned up video tracker")
    print(f"📊 Remaining entries: {len(data)}")
    
    # Show remaining languages
    languages = set()
    for key, video_data in data.items():
        languages.add(video_data.get('language', 'unknown'))
    
    print(f"🌍 Active languages: {sorted(languages)}")

if __name__ == "__main__":
    cleanup_arabic_entries()