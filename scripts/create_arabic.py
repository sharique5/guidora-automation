#!/usr/bin/env python3
"""
Generate Arabic translation and save it
"""
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lib.translators.natural_translator import NaturalTranslator

def create_arabic_translation():
    # Load English story
    english_story_path = "data/stories/en/seeing_signs_a_journey_to_inner_strength_en.json"
    with open(english_story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)
    
    # Translate to Arabic
    translator = NaturalTranslator()
    arabic_result = translator.translate_story(story_data, 'ar')
    
    # Save Arabic translation
    arabic_story_path = "data/stories/ar/seeing_signs_a_journey_to_inner_strength_ar.json"
    with open(arabic_story_path, 'w', encoding='utf-8') as f:
        json.dump(arabic_result, f, ensure_ascii=False, indent=2)
    
    print("✅ Arabic translation saved!")
    print(f"📝 Title: {arabic_result.get('title', 'N/A')}")
    print(f"💰 Cost: ${arabic_result['translation_metadata']['estimated_cost']:.4f}")
    print(f"⏱️ Duration: {arabic_result.get('estimated_duration', 'N/A')} seconds")
    
    # Extract and save clean script
    clean_script = translator.extract_clean_script(arabic_result)
    script_path = "data/stories/ar/ARABIC_INSTADOODLE_SCRIPT.txt"
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write("# ARABIC SCRIPT - Maya's Story\n")
        f.write("# علامات الطريق: رحلة نحو القوة الداخلية\n")
        f.write("# Duration: ~179 seconds | Quality: Optimized for Instadoodle\n\n")
        f.write(clean_script)
    
    print(f"📄 Clean script saved: {script_path}")
    
    return True

if __name__ == "__main__":
    create_arabic_translation()