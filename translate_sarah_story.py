#!/usr/bin/env python3
"""
Translate Sarah's YouTube-optimized story into multiple languages.
Story ID: youtube_optimized_learning_1_1_b9b9bc1f_2d15ef3d
Languages: Spanish, French, Hinglish (Hindi in Roman script)
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.append(str(Path(__file__).parent / "lib"))
from llm_tools import create_default_manager

def load_sarah_story():
    """Load Sarah's YouTube-optimized story."""
    story_file = Path("data/stories/youtube_optimized/youtube_optimized_learning_1_1_b9b9bc1f_2d15ef3d.json")
    
    with open(story_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def translate_story(story_content, target_language, language_name):
    """Translate story content to target language."""
    
    if target_language == 'hi':  # Hinglish
        translation_prompt = f"""Translate this YouTube story into HINGLISH (Hindi written in Roman/Latin script mixed with English).

HINGLISH RULES:
- Write Hindi words using English alphabet (Roman script)
- Mix Hindi and English naturally (like Indian millennials speak)
- Keep English words that are commonly used in India (nurse, hospital, shift, etc.)
- Use conversational Hinglish tone
- NO Devanagari script - only Roman letters
- Examples: "yaar", "achha", "kya baat hai", "bahut", "ekdum"

Original Story:
{story_content}

Translate while maintaining:
- YouTube optimization (curiosity-driven title, pattern interruption hook)
- Emotional impact
- Natural Hinglish flow
- Keep names as they are (Sarah)

Provide the complete translated story in the same format."""
    else:
        translation_prompt = f"""Translate this YouTube-optimized story into {language_name}.

Original Story:
{story_content}

Translate while maintaining:
- YouTube optimization (curiosity-driven title, pattern interruption hook)
- Emotional impact and urgency
- Natural flow in {language_name}
- Cultural appropriateness
- Keep names as they are (Sarah)

Provide the complete translated story in the same format."""
    
    llm = create_default_manager()
    response = llm.generate(prompt=translation_prompt)
    
    return response.content, response.cost_estimate

def translate_metadata(metadata_content, target_language, language_name):
    """Translate YouTube metadata to target language."""
    
    if target_language == 'hi':  # Hinglish
        translation_prompt = f"""Translate this YouTube metadata into HINGLISH (Hindi in Roman script mixed with English).

HINGLISH RULES:
- Write Hindi in Roman/English letters only
- Mix Hindi and English naturally
- Keep technical terms in English (burnout, stress, nurse, etc.)
- Use conversational tone
- NO Devanagari script

Original Metadata:
{metadata_content}

Translate while keeping:
- SEO keywords effective
- Call-to-action clear
- Natural Hinglish flow

Provide the complete translated metadata."""
    else:
        translation_prompt = f"""Translate this YouTube metadata into {language_name}.

Original Metadata:
{metadata_content}

Translate while maintaining:
- SEO effectiveness
- Call-to-action clarity
- Cultural appropriateness
- Search keywords relevance

Provide the complete translated metadata."""
    
    llm = create_default_manager()
    response = llm.generate(prompt=translation_prompt)
    
    return response.content, response.cost_estimate

def main():
    """Translate Sarah's story to multiple languages."""
    
    print("🌍 TRANSLATING SARAH'S YOUTUBE-OPTIMIZED STORY")
    print("Story: 'The Mistake That Destroys Your Peace Daily'")
    print("=" * 70)
    
    # Load original story
    original_story = load_sarah_story()
    
    # Languages to translate
    languages = {
        'es': 'Spanish',
        'fr': 'French',
        'hi': 'Hinglish (Hindi in Roman script)'
    }
    
    total_cost = 0.0
    translations = {}
    
    for lang_code, lang_name in languages.items():
        print(f"\n{'='*70}")
        print(f"🌍 Translating to {lang_name.upper()}")
        print(f"{'='*70}")
        
        # Translate story content
        print(f"   ⏳ Translating story content...")
        story_translated, story_cost = translate_story(
            original_story['story_content'],
            lang_code,
            lang_name
        )
        print(f"   ✅ Story translated (${story_cost:.4f})")
        
        # Translate metadata
        print(f"   ⏳ Translating YouTube metadata...")
        metadata_translated, metadata_cost = translate_metadata(
            original_story['youtube_metadata'],
            lang_code,
            lang_name
        )
        print(f"   ✅ Metadata translated (${metadata_cost:.4f})")
        
        lang_total = story_cost + metadata_cost
        total_cost += lang_total
        
        print(f"   💰 {lang_name} total: ${lang_total:.4f}")
        
        # Create translated story object
        translated_story = {
            "id": original_story['id'],
            "source_learning_id": original_story['source_learning_id'],
            "story_content": story_translated,
            "youtube_metadata": metadata_translated,
            "language": lang_code,
            "language_name": lang_name,
            "generation_metadata": {
                **original_story['generation_metadata'],
                "translation_cost": lang_total,
                "translated_at": datetime.now().isoformat()
            },
            "generated_at": original_story['generated_at']
        }
        
        # Save to file
        output_dir = Path(f"data/stories/{lang_code}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"the_mistake_that_destroys_your_peace_sarah_{lang_code}.json"
        output_file = output_dir / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(translated_story, f, indent=2, ensure_ascii=False)
        
        print(f"   💾 Saved to: {output_file}")
        
        translations[lang_code] = {
            'file': str(output_file),
            'cost': lang_total
        }
    
    # Summary
    print(f"\n{'='*70}")
    print(f"📊 TRANSLATION COMPLETE")
    print(f"{'='*70}")
    print(f"✅ Languages translated: {len(languages)}")
    print(f"💰 Total cost: ${total_cost:.4f}")
    print(f"\n📁 Translated files:")
    for lang_code, info in translations.items():
        print(f"   {languages[lang_code]}: {info['file']}")
    
    print(f"\n{'='*70}")
    print(f"NEXT STEPS:")
    print(f"1. Add to video tracker (004_en, 004_es, 004_fr, 004_hi)")
    print(f"2. Generate YouTube-optimized thumbnails")
    print(f"3. Create whiteboard animation videos")
    print(f"4. Upload to YouTube")
    print(f"5. Track performance (CTR, retention, engagement)")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
