#!/usr/bin/env python3
"""
Quick test for Urdu translation fix
"""

import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath('.'))

from lib.translators.natural_translator import NaturalTranslator

# Simple test story
SIMPLE_STORY = {
    "title": "Test Story",
    "story_content": "This is a simple test story to check if our Urdu translation works properly."
}

def test_urdu_fix():
    """Test Urdu translation with the fix."""
    print("🧪 Testing Urdu Translation Fix")
    print("=" * 50)
    
    try:
        translator = NaturalTranslator()
        result = translator.translate_story(SIMPLE_STORY, 'ur')
        
        print(f"📝 Raw translation result keys: {list(result.keys())}")
        print(f"📝 Story content type: {type(result.get('story_content'))}")
        
        # Show first 200 chars of raw story content
        raw_content = result.get('story_content', '')
        print(f"📖 First 200 chars of raw content:\n'{str(raw_content)[:200]}...'")
        
        # Test clean script extraction
        clean_script = translator.extract_clean_script(result)
        print(f"\n✨ Clean script length: {len(clean_script)} characters")
        print(f"📖 First 200 chars of clean script:\n'{clean_script[:200]}...'")
        
        # Test quality metrics
        quality_metrics = translator.validate_script_quality(clean_script, 'ur')
        print(f"\n📊 Quality metrics:")
        print(f"   - Word count: {quality_metrics['word_count']}")
        print(f"   - Whiteboard ready: {'✅' if quality_metrics['whiteboard_ready'] else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_urdu_fix()