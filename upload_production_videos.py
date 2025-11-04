#!/usr/bin/env python3
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
        
        print(f"\n🎬 Uploading {lang.upper()} video...")
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
    print(f"\n📊 UPLOAD SUMMARY")
    print("=" * 30)
    print(f"✅ Successful uploads: {len(results)}")
    
    if results:
        print(f"\n🎯 Uploaded Videos:")
        for result in results:
            print(f"  {result['language'].upper()}: {result['title']}")
            print(f"     🔗 {result['url']}")
    
    # Save results
    with open('upload_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📋 Results saved to: upload_results.json")
    
    return results

if __name__ == "__main__":
    upload_all_videos()
