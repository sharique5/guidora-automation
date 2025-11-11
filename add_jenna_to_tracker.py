"""
Add Jenna's translated stories to the video tracker.
"""

import json
from pathlib import Path
from datetime import datetime

# Load video tracker
tracker_file = Path("data/video_tracker.json")
with open(tracker_file, 'r', encoding='utf-8') as f:
    tracker_data = json.load(f)

# Load the translated stories
languages = ['en', 'es', 'fr', 'ur']
language_names = {'en': 'English', 'es': 'Spanish', 'fr': 'French', 'ur': 'Urdu'}

print("=" * 70)
print("ADDING JENNA'S STORY TO VIDEO TRACKER")
print("=" * 70)

# Find the next video ID number
existing_ids = [int(vid.split('_')[0]) for vid in tracker_data.keys() if vid.split('_')[0].isdigit()]
next_id = max(existing_ids) + 1 if existing_ids else 3

added_count = 0

for lang in languages:
    story_file = Path(f"data/stories/{lang}/finding_peace_in_the_daily_hustle_jenna_{lang}.json")
    
    if story_file.exists():
        with open(story_file, 'r', encoding='utf-8') as f:
            story = json.load(f)
        
        video_id = f"{next_id:03d}_{lang}"
        
        # Add to tracker
        tracker_data[video_id] = {
            "video_id": video_id,
            "title": story.get('title', 'Finding Peace in the Daily Hustle'),
            "language": lang,
            "source_learning_id": story.get('source_learning_id', 'learning_1_1_b9b9bc1f'),
            "story_file": str(story_file),
            "status": "script_ready",
            "created_at": datetime.now().isoformat(),
            "estimated_duration": story.get('estimated_duration', 208)
        }
        
        added_count += 1
        print(f"Added {video_id}: {language_names[lang]} - {story.get('title', 'Finding Peace')[:50]}")

# Save updated tracker
with open(tracker_file, 'w', encoding='utf-8') as f:
    json.dump(tracker_data, f, indent=2, ensure_ascii=False)

print(f"\n" + "=" * 70)
print(f"TRACKER UPDATE COMPLETE")
print("=" * 70)
print(f"Added {added_count} videos to tracker")
print(f"Video IDs: {next_id:03d}_en, {next_id:03d}_es, {next_id:03d}_fr, {next_id:03d}_ur")
print(f"Status: script_ready")
print(f"\nTotal videos in tracker: {len(tracker_data)}")
print("=" * 70)
