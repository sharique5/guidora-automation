#!/usr/bin/env python3
"""
Final test for Urdu enhanced translation
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.abspath('.'))

from lib.translators.natural_translator import NaturalTranslator

# Simple test story
SIMPLE_STORY = {
    "title": "Seeing Signs: A Journey to Inner Strength",
    "description": "A story about finding strength in challenges",
    "story_content": "Imagine you're about to miss an important interview because your car won't start. This is Maya's story of discovering inner strength through unexpected setbacks."
}

def test_urdu_enhanced():
    """Test enhanced Urdu translation."""
    print("🎬 Enhanced Urdu Translation Test")
    print("=" * 50)
    
    try:
        translator = NaturalTranslator()
        result = translator.translate_story(SIMPLE_STORY, 'ur')
        
        print(f"✅ Translation completed!")
        print(f"📝 Result keys: {list(result.keys())}")
        
        # Get the clean script (new format uses 'script' field)
        clean_script = result.get('script', '')
        
        print(f"📝 Clean script length: {len(clean_script)} characters")
        print(f"📖 First 300 chars of clean script:")
        print(f"'{clean_script[:300]}...'")
        
        # Test quality metrics
        quality_metrics = translator.validate_script_quality(clean_script, 'ur')
        print(f"\n📊 Quality metrics:")
        print(f"   - Word count: {quality_metrics['word_count']}")
        print(f"   - Average sentence length: {quality_metrics['avg_sentence_length']:.1f} words")
        print(f"   - Whiteboard ready: {'✅' if quality_metrics['whiteboard_ready'] else '❌'}")
        
        # Show cultural adaptations
        if 'cultural_adaptations' in result:
            print(f"\n🌍 Cultural adaptations: {result['cultural_adaptations']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_urdu_enhanced()