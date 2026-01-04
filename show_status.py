#!/usr/bin/env python3
"""
Show status overview of all videos in the tracker.
Groups by story and shows status for each language.
"""

import json
from pathlib import Path
from collections import defaultdict

def show_status():
    """Display organized status overview."""
    tracker_file = Path("data/video_tracker.json")
    
    if not tracker_file.exists():
        print(f"❌ Error: Tracker file not found: {tracker_file}")
        return
    
    with open(tracker_file, 'r', encoding='utf-8') as f:
        tracker_data = json.load(f)
    
    # Group by story number (004, 005, 006) and type
    stories = defaultdict(lambda: {'main': {}, 'shorts': []})
    
    for video_id, video in tracker_data.items():
        # Skip old entries
        if 'story_id' in video and 'seeing' in video.get('story_id', ''):
            continue
        if 'finding' in video.get('story_file', '').lower():
            continue
        
        # Extract story number
        story_num = None
        if video_id.startswith('004'):
            story_num = '004'
        elif video_id.startswith('005'):
            story_num = '005'
        elif video_id.startswith('006'):
            story_num = '006'
        
        if not story_num:
            continue
        
        video_type = video.get('type', 'main')
        
        if video_type == 'short':
            stories[story_num]['shorts'].append({
                'id': video_id,
                'title': video.get('title', 'N/A'),
                'short_type': video.get('short_type', 'N/A'),
                'status': video.get('status', 'unknown'),
                'language': video.get('language', 'N/A')
            })
        else:
            lang = video.get('language', 'unknown')
            stories[story_num]['main'][lang] = {
                'id': video_id,
                'title': video.get('title', 'N/A'),
                'status': video.get('status', 'unknown'),
                'file_size_mb': video.get('file_size_mb', 'N/A')
            }
    
    print("\n📊 VIDEO STATUS OVERVIEW")
    print("=" * 100)
    
    # Define characters
    characters = {
        '004': 'Sarah (Nurse)',
        '005': 'Tom (Father)',
        '006': 'Emma (Teacher)'
    }
    
    # Status emojis
    status_emoji = {
        'published': '✅',
        'video_ready': '📹',
        'script_ready': '📝',
        'unknown': '❓'
    }
    
    for story_num in sorted(stories.keys()):
        story_data = stories[story_num]
        character = characters.get(story_num, 'Unknown')
        
        print(f"\n{'─' * 100}")
        print(f"📺 STORY {story_num}: {character}")
        print(f"{'─' * 100}")
        
        # Main story
        print(f"\n🎬 Main Story:")
        if story_data['main']:
            title = list(story_data['main'].values())[0]['title']
            print(f"   Title: {title}")
            print(f"   Languages:")
            for lang in ['en', 'hi', 'es', 'fr', 'ur']:
                if lang in story_data['main']:
                    video = story_data['main'][lang]
                    status = video['status']
                    emoji = status_emoji.get(status, '❓')
                    size = f" ({video['file_size_mb']} MB)" if video.get('file_size_mb') != 'N/A' else ""
                    print(f"      {emoji} {lang.upper()}: {status}{size}")
                else:
                    print(f"      ⚪ {lang.upper()}: not tracked")
        else:
            print(f"   No main story videos")
        
        # Shorts
        print(f"\n📱 Shorts (English only):")
        if story_data['shorts']:
            shorts_by_type = {}
            for short in story_data['shorts']:
                short_type = short['short_type']
                if short_type not in shorts_by_type:
                    shorts_by_type[short_type] = []
                shorts_by_type[short_type].append(short)
            
            for short_type in ['hook', 'wisdom']:
                if short_type in shorts_by_type:
                    for short in shorts_by_type[short_type]:
                        status = short['status']
                        emoji = status_emoji.get(status, '❓')
                        print(f"      {emoji} {short_type.title()}: {short['title'][:50]}... ({status})")
        else:
            print(f"   No shorts")
    
    print(f"\n{'=' * 100}")
    
    # Summary counts
    total_published = sum(1 for v in tracker_data.values() 
                         if v.get('status') == 'published' and 
                         (v.get('video_id', '').startswith(('004', '005', '006'))))
    total_ready = sum(1 for v in tracker_data.values() 
                     if v.get('status') == 'video_ready' and 
                     (v.get('video_id', '').startswith(('004', '005', '006'))))
    total_script = sum(1 for v in tracker_data.values() 
                      if v.get('status') == 'script_ready' and 
                      (v.get('video_id', '').startswith(('004', '005', '006'))))
    
    print(f"\n📈 SUMMARY:")
    print(f"   ✅ Published: {total_published}")
    print(f"   📹 Video Ready: {total_ready}")
    print(f"   📝 Script Ready: {total_script}")
    print(f"   Total tracked: {total_published + total_ready + total_script}")
    print(f"\n{'=' * 100}\n")
    
    # Legend
    print("Legend:")
    print("  ✅ Published  📹 Video Ready  📝 Script Ready  ⚪ Not Tracked")
    print()

if __name__ == "__main__":
    show_status()
