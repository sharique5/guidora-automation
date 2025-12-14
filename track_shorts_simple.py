#!/usr/bin/env python3
"""
Simplified shorts tracker - track most recent shorts
Usage: python track_shorts_simple.py
"""

import json
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent))
from config.paths import VIDEO_TRACKER_FILE, STORY_DIRS
from lib.story_utils import load_story

def extract_short_title(short_content: str) -> str:
    """Extract title from short script."""
    lines = short_content.split('\n')
    for line in lines:
        if '**SHORT TITLE**:' in line:
            return line.split('**SHORT TITLE**:')[1].strip().strip('"')
    return "Untitled Short"

# Load tracker
with open(VIDEO_TRACKER_FILE, 'r', encoding='utf-8') as f:
    tracker_data = json.load(f)

# Find all shorts
shorts_dir = STORY_DIRS['youtube_optimized'].parent / "shorts"
all_shorts = sorted(shorts_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

print("📺 TRACK RECENT SHORTS")
print("=" * 70)
print(f"Found {len(all_shorts)} total shorts\n")

# Show recent shorts and ask to track
for i, short_file in enumerate(all_shorts[:5], 1):
    short_data = load_story(short_file)
    if short_data:
        title = extract_short_title(short_data.get('short_content', ''))
        short_type = short_data.get('short_type', 'unknown')
        print(f"{i}. [{short_type.upper()}] {title}")
        print(f"   File: {short_file.name}")

choice = input(f"\nTrack which shorts? (1-{min(5, len(all_shorts))}, 'all', or 'q' to quit): ").strip().lower()

if choice == 'q':
    print("Cancelled")
    sys.exit(0)

if choice == 'all':
    shorts_to_track = all_shorts[:5]
else:
    try:
        idx = int(choice) - 1
        shorts_to_track = [all_shorts[idx]]
    except:
        print("Invalid choice")
        sys.exit(1)

# Get story number
story_num = input("Enter story number for these shorts (e.g., 006): ").strip()

# Track them
for short_file in shorts_to_track:
    short_data = load_story(short_file)
    if short_data:
        short_type = short_data.get('short_type', 'unknown')
        title = extract_short_title(short_data.get('short_content', ''))
        
        video_id = f"{story_num}_short_{short_type}"
        
        tracker_data[video_id] = {
            "video_id": video_id,
            "title": title,
            "type": "short",
            "format": "vertical_9_16",
            "parent_video": f"{story_num}_en",
            "short_type": short_type,
            "short_file": str(short_file),
            "language": "en",
            "status": "script_ready",
            "created_at": datetime.now().isoformat(),
            "estimated_duration": "30-60 seconds",
            "updated_at": datetime.now().isoformat()
        }
        
        print(f"\n✅ Tracked: {video_id}")
        print(f"   {title}")

# Save
with open(VIDEO_TRACKER_FILE, 'w', encoding='utf-8') as f:
    json.dump(tracker_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved to tracker")
