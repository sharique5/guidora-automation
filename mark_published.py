#!/usr/bin/env python3
"""
Mark video(s) as published in the video tracker.
Universal script for all stories and languages.

Usage:
    # Mark specific video
    python mark_published.py 003_en
    
    # Mark all languages for a story
    python mark_published.py 003
    
    # Mark multiple specific videos
    python mark_published.py 003_en 003_es 004_fr
    
    # Mark all videos for multiple stories
    python mark_published.py 003 004 005
"""

import sys
import json
from pathlib import Path
from datetime import datetime

def mark_published(*video_ids):
    """Mark video(s) as published."""
    if not video_ids:
        print("❌ Error: Please provide at least one video ID")
        print("\nUsage:")
        print("  python mark_published.py 003_en          # Single video")
        print("  python mark_published.py 003             # All languages for story 003")
        print("  python mark_published.py 003_en 003_es   # Multiple videos")
        return
    
    tracker_file = Path("data/video_tracker.json")
    
    if not tracker_file.exists():
        print(f"❌ Error: Tracker file not found: {tracker_file}")
        return
    
    # Load tracker data
    with open(tracker_file, 'r', encoding='utf-8') as f:
        tracker_data = json.load(f)
    
    # Expand story IDs to all languages
    all_languages = ['en', 'es', 'fr', 'ur']
    expanded_ids = []
    
    for vid in video_ids:
        if '_' in vid:
            # Already has language suffix
            expanded_ids.append(vid)
        else:
            # Story ID without language - expand to all languages
            expanded_ids.extend([f"{vid}_{lang}" for lang in all_languages])
    
    print("📺 MARKING VIDEOS AS PUBLISHED")
    print("=" * 70)
    
    updated = []
    not_found = []
    already_published = []
    
    for video_id in expanded_ids:
        if video_id not in tracker_data:
            not_found.append(video_id)
            continue
        
        video = tracker_data[video_id]
        current_status = video.get('status', 'unknown')
        
        if current_status == 'published':
            already_published.append(video_id)
            print(f"\n✓ {video_id}: Already published")
            print(f"  Title: {video.get('title', 'N/A')}")
            continue
        
        # Update to published
        video['status'] = 'published'
        video['updated_at'] = datetime.now().isoformat()
        video['actual_publish_time'] = datetime.now().isoformat()
        
        updated.append(video_id)
        print(f"\n✅ {video_id}: {current_status} → published")
        print(f"  Title: {video.get('title', 'N/A')}")
        print(f"  Language: {video.get('language', 'N/A').upper()}")
        print(f"  Published: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save updated tracker data
    if updated:
        with open(tracker_file, 'w', encoding='utf-8') as f:
            json.dump(tracker_data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Saved changes to {tracker_file}")
    
    # Summary
    print(f"\n{'=' * 70}")
    print(f"📊 SUMMARY")
    print(f"{'=' * 70}")
    print(f"✅ Updated to published: {len(updated)}")
    print(f"✓  Already published: {len(already_published)}")
    print(f"❌ Not found: {len(not_found)}")
    
    if updated:
        print(f"\n📺 Updated videos:")
        for vid in updated:
            print(f"  • {vid}")
    
    if not_found:
        print(f"\n❌ Not found in tracker:")
        for vid in not_found:
            print(f"  • {vid}")
    
    print(f"{'=' * 70}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: Please provide video ID(s)")
        print("\nUsage:")
        print("  python mark_published.py 003_en          # Single video")
        print("  python mark_published.py 003             # All languages for story 003")
        print("  python mark_published.py 003_en 003_es   # Multiple videos")
        print("  python mark_published.py 003 004         # Multiple stories (all languages)")
        sys.exit(1)
    
    mark_published(*sys.argv[1:])
