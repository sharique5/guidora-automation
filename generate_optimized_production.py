#!/usr/bin/env python3
"""
Generate optimized thumbnails for production videos
Addressing user feedback: Secular + Professional + Engaging Text
"""

import sys
import os
sys.path.append('lib')
sys.path.append('lib/video_tools')

from optimized_thumbnail_generator import OptimizedThumbnailGenerator
import shutil

def generate_optimized_production_thumbnails():
    """Generate optimized thumbnails for all production videos"""
    
    print("🎯 GENERATING OPTIMIZED PRODUCTION THUMBNAILS")
    print("Addressing: Secular tone + Engaging CTR text")
    print("=" * 60)
    
    # Production video data with engaging titles
    production_videos = [
        {
            'filename': 'seeing_signs_a_journey_to_inner_strength_en.mp4',
            'language': 'en',
            'story_data': {
                'story_number': 1,
                'title': 'Seeing Signs: A Journey to Inner Strength',
                'youtube_title': 'The Hidden Signs That Changed Everything',
                'youtube_description': 'How I discovered the power within by paying attention to subtle signs around me',
                'language': 'en',
                'category': 'professional_development',
                'themes': ['career_growth', 'mindful_awareness', 'life_optimization']
            }
        }
    ]
    
    generator = OptimizedThumbnailGenerator()
    results = []
    
    for video_info in production_videos:
        filename = video_info['filename']
        language = video_info['language']
        story_data = video_info['story_data']
        
        print(f"\n🎬 Processing: {filename}")
        print(f"🌍 Language: {language.upper()}")
        print(f"📝 Optimized Title: {story_data['youtube_title']}")
        print(f"🎯 Style: Secular, professional, engaging")
        
        try:
            video_id = f"story_001_{language}_optimized"
            
            thumbnail_path = generator.generate_thumbnail(
                story_data=story_data,
                language=language, 
                video_id=video_id
            )
            
            if thumbnail_path:
                print(f"✅ SUCCESS! Optimized thumbnail generated:")
                print(f"📁 {thumbnail_path}")
                
                results.append({
                    'language': language,
                    'filename': filename,
                    'thumbnail_path': thumbnail_path,
                    'title': story_data['youtube_title'],
                    'status': 'success'
                })
            else:
                print(f"❌ Failed to generate optimized thumbnail")
                results.append({
                    'language': language,
                    'filename': filename, 
                    'status': 'failed'
                })
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                'language': language,
                'filename': filename,
                'error': str(e),
                'status': 'error'
            })
    
    # Setup universal strategy for other languages
    if results and results[0]['status'] == 'success':
        setup_optimized_universal_strategy(results[0]['thumbnail_path'])
    
    # Summary
    print(f"\n📊 OPTIMIZED THUMBNAIL SUMMARY")
    print("=" * 40)
    
    successful = [r for r in results if r['status'] == 'success']
    
    if successful:
        print(f"✅ Generated: {len(successful)} optimized thumbnail(s)")
        for result in successful:
            print(f"  {result['language'].upper()}: {result['title']}")
            print(f"     📁 {result['thumbnail_path']}")
    
    print(f"\n🎯 OPTIMIZATIONS APPLIED:")
    print(f"  ✅ Secular, professional tone (not preachy/religious)")
    print(f"  ✅ Engaging text overlay for higher CTR")
    print(f"  ✅ Modern workplace/life coaching aesthetic")
    print(f"  ✅ Clickable, benefit-focused titles")
    print(f"  ✅ Universal strategy (75% cost savings)")

def setup_optimized_universal_strategy(source_thumbnail_path):
    """Copy optimized English thumbnail to other languages"""
    
    print(f"\n🔄 Setting up optimized universal strategy...")
    
    base_dir = os.path.dirname(os.path.dirname(source_thumbnail_path))
    languages = ['es', 'fr', 'ur']
    
    for lang in languages:
        lang_dir = os.path.join(base_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        target_file = os.path.join(lang_dir, f"story_001_{lang}_optimized_thumbnail.png")
        
        try:
            shutil.copy2(source_thumbnail_path, target_file)
            print(f"✅ {lang.upper()}: Copied optimized thumbnail")
        except Exception as e:
            print(f"❌ {lang.upper()}: Failed to copy - {e}")

if __name__ == "__main__":
    generate_optimized_production_thumbnails()