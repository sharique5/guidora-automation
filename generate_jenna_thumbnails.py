#!/usr/bin/env python3
"""
Generate Optimized Thumbnails for Jenna's "Finding Peace in the Daily Hustle" Story
Uses all YouTube best practices: human faces, high contrast, emotional symbols, top title placement.
"""

import sys
import json
from pathlib import Path

# Add the lib directory to the path
sys.path.append(str(Path(__file__).parent / "lib"))

from video_tools.whiteboard_thumbnail_generator import WhiteboardThumbnailGenerator, WhiteboardThumbnailConfig

def generate_jenna_thumbnails():
    """Generate optimized thumbnails for all Jenna story languages."""
    print("🎨 GENERATING OPTIMIZED THUMBNAILS FOR JENNA'S STORY")
    print("Story: 'Finding Peace in the Daily Hustle'")
    print("Using YouTube Best Practices:")
    print("  ✓ Human face with emotional expression (2-5x better CTR)")
    print("  ✓ High contrast thick outlines (mobile-friendly)")
    print("  ✓ Emotional symbols (stress → calm transformation)")
    print("  ✓ Title at TOP (YouTube UI covers bottom)")
    print("  ✓ Brand mark (Guidora recognition)")
    print("  ✓ Auto-enhanced (contrast, sharpen)")
    print("  ✓ 2 variants per language (pick best)")
    print("=" * 70)
    
    # Story files for each language
    languages = {
        'en': 'finding_peace_in_the_daily_hustle_jenna_en.json',
        'es': 'finding_peace_in_the_daily_hustle_jenna_es.json', 
        'fr': 'finding_peace_in_the_daily_hustle_jenna_fr.json',
        'ur': 'finding_peace_in_the_daily_hustle_jenna_ur.json'
    }
    
    # Configure with ALL YouTube optimizations enabled
    config = WhiteboardThumbnailConfig(
        # Visual style
        style="whiteboard_sketch",
        background_color="white",
        sketch_color="black",
        accent_color="#4a90e2",  # Calming blue for Jenna's story
        
        # YouTube optimizations (ALL ENABLED)
        include_human_face=True,      # 2-5x better CTR
        high_contrast=True,            # Mobile readability
        emotional_symbols=True,        # Transformation visual markers
        add_brand_mark=True,           # Guidora recognition
        brand_mark_position="top_left", # Unobtrusive but visible
        
        # Title settings
        use_youtube_title=True,
        title_position="top",          # CRITICAL: Avoids YouTube UI covering
        title_style="bold_modern",
        font_size_ratio=0.08,
        
        # Post-processing
        auto_enhance=True,             # Contrast + sharpen
        generate_variants=2,           # Generate 2 options, pick best
        
        # Language strategy
        language_strategy="localized", # Generate for EN and UR (ES/FR use EN)
        
        # Provider
        primary_provider="openai"
    )
    
    generator = WhiteboardThumbnailGenerator(config)
    
    results = {}
    total_cost = 0.0
    
    language_names = {'en': 'English', 'es': 'Spanish', 'fr': 'French', 'ur': 'Urdu'}
    
    for lang, filename in languages.items():
        print(f"\n{'='*70}")
        print(f"🌍 {lang.upper()} - {language_names[lang]}")
        print(f"{'='*70}")
        
        # Load story data
        story_path = Path(f"data/stories/{lang}/{filename}")
        
        if not story_path.exists():
            print(f"   ❌ Story file not found: {story_path}")
            continue
            
        try:
            with open(story_path, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
        except Exception as e:
            print(f"   ❌ Failed to load story: {e}")
            continue
        
        print(f"   📖 Title: {story_data.get('title', 'Unknown')}")
        print(f"   🎭 Theme: Stress → Mindfulness → Peace")
        print(f"   🎨 Features:")
        print(f"      • Human figure showing emotional journey")
        print(f"      • Stress symbols (chaos) → Peace symbols (calm)")
        print(f"      • Bold thick outlines for mobile")
        print(f"      • Title at TOP (avoids YouTube UI)")
        print(f"      • Guidora brand mark")
        print(f"      • Auto-enhanced contrast & sharpening")
        
        # Check if we'll actually generate or reuse
        should_generate = generator.should_create_localized_thumbnail(lang)
        
        if not should_generate and lang != 'en':
            print(f"   🔄 Will use English thumbnail (universal strategy)")
            print(f"   💰 Cost: $0.000 (reusing EN)")
            continue
        
        variants = config.generate_variants
        cost_per_variant = 0.040
        total_lang_cost = variants * cost_per_variant
        
        print(f"   💰 Cost: ${total_lang_cost:.3f} ({variants} variants × $0.040)")
        
        try:
            # Generate thumbnail with video ID format
            video_id = f"003_{lang}"  # Matching our tracking system
            thumbnail_path = generator.generate_thumbnail(story_data, lang, video_id)
            
            if thumbnail_path:
                print(f"   ✅ SUCCESS!")
                print(f"   📁 Primary: {thumbnail_path}")
                if variants > 1:
                    print(f"   📁 Review all {variants} variants and select best for upload")
                results[lang] = {
                    'path': thumbnail_path,
                    'video_id': video_id,
                    'cost': total_lang_cost,
                    'variants': variants
                }
                total_cost += total_lang_cost
            else:
                print(f"   ❌ Generation failed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n{'='*70}")
    print(f"📊 GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"✅ Successful: {len(results)}/{len(languages)} languages")
    print(f"💰 Total cost: ${total_cost:.3f}")
    print(f"📈 Expected CTR improvement: 2-5x over standard thumbnails")
    print(f"📁 Location: assets/thumbnails/{{lang}}/")
    
    if results:
        print(f"\n🎯 GENERATED THUMBNAILS:")
        for lang, info in results.items():
            print(f"\n   {lang.upper()}:")
            print(f"      Primary: {info['path']}")
            if info['variants'] > 1:
                print(f"      Variants: {info['variants']} (review and select best)")
    
    print(f"\n{'='*70}")
    print(f"NEXT STEPS:")
    print(f"1. Review generated variants (if multiple per language)")
    print(f"2. Select best thumbnail for each language")
    print(f"3. Upload videos to YouTube with selected thumbnails")
    print(f"4. A/B test if possible to measure CTR improvement")
    print(f"{'='*70}")

if __name__ == "__main__":
    generate_jenna_thumbnails()
