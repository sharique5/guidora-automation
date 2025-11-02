#!/usr/bin/env python3
"""
Enhanced Natural Language Translator Test Suite
Tests the improved translator with whiteboard-optimized script generation.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath('.'))

from lib.translators.natural_translator import NaturalTranslator

# Maya's story for testing
MAYA_STORY = {
    "title": "Seeing Signs: A Journey to Inner Strength",
    "description": "Discover how everyday challenges can reveal unexpected paths to personal growth and resilience. This story showcases how recognizing subtle signs in our lives can transform our perspective and strengthen our spirit.",
    "story_content": """Imagine you're about to miss an important interview because your car won't start.

Meet Maya, a software developer in her early thirties, living in a bustling city. She's dedicated and talented but recently has been feeling lost in the sea of daily demands and competitive pressures at work. The project deadlines are looming, her boss is increasingly demanding, and she's questioning if her job is even worth the stress anymore.

On this particularly crucial morning, when she has the final interview for a job she's been eyeing at a prestigious startup, her car fails to start. She feels the panic rise, her breath quickens, and a sense of defeat looms over her.

Maya's immediate reaction is frustration mixed with despair. Her mind races through the consequences of missing this interview. She's worked hard for this opportunity, feeling it might be her break from the current job stress. However, as she stands beside her motionless car, her mind starts replaying other recent setbacks: her broken laptop last week, her lost phone, a misunderstanding with a close friend. It feels like a pattern of chaos, clouding her vision and dampening her spirit.

As Maya waits for the tow truck, she scrolls absently through her phone and stumbles upon a video about finding strength and guidance through recognizing life's subtle signs. The message strikes a chord. She starts reflecting on her recent "misfortunes." Could these be signs pushing her to pause and reconsider her path?

With time to think as she rides the bus to her interview, Maya contemplates her relentless pursuit of career advancement at the expense of her health and happiness. She realizes these disruptions could be nudges towards a more balanced life, urging her to slow down and reassess what truly matters.

Maya walks into the interview with a newfound sense of calm and perspective. She answers questions with honesty, expressing not only her skills but also her desire for a work environment that values well-being and creativity. She feels a shift within herself—a deeper understanding of her personal and professional needs.

Maya's story reminds us to stay open to the signs life offers us, often hidden in disruptions or challenges. These moments, though initially unsettling, can guide us to greater self-awareness and resilience. Next time you face a setback, take a moment to look deeper. What could life be trying to tell you?""",
    "youtube_title": "How Missing My Interview Revealed My True Path",
    "youtube_description": "Discover Maya's transformative journey when a broken car leads her to uncover the hidden signs in life's challenges. Watch how a day filled with setbacks teaches her to reassess her values and goals for a more fulfilling life. Did you ever find a hidden message in your setbacks? Share your story in the comments!",
    "youtube_tags": [
        "wisdom", "inspiration", "personal growth", "spiritual journey", "motivation", 
        "life lessons", "resilience", "inner strength", "Maya's story", "life transformation",
        "finding balance", "career vs happiness", "recognizing signs", "life advice", "success stories"
    ]
}

def test_enhanced_translation(language: str) -> dict:
    """Test enhanced translation for a specific language."""
    print(f"\n🎬 Testing Enhanced {language.upper()} Translation")
    print("=" * 60)
    
    try:
        translator = NaturalTranslator()
        result = translator.translate_story(MAYA_STORY, language)
        
        # Extract clean script
        clean_script = translator.extract_clean_script(result)
        
        # Debug: Show what we're working with
        print(f"🔍 Debug info:")
        print(f"   - Result has 'script' key: {'script' in result}")
        print(f"   - Result has 'story_content' key: {'story_content' in result}")
        if 'script' in result:
            print(f"   - Script content type: {type(result['script'])}")
            print(f"   - Script length: {len(str(result['script']))}")
        if 'story_content' in result:
            print(f"   - Story content type: {type(result['story_content'])}")
            print(f"   - Story content length: {len(str(result['story_content']))}")
        
        # Validate script quality
        quality_metrics = translator.validate_script_quality(clean_script, language)
        
        print(f"✅ Translation completed!")
        print(f"📝 Clean script length: {len(clean_script)} characters")
        print(f"📊 Quality metrics:")
        print(f"   - Word count: {quality_metrics['word_count']}")
        print(f"   - Average sentence length: {quality_metrics['avg_sentence_length']:.1f} words")
        print(f"   - Estimated duration: {quality_metrics['estimated_duration']} seconds")
        print(f"   - Readability score: {quality_metrics['readability_score']}/10")
        print(f"   - Whiteboard ready: {'✅' if quality_metrics['whiteboard_ready'] else '❌'}")
        
        # Show first 200 characters of clean script
        print(f"\n📖 First 200 characters of clean script:")
        print(f"'{clean_script[:200]}...'")
        
        # Show title and YouTube info if available
        if 'title' in result:
            print(f"\n🎯 Translated title: {result['title']}")
        if 'youtube_title' in result:
            print(f"📺 YouTube title: {result['youtube_title']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return {}

def show_translator_improvements():
    """Show the improvements made to the translator."""
    print("🚀 Enhanced Natural Language Translator")
    print("=" * 60)
    print("🎯 NEW FEATURES:")
    print("   ✅ Whiteboard-optimized script generation")
    print("   ✅ Clean JSON output (no nested formatting)")
    print("   ✅ Short sentences (10-15 words) for visual pacing")
    print("   ✅ Script quality validation and scoring")
    print("   ✅ Cultural adaptation for visual storytelling")
    print("   ✅ Duration estimation per language")
    print("   ✅ Pronunciation-friendly word choices")
    print("\n🎬 OPTIMIZED FOR:")
    print("   • Instadoodle whiteboard explainer videos")
    print("   • Clear narration over visual drawings")
    print("   • Natural speech patterns per language")
    print("   • Cultural authenticity and regional expressions")

def test_all_languages():
    """Test enhanced translations for all supported languages."""
    print("\n🌍 Testing All Enhanced Translations")
    print("=" * 60)
    
    languages = ['es', 'fr', 'ur']  # Skip Arabic for now
    results = {}
    total_cost = 0.0
    
    for lang in languages:
        result = test_enhanced_translation(lang)
        if result:
            results[lang] = result
            cost = result.get('translation_metadata', {}).get('estimated_cost', 0.0)
            total_cost += cost
    
    print(f"\n💰 Total translation cost: ${total_cost:.4f}")
    print(f"📁 Results ready for Instadoodle video creation!")
    
    return results

def main():
    """Main test function."""
    show_translator_improvements()
    
    # Test single language first
    print("\n" + "="*60)
    print("🧪 SINGLE LANGUAGE TEST")
    test_enhanced_translation('es')
    
    # Test all languages
    print("\n" + "="*60)
    print("🧪 MULTI-LANGUAGE TEST")
    test_all_languages()
    
    print("\n🎉 Enhanced translator testing complete!")
    print("📂 Check data/stories/ for clean, whiteboard-ready scripts")

if __name__ == "__main__":
    main()