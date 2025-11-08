#!/usr/bin/env python3
"""
Generate Thumbnails for Jamie's "Finding Calm in the Chaos" Story
Creates professional thumbnails for all 4 language versions.
"""

import sys
import json
from pathlib import Path

# Add the lib directory to the path
sys.path.append(str(Path(__file__).parent / "lib"))

from video_tools.whiteboard_thumbnail_generator import WhiteboardThumbnailGenerator, WhiteboardThumbnailConfig

def generate_jamie_thumbnails():
    """Generate thumbnails for all Jamie story languages."""
    print("🎨 GENERATING THUMBNAILS FOR JAMIE'S STORY")
    print("Story: 'Finding Calm in the Chaos: A Simple Daily Habit'")
    print("=" * 70)
    
    # Story files for each language
    languages = {
        'en': 'finding_calm_in_the_chaos_a_simple_daily_habit_en.json',
        'es': 'finding_calm_in_the_chaos_a_simple_daily_habit_es.json', 
        'fr': 'finding_calm_in_the_chaos_a_simple_daily_habit_fr.json',
        'ur': 'finding_calm_in_the_chaos_a_simple_daily_habit_ur.json'
    }
    
    # Configure for calm, professional theme matching Jamie's story
    config = WhiteboardThumbnailConfig(
        style="whiteboard_sketch",
        background_color="white",
        sketch_color="black",
        accent_color="#4a90e2",  # Calming blue
        use_youtube_title=True,
        title_position="bottom",
        title_style="bold_modern",
        language_strategy="localized",
        primary_provider="openai"
    )
    
    generator = WhiteboardThumbnailGenerator(config)
    
    results = {}
    total_cost = 0.0
    
    for lang, filename in languages.items():
        print(f"\n🌍 Generating {lang.upper()} thumbnail...")
        
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
        
        # Customize thumbnail concept for Jamie's calm theme
        story_data['thumbnail_concept'] = get_jamie_thumbnail_concept(lang)
        
        print(f"   📖 Title: {story_data.get('title', 'Unknown')}")
        print(f"   🎨 Theme: Professional calm & mindfulness")
        print(f"   💰 Cost: $0.040 (DALL-E 3)")
        
        try:
            # Generate thumbnail with video ID format
            video_id = f"001_{lang}"  # Matching our tracking system
            thumbnail_path = generator.generate_thumbnail(story_data, lang, video_id)
            
            if thumbnail_path:
                print(f"   ✅ SUCCESS! Generated: {thumbnail_path}")
                results[lang] = {
                    'path': thumbnail_path,
                    'video_id': video_id,
                    'cost': 0.040
                }
                total_cost += 0.040
            else:
                print(f"   ❌ Generation failed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Summary
    print(f"\n📊 GENERATION COMPLETE")
    print(f"   ✅ Successful: {len(results)}/{len(languages)} thumbnails")
    print(f"   💰 Total cost: ${total_cost:.3f}")
    print(f"   📁 Location: data/thumbnails/")
    
    if results:
        print(f"\n🎯 GENERATED THUMBNAILS:")
        for lang, info in results.items():
            print(f"   {lang.upper()}: {info['path']}")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Review thumbnails in data/thumbnails/")
        print(f"   2. Use for YouTube uploads")
        print(f"   3. Update video tracking with thumbnail paths")
        
        # Show tracking update commands
        print(f"\n📋 TRACKING UPDATES:")
        for lang, info in results.items():
            print(f"   python scripts/final_video_manager.py update-status {info['video_id']} video_ready --thumbnail-path {info['path']}")
    
    return results

def get_jamie_thumbnail_concept(language):
    """Get customized thumbnail concept for Jamie's story by language."""
    
    base_concept = """Professional software developer Jamie in a modern office setting, surrounded by a subtle aura of calm amidst technology. The scene shows a split visual: one side with chaotic elements (multiple screens, notifications, stress lines) transitioning to the other side showing the same person in a peaceful moment of reflection with soft, calming colors. The background features gentle blues and greens with subtle whiteboard-style drawings of breathing patterns, peaceful waves, and mindfulness symbols. Text overlay emphasizes the transformation theme."""
    
    language_specific = {
        'en': 'Text overlay: "3 Minutes to Transform Stress" in clean, modern font',
        'es': 'Text overlay: "3 Minutos para Transformar el Estrés" in clean, modern font', 
        'fr': 'Text overlay: "3 Minutes pour Transformer le Stress" in clean, modern font',
        'ur': 'Text overlay: "3 منٹ میں تناؤ کو سکون میں" in clean, readable Urdu font'
    }
    
    return f"{base_concept}. {language_specific.get(language, language_specific['en'])}"

def main():
    """Main thumbnail generation function."""
    print("🚀 Jamie's Story Thumbnail Generator")
    print("Theme: Finding Calm in Professional Chaos")
    print("Languages: EN, ES, FR, UR")
    print("=" * 70)
    
    try:
        results = generate_jamie_thumbnails()
        
        if results:
            print(f"\n🎉 SUCCESS! Jamie's thumbnails ready for production!")
            print(f"📈 Your thumbnail generation system is working perfectly!")
        else:
            print(f"\n⚠️ No thumbnails generated. Check API key and connection.")
            
    except Exception as e:
        print(f"\n❌ Script failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())