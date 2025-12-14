#!/usr/bin/env python3
"""
Universal Translation Script - Works for ANY story
Translates story to Spanish, French, and Hinglish

Usage:
    python translate_story.py <story_id>
    python translate_story.py youtube_optimized_learning_1_1_b9b9bc1f_2d15ef3d
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.append(str(Path(__file__).parent / "lib"))
from llm_tools import create_default_manager

def find_story_file(story_id):
    """Find story file in any subdirectory."""
    stories_dir = Path("data/stories")
    
    # Search in all subdirectories
    for json_file in stories_dir.rglob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('id') == story_id:
                    return json_file, data
        except:
            continue
    
    return None, None

def translate_content(content, target_language, language_name):
    """Translate content to target language."""
    
    if target_language == 'hi':  # Hinglish
        prompt = f"""Translate into HINGLISH (Hindi in Roman/Latin script mixed with English).

HINGLISH RULES:
- Write Hindi words using English alphabet only
- Mix Hindi and English naturally (like Indians speak)
- Keep English words that are common (nurse, hospital, etc.)
- Use conversational tone
- NO Devanagari script - only Roman letters

Content to translate:
{content}

Translate while maintaining emotional impact and natural flow."""
    else:
        prompt = f"""Translate into {language_name}.

Content to translate:
{content}

Translate while maintaining:
- Emotional impact
- Natural flow
- Cultural appropriateness"""
    
    llm = create_default_manager()
    response = llm.generate(prompt=prompt)
    return response.content, response.cost_estimate

def main():
    if len(sys.argv) < 2:
        print("❌ Error: Please provide story ID")
        print("\nUsage:")
        print("  python translate_story.py <story_id>")
        print("\nExample:")
        print("  python translate_story.py youtube_optimized_learning_1_1_b9b9bc1f_2d15ef3d")
        sys.exit(1)
    
    story_id = sys.argv[1]
    
    print("🌍 UNIVERSAL STORY TRANSLATOR")
    print(f"Story ID: {story_id}")
    print("=" * 70)
    
    # Find the story
    print(f"\n🔍 Searching for story...")
    story_file, story_data = find_story_file(story_id)
    
    if not story_data:
        print(f"❌ Story not found: {story_id}")
        sys.exit(1)
    
    print(f"✅ Found: {story_file}")
    
    # Get story content (handle different formats)
    story_content = story_data.get('story_content') or story_data.get('content', '')
    metadata_content = story_data.get('youtube_metadata', '')
    
    # Languages
    languages = {
        'es': 'Spanish',
        'fr': 'French',
        'hi': 'Hinglish'
    }
    
    total_cost = 0.0
    
    for lang_code, lang_name in languages.items():
        print(f"\n{'='*70}")
        print(f"🌍 {lang_name.upper()}")
        print(f"{'='*70}")
        
        # Translate main content
        print(f"   ⏳ Translating story...")
        story_translated, story_cost = translate_content(story_content, lang_code, lang_name)
        print(f"   ✅ Story (${story_cost:.4f})")
        
        # Translate metadata if exists
        metadata_translated = ""
        metadata_cost = 0.0
        if metadata_content:
            print(f"   ⏳ Translating metadata...")
            metadata_translated, metadata_cost = translate_content(metadata_content, lang_code, lang_name)
            print(f"   ✅ Metadata (${metadata_cost:.4f})")
        
        lang_total = story_cost + metadata_cost
        total_cost += lang_total
        print(f"   💰 Total: ${lang_total:.4f}")
        
        # Create translated object
        translated_data = {
            **story_data,
            "story_content": story_translated if story_content else None,
            "content": story_translated if not story_content else story_data.get('content'),
            "youtube_metadata": metadata_translated if metadata_content else story_data.get('youtube_metadata'),
            "language": lang_code,
            "language_name": lang_name,
            "translation_cost": lang_total,
            "translated_at": datetime.now().isoformat()
        }
        
        # Save
        output_dir = Path(f"data/stories/{lang_code}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename from title or story_id
        title = story_data.get('title', story_id)
        safe_filename = title.lower().replace('"', '').replace("'", '').replace(' ', '_')[:60]
        filename = f"{safe_filename}_{lang_code}.json"
        
        output_file = output_dir / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, indent=2, ensure_ascii=False)
        
        print(f"   💾 {output_file}")
    
    print(f"\n{'='*70}")
    print(f"✅ Translated to {len(languages)} languages")
    print(f"💰 Total cost: ${total_cost:.4f}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
