"""
Test script for Natural Language Translator

This script tests the translation system with Maya's story to demonstrate
natural, conversational translations with cultural adaptation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from lib.translators.natural_translator import NaturalTranslator
from pathlib import Path

def load_maya_story():
    """Load Maya's story data for testing."""
    return {
        "title": "Seeing Signs: A Journey to Inner Strength",
        "description": "Discover how everyday challenges can reveal unexpected paths to personal growth and resilience. This story showcases how recognizing subtle signs in our lives can transform our perspective and strengthen our spirit.",
        "category": "faith_recognition",
        "target_audience": "universal",
        "estimated_duration": 179,
        "themes": ["Faith", "Guidance", "Psychology"],
        "characters": ["professional"],
        "setting": "general",
        "story_content": """
Imagine you're about to miss an important interview because your car won't start.

Meet Maya, a software developer in her early thirties, living in a bustling city. She's dedicated and talented but recently has been feeling lost in the sea of daily demands and competitive pressures at work. The project deadlines are looming, her boss is increasingly demanding, and she's questioning if her job is even worth the stress anymore.

On this particularly crucial morning, when she has the final interview for a job she's been eyeing at a prestigious startup, her car fails to start. She feels the panic rise, her breath quickens, and a sense of defeat looms over her.

Maya's immediate reaction is frustration mixed with despair. Her mind races through the consequences of missing this interview. She's worked hard for this opportunity, feeling it might be her break from the current job stress. However, as she stands beside her motionless car, her mind starts replaying other recent setbacks: her broken laptop last week, her lost phone, a misunderstanding with a close friend. It feels like a pattern of chaos, clouding her vision and dampening her spirit.

As Maya waits for the tow truck, she scrolls absently through her phone and stumbles upon a video about finding strength and guidance through recognizing life's subtle signs. The message strikes a chord. She starts reflecting on her recent "misfortunes." Could these be signs pushing her to pause and reconsider her path?

With time to think as she rides the bus to her interview, Maya contemplates her relentless pursuit of career advancement at the expense of her health and happiness. She realizes these disruptions could be nudges towards a more balanced life, urging her to slow down and reassess what truly matters.

Maya walks into the interview with a newfound sense of calm and perspective. She answers questions with honesty, expressing not only her skills but also her desire for a work environment that values well-being and creativity. She feels a shift within herself—a deeper understanding of her personal and professional needs.

Maya's story reminds us to stay open to the signs life offers us, often hidden in disruptions or challenges. These moments, though initially unsettling, can guide us to greater self-awareness and resilience. Next time you face a setback, take a moment to look deeper. What could life be trying to tell you?
        """,
        "youtube_title": "How Missing My Interview Revealed My True Path",
        "youtube_description": "Discover Maya's transformative journey when a broken car leads her to uncover the hidden signs in life's challenges. Watch how a day filled with setbacks teaches her to reassess her values and goals for a more fulfilling life. Did you ever find a hidden message in your setbacks? Share your story in the comments!",
        "youtube_tags": ["wisdom", "inspiration", "personal growth", "spiritual journey", "motivation", "life lessons", "resilience", "inner strength", "Maya's story", "life transformation", "finding balance", "career vs happiness", "recognizing signs", "life advice", "success stories"],
        "thumbnail_concept": "The thumbnail features Maya, a woman in her early thirties, looking contemplative beside a broken car with a city backdrop. The color scheme is a mix of soothing blues and energetic oranges, reflecting a mood of calm amid chaos. Text overlay reads: \"The Day Everything Changed.\"",
        "target_keywords": ["personal growth", "inner strength", "resilience", "life transformation", "recognizing signs", "career stress", "spiritual journey"],
        "generation_metadata": {
            "story_tokens": 1056,
            "metadata_tokens": 1230,
            "total_cost": 0.06858,
            "model_used": "gpt-4-turbo",
            "prompt_type": "universal"
        },
        "generated_at": "2025-10-12T20:48:25.529064",
        "quality_score": 0.0
    }

def test_single_translation():
    """Test translation to a single language (Spanish)."""
    print("🚀 Testing Single Translation (Spanish)")
    print("=" * 50)
    
    # Initialize translator
    translator = NaturalTranslator()
    
    # Load Maya's story
    maya_story = load_maya_story()
    
    try:
        # Translate to Spanish
        spanish_story = translator.translate_story(maya_story, 'es')
        
        print("✅ Spanish Translation Success!")
        print(f"Original Title: {maya_story['title']}")
        print(f"Spanish Title: {spanish_story.get('title', 'N/A')}")
        print(f"Translation Cost: ${spanish_story.get('translation_metadata', {}).get('estimated_cost', 0):.4f}")
        print()
        
        # Show first part of translated story content
        translated_content = spanish_story.get('story_content', '')
        if translated_content:
            print("📝 First 200 characters of translated story:")
            print(translated_content[:200] + "...")
            print()
        
        # Save translation
        translator.save_translated_stories({'es': [spanish_story]})
        print("💾 Spanish translation saved to data/stories/es/")
        
        return True
        
    except Exception as e:
        print(f"❌ Spanish translation failed: {e}")
        return False

def test_multi_language_translation():
    """Test translation to multiple languages."""
    print("🌍 Testing Multi-Language Translation")
    print("=" * 50)
    
    # Initialize translator
    translator = NaturalTranslator()
    
    # Load Maya's story
    maya_story = load_maya_story()
    
    # Target languages
    target_languages = ['es', 'fr', 'ur']  # Start with 3 languages for testing
    
    try:
        # Batch translation
        translated_stories = translator.translate_batch([maya_story], target_languages)
        
        total_cost = 0.0
        for lang_code, stories in translated_stories.items():
            if stories:
                story = stories[0]
                lang_name = translator.supported_languages[lang_code]['name']
                cost = story.get('translation_metadata', {}).get('estimated_cost', 0)
                total_cost += cost
                
                print(f"✅ {lang_name} translation completed!")
                print(f"   Title: {story.get('title', 'N/A')}")
                print(f"   Cost: ${cost:.4f}")
                print()
        
        print(f"💰 Total translation cost: ${total_cost:.4f}")
        
        # Save all translations
        translator.save_translated_stories(translated_stories)
        print("💾 All translations saved to data/stories/")
        
        return True
        
    except Exception as e:
        print(f"❌ Multi-language translation failed: {e}")
        return False

def show_language_info():
    """Display supported languages and their cultural contexts."""
    print("🌍 Supported Languages & Cultural Context")
    print("=" * 50)
    
    translator = NaturalTranslator()
    languages = translator.get_supported_languages()
    
    for code, info in languages.items():
        print(f"🗣️  {info['name']} ({code})")
        print(f"   Region: {info['region']}")
        print(f"   Cultural Context: {info['cultural_context']}")
        print(f"   Common Phrases: {', '.join(info['common_phrases'])}")
        print()

def main():
    """Run translation tests."""
    print("🎯 Natural Language Translator Test Suite")
    print("=" * 60)
    print()
    
    # Show supported languages
    show_language_info()
    
    # Test single translation
    success_single = test_single_translation()
    print()
    
    # Test multi-language if single was successful
    if success_single:
        success_multi = test_multi_language_translation()
        print()
        
        if success_multi:
            print("🎉 All translation tests passed!")
            print("📁 Check data/stories/ for translated content")
            
            # Show directory structure
            stories_dir = Path("data/stories")
            if stories_dir.exists():
                print("\n📂 Generated file structure:")
                for lang_dir in stories_dir.iterdir():
                    if lang_dir.is_dir():
                        files = list(lang_dir.glob("*.json"))
                        print(f"   {lang_dir.name}/ ({len(files)} files)")
                        for file in files:
                            print(f"     - {file.name}")
        else:
            print("❌ Multi-language translation tests failed")
    else:
        print("❌ Single translation test failed - skipping multi-language test")

if __name__ == "__main__":
    main()