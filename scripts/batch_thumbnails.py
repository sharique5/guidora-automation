#!/usr/bin/env python3
"""
Batch Thumbnail Generation
Generate thumbnails for all languages in the current story batch.
"""

import sys
import json
from pathlib import Path

# Add the lib directory to the path
sys.path.append(str(Path(__file__).parent.parent / "lib"))

from video_tools.thumbnail_generator import ThumbnailGenerator, ThumbnailConfig
from video_tools.video_naming import VideoNamingManager

def generate_batch_thumbnails():
    """Generate thumbnails for all language versions of current stories."""
    print("🎨 BATCH THUMBNAIL GENERATION")
    print("=" * 60)
    
    # Initialize systems
    naming_manager = VideoNamingManager()
    batch_filenames = naming_manager.generate_batch_filenames()
    
    if not batch_filenames:
        print("❌ No stories found for thumbnail generation")
        return
    
    print(f"📦 Found {len(batch_filenames)} videos for thumbnail generation")
    
    # Configure thumbnail generation
    config = ThumbnailConfig(
        style="photorealistic",
        primary_provider="openai",
        include_title_overlay=True,
        mood="inspirational"
    )
    
    generator = ThumbnailGenerator(config)
    
    # Prepare batch data
    stories_batch = []
    total_cost = 0
    
    print(f"\n🔍 Processing stories:")
    
    for key, info in batch_filenames.items():
        video_id = key
        language = info['language']
        story_file = info['story_file']
        
        print(f"   📚 {language.upper()}: {Path(story_file).name}")
        
        # Load story data
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
            
            stories_batch.append({
                'story_data': story_data,
                'language': language,
                'video_id': video_id
            })
            
            total_cost += 0.040  # OpenAI cost per image
            
        except Exception as e:
            print(f"   ❌ Failed to load {story_file}: {e}")
    
    print(f"\n💰 Total estimated cost: ${total_cost:.3f}")
    print(f"⏱️ Estimated time: {len(stories_batch) * 15} seconds")
    
    # Generate batch
    print(f"\n🔄 Generating {len(stories_batch)} thumbnails...")
    
    results = {}
    successful = 0
    failed = 0
    
    for i, story_info in enumerate(stories_batch, 1):
        video_id = story_info['video_id']
        language = story_info['language']
        
        print(f"\n[{i}/{len(stories_batch)}] 🎨 Generating {language.upper()} thumbnail...")
        
        try:
            thumbnail_path = generator.generate_thumbnail(
                story_info['story_data'],
                language,
                video_id
            )
            
            if thumbnail_path:
                results[video_id] = thumbnail_path
                successful += 1
                print(f"   ✅ Success: {Path(thumbnail_path).name}")
            else:
                failed += 1
                print(f"   ❌ Failed: Generation returned None")
                
        except Exception as e:
            failed += 1
            print(f"   ❌ Error: {e}")
    
    # Summary
    print(f"\n🎯 BATCH COMPLETE!")
    print(f"   ✅ Successful: {successful}/{len(stories_batch)}")
    print(f"   ❌ Failed: {failed}/{len(stories_batch)}")
    print(f"   💰 Actual cost: ${successful * 0.040:.3f}")
    
    if results:
        print(f"\n📁 Generated thumbnails:")
        for video_id, thumbnail_path in results.items():
            lang = video_id.split('_')[-1].upper()
            print(f"   {lang}: {thumbnail_path}")
        
        print(f"\n💡 Next steps:")
        print(f"   1. Review all thumbnails in assets/thumbnails/")
        print(f"   2. Use for your Instadoodle video uploads")
        print(f"   3. Update video tracking with thumbnail paths")
    
    return results

def main():
    """Run batch thumbnail generation."""
    results = generate_batch_thumbnails()
    
    if results and len(results) >= 4:  # Most languages successful
        print(f"\n🌟 PRODUCTION READY!")
        print(f"   You now have professional thumbnails for all languages!")
        print(f"   Your multi-language thumbnail system is fully operational!")
    elif results:
        print(f"\n⚠️ PARTIAL SUCCESS")
        print(f"   Some thumbnails generated, check for any API issues.")
    else:
        print(f"\n🔧 NEEDS ATTENTION")
        print(f"   No thumbnails generated. Check API key and connectivity.")

if __name__ == "__main__":
    main()