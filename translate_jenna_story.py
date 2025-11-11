"""
Translate Jenna's "Finding Peace in the Daily Hustle" story into multiple languages.
Story ID: enhanced_story_1_1_universal_9f285839
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.llm_tools import create_default_manager

def load_jenna_story():
    """Load Jenna's story from the stories JSONL file."""
    stories_file = Path("data/stories/stories.jsonl")
    
    with open(stories_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                story = json.loads(line)
                if story['id'] == 'enhanced_story_1_1_universal_9f285839':
                    return story
    
    raise ValueError("Jenna's story not found in stories.jsonl")

def translate_story(story: dict, target_language: str, language_name: str) -> dict:
    """Translate a story to the target language using natural language translation."""
    
    print(f"\n{'='*60}")
    print(f"Translating to {language_name} ({target_language})")
    print(f"{'='*60}")
    
    llm_manager = create_default_manager()
    
    # Create natural translation prompt
    translation_prompt = f"""You are a professional translator specializing in inspirational and spiritual content for YouTube videos.

Translate the following story content into {language_name}. Maintain the emotional impact, cultural sensitivity, and engagement of the original while adapting idioms and expressions naturally.

IMPORTANT GUIDELINES:
1. Keep the structure intact (TITLE, DESCRIPTION, STORY CONTENT, sections)
2. Preserve all section markers (HOOK, CHARACTER & SCENARIO, etc.)
3. Adapt names naturally if common in that culture, or keep them universal
4. Ensure the message remains authentic and culturally appropriate
5. Keep the engagement outro and branding message translated naturally
6. Maintain the professional, inspirational tone

ORIGINAL STORY TO TRANSLATE:

{story['content']}

---

YOUTUBE METADATA TO TRANSLATE:

Title: {story['title']}
YouTube Title: Finding Peace in the Daily Hustle - A Simple Daily Practice
YouTube Description: Discover how Jenna, a busy project manager and mother, transformed her overwhelming stress into peace and clarity through simple mindful moments. This inspiring story shows the power of brief mental breaks to navigate life's chaos. Can a few moments of reflection really change your day? Watch to discover how you can apply this practice and witness the transformation in your own life.

---

Please provide the complete translation in {language_name}, maintaining all structure and formatting."""

    print(f"   Sending translation request to LLM...")
    response = llm_manager.generate(translation_prompt)
    
    print(f"   ✅ Translation completed")
    print(f"   Tokens used: {response.tokens_used}")
    print(f"   Cost: ${response.cost_estimate:.6f}")
    
    # Parse the translated content
    translated_content = response.content
    
    # Create translated story object
    translated_story = story.copy()
    translated_story['content'] = translated_content
    
    # Extract translated title and description from the response
    # Try to find translated metadata in the response
    lines = translated_content.split('\n')
    for i, line in enumerate(lines):
        if 'TITLE:' in line or 'TÍTULO:' in line or 'TITRE:' in line or 'عنوان:' in line:
            if i + 1 < len(lines):
                translated_story['title'] = lines[i+1].strip().strip('"')
                break
    
    # Set metadata
    translated_story['youtube_title'] = f"Finding Peace in the Daily Hustle - {language_name}"
    translated_story['youtube_description'] = "Translated version of Jenna's inspiring story about finding peace through mindful moments."
    
    # Add translation metadata
    translated_story['translation_metadata'] = {
        'target_language': target_language,
        'language_name': language_name,
        'translated_at': datetime.now().isoformat(),
        'translation_model': response.model,
        'cultural_adaptation': True,
        'original_language': 'en',
        'estimated_cost': response.cost_estimate
    }
    
    return translated_story

def save_translated_story(story: dict, language_code: str):
    """Save translated story to language-specific directory."""
    output_dir = Path(f"data/stories/{language_code}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename
    filename = "finding_peace_in_the_daily_hustle_jenna"
    filename = f"{filename}_{language_code}.json"
    
    output_path = output_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(story, f, indent=2, ensure_ascii=False)
    
    print(f"   💾 Saved to: {output_path}")
    return output_path

def main():
    print("="*60)
    print("JENNA'S STORY TRANSLATION")
    print("Story: Finding Peace in the Daily Hustle")
    print("="*60)
    
    # Load original story
    print("\n📖 Loading original story...")
    original_story = load_jenna_story()
    print(f"✅ Loaded: {original_story['title']}")
    print(f"   Duration: {original_story['estimated_duration']}s")
    print(f"   Category: {original_story['category']}")
    
    # Define target languages
    languages = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('ur', 'Urdu')
    ]
    
    print(f"\n🌍 Translating to {len(languages)} languages...")
    
    total_cost = 0
    translated_files = []
    
    for lang_code, lang_name in languages:
        if lang_code == 'en':
            # Save English original with proper structure
            print(f"\n{'='*60}")
            print(f"Saving English original")
            print(f"{'='*60}")
            output_path = save_translated_story(original_story, lang_code)
            translated_files.append((lang_code, lang_name, output_path))
            print(f"   ✅ English original saved")
        else:
            # Translate to other languages
            try:
                translated_story = translate_story(original_story, lang_code, lang_name)
                output_path = save_translated_story(translated_story, lang_code)
                translated_files.append((lang_code, lang_name, output_path))
                
                cost = translated_story['translation_metadata']['estimated_cost']
                total_cost += cost
                
            except Exception as e:
                print(f"   ❌ Error translating to {lang_name}: {e}")
                continue
    
    # Summary
    print(f"\n{'='*60}")
    print("TRANSLATION COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Translated to {len(translated_files)} languages:")
    for lang_code, lang_name, path in translated_files:
        print(f"   • {lang_name} ({lang_code}): {path}")
    
    print(f"\n💰 Total translation cost: ${total_cost:.4f}")
    
    print(f"\n{'='*60}")
    print("NEXT STEPS:")
    print("1. Review translated stories in data/stories/{lang}/ directories")
    print("2. Generate videos for each language version")
    print("3. Create thumbnails for each language")
    print("4. Upload to YouTube")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
