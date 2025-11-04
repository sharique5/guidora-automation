#!/usr/bin/env python3
"""
Generate whiteboard thumbnails for actual production videos
"""

import sys
import os
sys.path.append('lib')
sys.path.append('lib/video_tools')

from whiteboard_thumbnail_generator import WhiteboardThumbnailGenerator
from dotenv import load_dotenv
import json

def create_video_data_from_filename(filename, language):
    """Create video data structure from filename and language"""
    
    # Extract story info from filename
    # seeing_signs_a_journey_to_inner_strength_en.mp4
    base_name = filename.replace(f'_{language}.mp4', '').replace('_', ' ').title()
    
    # Create proper YouTube titles for each language
    youtube_titles = {
        'en': 'Seeing Signs: A Journey to Inner Strength',
        'es': 'Viendo Señales: Un Viaje Hacia la Fortaleza Interior', 
        'fr': 'Voir les Signes: Un Voyage vers la Force Intérieure',
        'ur': 'نشانیاں دیکھنا: اندرونی طاقت کا سفر'
    }
    
    descriptions = {
        'en': 'Discover how to recognize the signs around you and build inner strength through mindful awareness and spiritual growth.',
        'es': 'Descubre cómo reconocer las señales a tu alrededor y construir fortaleza interior a través de la conciencia y el crecimiento espiritual.',
        'fr': 'Découvrez comment reconnaître les signes autour de vous et construire une force intérieure grâce à la conscience et la croissance spirituelle.',
        'ur': 'دریافت کریں کہ آپ کے ارد گرد کی نشانیوں کو کیسے پہچانا جائے اور روحانی نمو کے ذریعے اندرونی طاقت کیسے بنائی جائے۔'
    }
    
    return {
        'story_number': 1,
        'title': base_name,
        'youtube_title': youtube_titles.get(language, youtube_titles['en']),
        'youtube_description': descriptions.get(language, descriptions['en']),
        'language': language,
        'video_filename': filename,
        'category': 'spiritual_growth',
        'themes': ['inner_strength', 'spiritual_awareness', 'personal_growth', 'mindfulness']
    }

def generate_production_thumbnails():
    """Generate thumbnails for all production videos"""
    
    # Load environment variables
    load_dotenv()
    
    print("🎨 GENERATING WHITEBOARD THUMBNAILS FOR PRODUCTION VIDEOS")
    print("=" * 60)
    
    # Define our production videos
    production_videos = [
        ('seeing_signs_a_journey_to_inner_strength_en.mp4', 'en'),
        ('seeing_signs_a_journey_to_inner_strength_es.mp4', 'es'), 
        ('seeing_signs_a_journey_to_inner_strength_fr.mp4', 'fr'),
        ('seeing_signs_a_journey_to_inner_strength_ur.mp4', 'ur')
    ]
    
    # Initialize generator
    generator = WhiteboardThumbnailGenerator()
    
    results = []
    
    for filename, language in production_videos:
        print(f"\n🎬 Processing: {filename}")
        print(f"🌍 Language: {language.upper()}")
        
        # Create video data
        video_data = create_video_data_from_filename(filename, language)
        print(f"📝 Title: {video_data['youtube_title']}")
        
        # Check if we should use universal strategy
        if generator.config.language_strategy == "universal" and language != 'en':
            print(f"🔄 Using universal strategy - will reuse English thumbnail")
            print(f"💰 Cost savings: $0.040 per language")
            continue
        
        try:
            print(f"🔄 Generating whiteboard thumbnail...")
            
            # Generate video ID
            video_id = f"story_001_{language}"
            
            thumbnail_path = generator.generate_thumbnail(
                story_data=video_data,
                language=language,
                video_id=video_id
            )
            
            if thumbnail_path:
                print(f"✅ SUCCESS! Thumbnail generated:")
                print(f"📁 {thumbnail_path}")
                results.append({
                    'language': language,
                    'filename': filename,
                    'thumbnail_path': thumbnail_path,
                    'title': video_data['youtube_title'],
                    'status': 'success'
                })
            else:
                print(f"❌ Failed to generate thumbnail")
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
    
    # Summary
    print(f"\n📊 THUMBNAIL GENERATION SUMMARY")
    print("=" * 40)
    
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] != 'success']
    
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print(f"\n🎯 Generated Thumbnails:")
        for result in successful:
            print(f"  {result['language'].upper()}: {result['title']}")
            print(f"     📁 {result['thumbnail_path']}")
    
    if generator.config.language_strategy == "universal":
        print(f"\n💡 Universal Strategy Benefits:")
        print(f"  ✅ English thumbnail can be used for ES, FR, UR")
        print(f"  ✅ Cost: $0.040 instead of $0.160 (75% savings)")
        print(f"  ✅ Consistent branding across languages")
    
    return results

if __name__ == "__main__":
    generate_production_thumbnails()