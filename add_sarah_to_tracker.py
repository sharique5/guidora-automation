#!/usr/bin/env python3
"""
Add Sarah's YouTube-optimized story to video tracker.
Story: "The Mistake That Destroys Your Peace Daily"
Languages: EN, ES, FR, HI (Hinglish)
"""

import json
from pathlib import Path
from datetime import datetime

# Load tracker
tracker_file = Path("data/video_tracker.json")
with open(tracker_file, 'r', encoding='utf-8') as f:
    tracker_data = json.load(f)

print("📺 ADDING SARAH'S STORY TO VIDEO TRACKER")
print("Story: 'The Mistake That Destroys Your Peace Daily'")
print("=" * 70)

# Story files for each language
languages = {
    'en': ('English', 'youtube_optimized/youtube_optimized_learning_1_1_b9b9bc1f_2d15ef3d.json'),
    'es': ('Spanish', 'es/the_mistake_that_destroys_your_peace_sarah_es.json'),
    'fr': ('French', 'fr/the_mistake_that_destroys_your_peace_sarah_fr.json'),
    'hi': ('Hinglish', 'hi/the_mistake_that_destroys_your_peace_sarah_hi.json')
}

for lang, (lang_name, story_path) in languages.items():
    video_id = f"004_{lang}"
    
    # Load story to get title
    story_file = Path(f"data/stories/{story_path}")
    with open(story_file, 'r', encoding='utf-8') as f:
        story = json.load(f)
    
    # Extract title from story content
    if lang == 'en':
        title = "The Mistake That Destroys Your Peace Daily"
    else:
        # Try to extract title from translated content
        content = story.get('story_content', '')
        if '**Title**:' in content:
            title_line = content.split('**Title**:')[1].split('\n')[0].strip()
            title = title_line.strip('"').strip()
        else:
            title = "The Mistake That Destroys Your Peace Daily"
    
    tracker_data[video_id] = {
        "video_id": video_id,
        "title": title,
        "language": lang,
        "source_learning_id": "learning_1_1_b9b9bc1f",
        "story_file": f"data\\stories\\{story_path}",
        "status": "script_ready",
        "created_at": datetime.now().isoformat(),
        "estimated_duration": 208,
        "updated_at": datetime.now().isoformat(),
        "optimization_features": [
            "pattern_interruption_hook",
            "curiosity_driven_title",
            "diverse_character",
            "crisis_point_tension",
            "retention_hooks"
        ]
    }
    
    print(f"\n✅ Added {video_id}:")
    print(f"   Language: {lang_name}")
    print(f"   Title: {title}")
    print(f"   Status: script_ready")

# Save tracker
with open(tracker_file, 'w', encoding='utf-8') as f:
    json.dump(tracker_data, f, indent=2, ensure_ascii=False)

print(f"\n{'='*70}")
print(f"📊 SUMMARY")
print(f"{'='*70}")
print(f"✅ Added 4 videos to tracker (004_en, 004_es, 004_fr, 004_hi)")
print(f"📁 Status: script_ready")
print(f"🎯 Optimization: YouTube best practices applied")
print(f"{'='*70}")
