#!/usr/bin/env python3
"""
Add video files to tracker - updates existing entries with video paths
"""

import json
from pathlib import Path
from datetime import datetime

tracker_file = Path("data/video_tracker.json")

# Load tracker
with open(tracker_file, 'r', encoding='utf-8') as f:
    tracker = json.load(f)

# Video files found
videos = {
    # Main videos - English
    '004_en': {
        'video_path': 'data\\videos\\production\\en\\004_sarah_nurse_story_en.mp4',
        'file_size_mb': 15.42,
        'status': 'video_ready'
    },
    '005_en': {
        'video_path': 'data\\videos\\production\\en\\005_tom_father_story_en.mp4',
        'file_size_mb': 18.1,
        'status': 'video_ready'
    },
    '006_en': {
        'video_path': 'data\\videos\\production\\en\\006_emma_teacher_story_en.mp4',
        'file_size_mb': 16.92,
        'status': 'video_ready'
    },
    
    # Main videos - Hindi
    '004_hi': {
        'video_path': 'data\\videos\\production\\hi\\004_sarah_nurse_story_hi.mp4',
        'file_size_mb': 20.56,
        'status': 'video_ready'
    },
    '005_hi': {
        'video_path': 'data\\videos\\production\\hi\\005_tom_father_story_hi.mp4',
        'file_size_mb': 20.37,
        'status': 'video_ready'
    },
    '006_hi': {
        'video_path': 'data\\videos\\production\\hi\\006_emma_teacher_story_hi.mp4',
        'file_size_mb': 21.1,
        'status': 'video_ready'
    },
    
    # Shorts - English only
    '004_short_hook': {
        'video_path': 'data\\videos\\shorts\\en\\004_sarah_short_hook.mp4',
        'file_size_mb': 2.44,
        'status': 'video_ready'
    },
    '004_short_wisdom': {
        'video_path': 'data\\videos\\shorts\\en\\004_sarah_short_wisdom.mp4',
        'file_size_mb': 10.47,
        'status': 'video_ready'
    },
    '005_short_hook': {
        'video_path': 'data\\videos\\shorts\\en\\005_tom_short_hook.mp4',
        'file_size_mb': 5.62,
        'status': 'video_ready'
    },
    '005_short_wisdom': {
        'video_path': 'data\\videos\\shorts\\en\\005_tom_short_wisdom.mp4',
        'file_size_mb': 12.43,
        'status': 'video_ready'
    },
    '006_short_hook': {
        'video_path': 'data\\videos\\shorts\\en\\006_emma_short_hook.mp4',
        'file_size_mb': 11.23,
        'status': 'video_ready'
    },
    '006_short_wisdom': {
        'video_path': 'data\\videos\\shorts\\en\\006_emma_short_wisdom.mp4',
        'file_size_mb': 9.7,
        'status': 'video_ready'
    }
}

print("📹 ADDING VIDEOS TO TRACKER")
print("=" * 70)

updated = 0
not_found = 0

for video_id, video_info in videos.items():
    if video_id in tracker:
        # Update existing entry
        tracker[video_id]['video_path'] = video_info['video_path']
        tracker[video_id]['file_size_mb'] = video_info['file_size_mb']
        tracker[video_id]['status'] = video_info['status']
        tracker[video_id]['updated_at'] = datetime.now().isoformat()
        
        print(f"✅ {video_id}")
        print(f"   Video: {Path(video_info['video_path']).name}")
        print(f"   Size: {video_info['file_size_mb']} MB")
        updated += 1
    else:
        print(f"⚠️  {video_id} - Not found in tracker")
        not_found += 1

# Save
with open(tracker_file, 'w', encoding='utf-8') as f:
    json.dump(tracker, f, indent=2, ensure_ascii=False)

print(f"\n{'=' * 70}")
print(f"✅ TRACKER UPDATED")
print(f"📊 Updated: {updated} entries")
print(f"⚠️  Not found: {not_found} entries")
print(f"{'=' * 70}")

print(f"\n📺 VIDEO STATUS:")
print(f"  Main Videos (EN): 3 (Sarah, Tom, Emma)")
print(f"  Main Videos (HI): 3 (Sarah, Tom, Emma)")
print(f"  Shorts (EN): 6 (2 per story)")
print(f"  TOTAL: 12 videos ready")
