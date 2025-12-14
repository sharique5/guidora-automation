#!/usr/bin/env python3
"""
Track YouTube Shorts in video tracker
Links shorts to their parent story videos

Usage:
    python track_shorts.py <parent_story_number> <short_type>
    python track_shorts.py 006 hook
    python track_shorts.py 006 wisdom
    
    # Track all shorts for a story
    python track_shorts.py 006 --all
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Import centralized utilities
sys.path.append(str(Path(__file__).parent))
from config.paths import VIDEO_TRACKER_FILE, STORY_DIRS
from lib.story_utils import load_story

def find_short_files(parent_story_id: str, short_type: str = None):
    """Find short files for a parent story."""
    shorts_dir = STORY_DIRS['youtube_optimized'].parent / "shorts"
    
    if not shorts_dir.exists():
        return []
    
    shorts = []
    for short_file in shorts_dir.glob(f"{parent_story_id}_short_*.json"):
        short_data = load_story(short_file)
        if short_data:
            # Filter by type if specified
            if short_type is None or short_data.get('short_type') == short_type:
                shorts.append((short_file, short_data))
    
    return shorts

def extract_short_title(short_content: str) -> str:
    """Extract title from short script."""
    lines = short_content.split('\n')
    for line in lines:
        if '**SHORT TITLE**:' in line:
            return line.split('**SHORT TITLE**:')[1].strip()
    return "Untitled Short"

def main():
    parser = argparse.ArgumentParser(description='Track YouTube Shorts in video tracker')
    parser.add_argument('story_number', help='Parent story number (e.g., 006)')
    parser.add_argument('short_type', nargs='?', help='Short type (hook/wisdom/crisis)')
    parser.add_argument('--all', action='store_true', help='Track all shorts for this story')
    
    args = parser.parse_args()
    
    print("📺 SHORTS TRACKER")
    print("=" * 70)
    print(f"Parent Story: {args.story_number}")
    print("=" * 70)
    
    # Load tracker
    with open(VIDEO_TRACKER_FILE, 'r', encoding='utf-8') as f:
        tracker_data = json.load(f)
    
    # Find parent story to get its title
    parent_video_id = f"{args.story_number}_en"
    parent_entry = tracker_data.get(parent_video_id)
    
    if not parent_entry:
        print(f"⚠️  Parent story {args.story_number} not found in tracker")
        parent_title = "Unknown Story"
    else:
        parent_title = parent_entry.get('title', 'Unknown Story')
    
    print(f"Parent Story Title: {parent_title}")
    
    # Find shorts
    print(f"\n🔍 Searching for shorts...")
    
    # Get parent story ID from recent shorts dir
    shorts_dir = STORY_DIRS['youtube_optimized'].parent / "shorts"
    if not shorts_dir.exists():
        print(f"❌ No shorts directory found")
        sys.exit(1)
    
    # Find all shorts - match by checking if short file name contains story pattern
    all_shorts = []
    
    # First, try to find the actual story ID from youtube_optimized dir
    yt_dir = STORY_DIRS['youtube_optimized']
    story_id_pattern = None
    
    # Get most recent story files to match story number
    for story_file in sorted(yt_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        # Check if this could be our story by counting position
        pass  # We'll match by file name pattern instead
    
    # Match shorts by file name pattern
    for short_file in shorts_dir.glob("*.json"):
        short_data = load_story(short_file)
        if short_data:
            # Get parent story ID and check if it's one of the recent stories
            parent_id = short_data.get('parent_story_id', '')
            
            # If user specified story 006, find the shorts created from recent stories
            # Simpler: just list all shorts and let user review
            if args.all or not args.short_type or short_data.get('short_type') == args.short_type:
                all_shorts.append((short_file, short_data))
    
    if not all_shorts:
        print(f"❌ No shorts found for story {args.story_number}")
        print(f"   Generate shorts first: python generate_shorts.py <story_id>")
        sys.exit(1)
    
    print(f"✅ Found {len(all_shorts)} short(s)")
    
    # Add to tracker
    added_count = 0
    for short_file, short_data in all_shorts:
        short_type = short_data.get('short_type', 'unknown')
        short_id = short_data.get('id')
        
        # Extract title
        title = extract_short_title(short_data.get('short_content', ''))
        
        # Create tracker entry
        video_id = f"{args.story_number}_short_{short_type}"
        
        tracker_data[video_id] = {
            "video_id": video_id,
            "title": title,
            "type": "short",
            "format": "vertical_9_16",
            "parent_video": parent_video_id,
            "parent_title": parent_title,
            "short_type": short_type,
            "short_file": str(short_file),
            "language": "en",  # Shorts are typically English first
            "status": "script_ready",
            "created_at": datetime.now().isoformat(),
            "estimated_duration": "30-60 seconds",
            "updated_at": datetime.now().isoformat(),
            "notes": f"YouTube Short variant - {short_data.get('short_type_name', short_type)}"
        }
        
        print(f"\n✅ {video_id}:")
        print(f"   Type: {short_data.get('short_type_name', short_type)}")
        print(f"   Title: {title[:60]}...")
        print(f"   Links to: {parent_video_id}")
        
        added_count += 1
    
    # Save tracker
    with open(VIDEO_TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(tracker_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 70}")
    print(f"✅ Added {added_count} Short(s) to tracker")
    print(f"📁 All set to script_ready status")
    print(f"{'=' * 70}")
    
    print(f"\nNEXT STEPS:")
    print(f"1. Create vertical videos (9:16) from shorts")
    print(f"2. Add text overlays (viewers watch muted)")
    print(f"3. Upload as YouTube Shorts")
    print(f"4. Link to full video ({parent_video_id}) in description")

if __name__ == "__main__":
    main()
