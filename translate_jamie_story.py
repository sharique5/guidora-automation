#!/usr/bin/env python3
"""
Custom translator for the new Jamie story
Translates "Finding Calm in the Chaos: A Simple Daily Habit" to all target languages
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath('.'))

from lib.translators.natural_translator import NaturalTranslator

def extract_jamie_story():
    """Extract the new Jamie story from stories.jsonl"""
    stories_file = Path("data/stories/stories.jsonl")
    
    with open(stories_file, 'r', encoding='utf-8') as f:
        for line in f:
            story = json.loads(line)
            if 'enhanced_story_1_1_universal' in story['id']:
                # Convert to the format expected by translator
                return {
                    "title": story['title'].strip('"'),
                    "description": "Discover a transformative daily habit that can bring peace and guidance to your busy life.",
                    "story_content": story['content'],
                    "youtube_title": "3 Minutes to Transform Stress: Jamie's Daily Habit",
                    "youtube_description": "Discover how Jamie transformed overwhelming stress into serene calm with a simple daily habit. This inspiring story highlights the power of mindful pauses to navigate life's chaos. Can three minutes really change your day? Watch to find out how you can apply this daily habit and witness the transformation in your own life.",
                    "youtube_tags": [
                        "wisdom", "inspiration", "personal growth", "spiritual", "motivation", 
                        "life lessons", "daily habits", "stress relief", "mindfulness", "peace",
                        "productivity", "mental health", "self-care", "life balance", "Jamie's story"
                    ]
                }
    
    raise ValueError("Jamie story not found in stories.jsonl")

def translate_jamie_story():
    """Translate Jamie's story to all target languages"""
    print("🎬 Translating Jamie's Story: 'Finding Calm in the Chaos'")
    print("=" * 60)
    
    # Extract story
    jamie_story = extract_jamie_story()
    print(f"📖 Story Title: {jamie_story['title']}")
    print(f"📊 Story Length: {len(jamie_story['story_content'])} characters")
    
    # Initialize translator
    translator = NaturalTranslator()
    
    # Target languages
    languages = ['en', 'es', 'fr', 'ur']
    results = {}
    total_cost = 0.0
    
    for lang in languages:
        print(f"\n🌍 Translating to {lang.upper()}...")
        
        if lang == 'en':
            # For English, just format the existing content properly
            result = {
                'title': jamie_story['title'],
                'description': jamie_story['description'],
                'script': jamie_story['story_content'],
                'youtube_title': jamie_story['youtube_title'],
                'youtube_description': jamie_story['youtube_description'],
                'youtube_tags': jamie_story['youtube_tags'],
                'translation_metadata': {
                    'target_language': 'en',
                    'language_name': 'English',
                    'translated_at': '2025-11-08T00:00:00',
                    'translation_model': 'original',
                    'cultural_adaptation': False,
                    'original_language': 'en',
                    'estimated_cost': 0.0
                }
            }
        else:
            # Translate to other languages
            try:
                result = translator.translate_story(jamie_story, lang)
                cost = result.get('translation_metadata', {}).get('estimated_cost', 0.0)
                total_cost += cost
                print(f"   ✅ Completed! Cost: ${cost:.4f}")
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                continue
        
        results[lang] = result
        
        # Extract clean script for validation
        clean_script = translator.extract_clean_script(result) if lang != 'en' else result['script']
        quality = translator.validate_script_quality(clean_script, lang) if lang != 'en' else {'word_count': 'original', 'estimated_duration': '203s'}
        
        print(f"   📝 Clean script: {len(clean_script)} chars")
        print(f"   ⏱️ Duration: {quality.get('estimated_duration', 'N/A')}")
        print(f"   📺 YouTube: {result.get('youtube_title', 'N/A')}")
    
    print(f"\n💰 Total translation cost: ${total_cost:.4f}")
    print(f"✅ Translation complete for {len(results)} languages!")
    
    return results

def save_translated_stories(results):
    """Save translated stories to appropriate directories"""
    print("\n📁 Saving translated stories...")
    
    # Create directories
    stories_dir = Path("data/stories")
    
    for lang, result in results.items():
        lang_dir = stories_dir / lang
        lang_dir.mkdir(exist_ok=True)
        
        # Create filename
        filename = f"finding_calm_in_the_chaos_a_simple_daily_habit_{lang}.json"
        filepath = lang_dir / filename
        
        # Prepare story data
        story_data = {
            "title": result.get('title', 'Finding Calm in the Chaos: A Simple Daily Habit'),
            "description": result.get('description', ''),
            "category": "spiritual_practice",
            "target_audience": "universal",
            "estimated_duration": 203,
            "themes": ["Faith", "Worship", "Guidance"],
            "characters": ["professional"],
            "setting": "modern_urban",
            "story_content": result.get('script', ''),
            "youtube_title": result.get('youtube_title', ''),
            "youtube_description": result.get('youtube_description', ''),
            "youtube_tags": result.get('youtube_tags', []),
            "thumbnail_concept": "The thumbnail features Jamie in a moment of calm reflection, with soft colors and peaceful imagery representing balance and serenity.",
            "target_keywords": ["daily habits", "stress relief", "mindfulness", "personal growth", "peace"],
            "generation_metadata": {
                "story_tokens": 1396,
                "metadata_tokens": 2323,
                "total_cost": 0.11157,
                "model_used": "gpt-4-turbo",
                "prompt_type": "universal"
            },
            "generated_at": "2025-11-05T18:51:05.815223",
            "quality_score": 0.0
        }
        
        # Add translation metadata if not English
        if lang != 'en' and 'translation_metadata' in result:
            story_data['translation_metadata'] = result['translation_metadata']
        
        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ {lang.upper()}: {filepath}")
    
    print(f"📦 Saved {len(results)} translated stories!")

def main():
    """Main translation function"""
    print("🚀 Custom Jamie Story Translation")
    print("Story: 'Finding Calm in the Chaos: A Simple Daily Habit'")
    print("Languages: EN, ES, FR, UR")
    print("=" * 60)
    
    try:
        # Translate the story
        results = translate_jamie_story()
        
        # Save translated files
        save_translated_stories(results)
        
        print(f"\n🎉 Translation Process Complete!")
        print(f"📂 Check data/stories/[lang]/ for translated files")
        print(f"🎬 Ready for video production pipeline!")
        
        # Show next steps
        print(f"\n📋 NEXT STEPS:")
        print(f"1. Register stories: python scripts/final_video_manager.py register")
        print(f"2. Check status: python scripts/final_video_manager.py status") 
        print(f"3. Get batch: python scripts/final_video_manager.py batch")
        
    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())