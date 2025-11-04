#!/usr/bin/env python3
"""
Copy English thumbnail to other language directories for universal strategy
"""

import os
import shutil

def setup_universal_thumbnails():
    """Copy the English thumbnail to all language directories"""
    
    print("🔄 Setting up universal thumbnail strategy")
    print("=" * 50)
    
    # Source thumbnail (English)
    source_file = r"C:\Users\msharique\Code\Guidora\guidora-automation\assets\thumbnails\en\story_001_en_thumbnail.png"
    
    if not os.path.exists(source_file):
        print(f"❌ Source thumbnail not found: {source_file}")
        return
    
    # Target languages and their directories
    languages = ['es', 'fr', 'ur']
    base_dir = r"C:\Users\msharique\Code\Guidora\guidora-automation\assets\thumbnails"
    
    for lang in languages:
        # Create directory if it doesn't exist
        lang_dir = os.path.join(base_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        # Copy thumbnail with appropriate naming
        target_file = os.path.join(lang_dir, f"story_001_{lang}_thumbnail.png")
        
        try:
            shutil.copy2(source_file, target_file)
            print(f"✅ {lang.upper()}: Copied to {target_file}")
        except Exception as e:
            print(f"❌ {lang.upper()}: Failed to copy - {e}")
    
    print(f"\n🎯 Universal Strategy Complete!")
    print(f"📊 All 4 languages now have thumbnails:")
    
    # Verify all files exist
    for lang in ['en', 'es', 'fr', 'ur']:
        thumbnail_path = os.path.join(base_dir, lang, f"story_001_{lang}_thumbnail.png")
        if os.path.exists(thumbnail_path):
            print(f"  ✅ {lang.upper()}: {thumbnail_path}")
        else:
            print(f"  ❌ {lang.upper()}: Missing thumbnail")
    
    print(f"\n💰 Cost Summary:")
    print(f"  Generated: 1 thumbnail ($0.040)")
    print(f"  Copied: 3 thumbnails ($0.000)")
    print(f"  Total Cost: $0.040 (75% savings!)")

if __name__ == "__main__":
    setup_universal_thumbnails()