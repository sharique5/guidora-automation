#!/usr/bin/env python3
"""
Final YouTube Upload System Setup
Prepares everything needed for production upload
"""

import os
import sys
import shutil
from pathlib import Path

def setup_final_upload_system():
    """Prepare final upload system with correct file paths"""
    
    print("🚀 FINAL YOUTUBE UPLOAD SYSTEM SETUP")
    print("=" * 50)
    
    # Map correct thumbnail files
    thumbnail_mapping = {
        'en': 'story_001_en_optimized_optimized_thumbnail_with_text.png',
        'es': 'story_001_es_optimized_thumbnail.png', 
        'fr': 'story_001_fr_optimized_thumbnail.png',
        'ur': 'story_001_ur_optimized_thumbnail.png'
    }
    
    print("\n📋 CHECKING PRODUCTION ASSETS:")
    
    # Video files
    video_files = {}
    for lang in ['en', 'es', 'fr', 'ur']:
        video_path = f"data/videos/production/{lang}/seeing_signs_a_journey_to_inner_strength_{lang}.mp4"
        if os.path.exists(video_path):
            video_files[lang] = video_path
            print(f"✅ Video {lang.upper()}: {video_path}")
        else:
            print(f"❌ Video {lang.upper()}: Missing {video_path}")
    
    # Thumbnail files
    thumbnail_files = {}
    for lang in ['en', 'es', 'fr', 'ur']:
        thumb_path = f"assets/thumbnails/{lang}/{thumbnail_mapping[lang]}"
        if os.path.exists(thumb_path):
            thumbnail_files[lang] = thumb_path
            print(f"✅ Thumb {lang.upper()}: {thumb_path}")
        else:
            print(f"❌ Thumb {lang.upper()}: Missing {thumb_path}")
    
    # Create upload configuration
    upload_config = {
        'videos': video_files,
        'thumbnails': thumbnail_files,
        'metadata': {
            'en': {
                'title': 'The Hidden Signs That Changed Everything',
                'description': 'Discover how missing one opportunity can lead to finding your true path. This story explores how unexpected setbacks often contain hidden messages that guide us toward our authentic purpose.',
                'tags': ['personal development', 'mindfulness', 'inspiration', 'life lessons', 'growth', 'motivation'],
                'privacy': 'private'  # Start with private for testing
            },
            'es': {
                'title': 'Las Señales Ocultas Que Lo Cambiaron Todo', 
                'description': 'Descubre cómo perder una oportunidad puede llevarte a encontrar tu verdadero camino. Esta historia explora cómo los contratiempos inesperados contienen mensajes ocultos.',
                'tags': ['desarrollo personal', 'mindfulness', 'inspiración', 'lecciones de vida', 'crecimiento'],
                'privacy': 'private'
            },
            'fr': {
                'title': 'Les Signes Cachés Qui Ont Tout Changé',
                'description': 'Découvrez comment manquer une opportunité peut vous mener vers votre véritable chemin. Cette histoire explore comment les revers inattendus contiennent des messages cachés.',
                'tags': ['développement personnel', 'pleine conscience', 'inspiration', 'leçons de vie', 'croissance'],
                'privacy': 'private'
            },
            'ur': {
                'title': 'چھپے ہوئے نشانات جنہوں نے سب کچھ بدل دیا',
                'description': 'دریافت کریں کہ کیسے ایک موقع کھونا آپ کو اپنے اصل راستے کی طرف لے جا سکتا ہے۔ یہ کہانی بتاتی ہے کہ کیسے غیر متوقع رکاوٹوں میں چھپے ہوئے پیغامات ہوتے ہیں۔',
                'tags': ['ذاتی ترقی', 'ذہن سازی', 'تحریک', 'زندگی کے اسباق', 'نمو'],
                'privacy': 'private'
            }
        }
    }
    
    # Save configuration
    import json
    with open('config/upload_config.json', 'w', encoding='utf-8') as f:
        json.dump(upload_config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Created upload configuration: config/upload_config.json")
    
    # Create final upload script
    upload_script = '''#!/usr/bin/env python3
"""
Production YouTube Upload Script
Upload all videos with proper metadata and thumbnails
"""

import sys
import os
import json
sys.path.append('lib')
sys.path.append('lib/video_tools')

from youtube_uploader import YouTubeUploader

def load_upload_config():
    """Load upload configuration"""
    with open('config/upload_config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def upload_all_videos():
    """Upload all production videos"""
    
    print("🚀 UPLOADING ALL PRODUCTION VIDEOS")
    print("=" * 50)
    
    # Load configuration
    config = load_upload_config()
    
    # Initialize uploader
    uploader = YouTubeUploader()
    
    # Authenticate
    if not uploader.authenticate():
        print("❌ Authentication failed")
        return
    
    results = []
    
    for lang in ['en', 'es', 'fr', 'ur']:
        if lang not in config['videos']:
            print(f"⏭️ Skipping {lang.upper()}: No video file")
            continue
        
        video_path = config['videos'][lang]
        thumbnail_path = config['thumbnails'].get(lang)
        metadata = config['metadata'][lang].copy()
        
        # Add thumbnail to metadata if available
        if thumbnail_path:
            metadata['thumbnail_path'] = thumbnail_path
        
        print(f"\\n🎬 Uploading {lang.upper()} video...")
        print(f"📁 Video: {os.path.basename(video_path)}")
        print(f"📝 Title: {metadata['title']}")
        if thumbnail_path:
            print(f"🖼️ Thumbnail: {os.path.basename(thumbnail_path)}")
        
        # Upload video
        video_id = uploader.upload_video(
            video_path=video_path,
            metadata=metadata,
            language=lang
        )
        
        if video_id:
            video_url = f"https://youtube.com/watch?v={video_id}"
            print(f"✅ SUCCESS! {lang.upper()} uploaded: {video_url}")
            results.append({
                'language': lang,
                'video_id': video_id,
                'url': video_url,
                'title': metadata['title']
            })
        else:
            print(f"❌ Upload failed for {lang.upper()}")
    
    # Summary
    print(f"\\n📊 UPLOAD SUMMARY")
    print("=" * 30)
    print(f"✅ Successful uploads: {len(results)}")
    
    if results:
        print(f"\\n🎯 Uploaded Videos:")
        for result in results:
            print(f"  {result['language'].upper()}: {result['title']}")
            print(f"     🔗 {result['url']}")
    
    # Save results
    with open('upload_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\\n📋 Results saved to: upload_results.json")
    
    return results

if __name__ == "__main__":
    upload_all_videos()
'''
    
    with open('upload_production_videos.py', 'w', encoding='utf-8') as f:
        f.write(upload_script)
    
    print(f"✅ Created production upload script: upload_production_videos.py")
    
    # Summary
    print(f"\n📊 SETUP SUMMARY:")
    print(f"✅ Configuration: config/upload_config.json")
    print(f"✅ Upload script: upload_production_videos.py") 
    print(f"✅ Videos ready: {len(video_files)}/4")
    print(f"✅ Thumbnails ready: {len(thumbnail_files)}/4")
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. Get YouTube credentials: config/youtube_credentials.json")
    print(f"2. Test authentication: python lib/video_tools/youtube_uploader.py")
    print(f"3. Upload videos: python upload_production_videos.py")
    
    print(f"\n💡 CREDENTIALS SETUP:")
    print(f"   • Go to: https://console.cloud.google.com/")
    print(f"   • Enable YouTube Data API v3")
    print(f"   • Create OAuth 2.0 credentials")
    print(f"   • Download as: config/youtube_credentials.json")

if __name__ == "__main__":
    setup_final_upload_system()