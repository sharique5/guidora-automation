#!/usr/bin/env python3
"""
Generate thumbnail for a specific story

Usage:
    python generate_thumbnail.py 004_sarah_nurse_story_en
    python generate_thumbnail.py 004_sarah_nurse_story_en --short hook
"""

import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

sys.path.append('lib')
sys.path.append('lib/video_tools')

from whiteboard_thumbnail_generator import WhiteboardThumbnailGenerator

load_dotenv()

def generate_thumbnail(story_id: str, is_short: bool = False, short_type: str = None):
    """Generate thumbnail for story or short"""
    
    print("🎨 THUMBNAIL GENERATOR")
    print("=" * 70)
    
    # Determine file path
    if is_short:
        story_file = Path(f"data/stories/shorts/{story_id}.json")
        output_dir = Path("assets/thumbnails/shorts")
    else:
        story_file = Path(f"data/stories/youtube_optimized/{story_id}.json")
        output_dir = Path("assets/thumbnails/main")
    
    # Load story data
    if not story_file.exists():
        print(f"❌ Story file not found: {story_file}")
        return None
    
    with open(story_file, 'r', encoding='utf-8') as f:
        story_data = json.load(f)
    
    print(f"📖 Story: {story_id}")
    
    # Extract metadata from story
    youtube_metadata = story_data.get('youtube_metadata', '')
    
    # Parse title from metadata
    title = None
    
    # Check if it's a short (different structure)
    if is_short:
        short_content = story_data.get('short_content', '')
        for line in short_content.split('\n'):
            if '**SHORT TITLE**:' in line:
                title = line.split('**SHORT TITLE**:')[1].strip().strip('"')
                break
    else:
        # Main story - check youtube_metadata first
        for line in youtube_metadata.split('\n'):
            if line.startswith('**Title**:'):
                title = line.replace('**Title**:', '').strip().strip('"')
                break
    
    if not title:
        # Fallback to story_content
        content = story_data.get('story_content', '')
        for line in content.split('\n'):
            if line.startswith('**Title**:'):
                title = line.replace('**Title**:', '').strip().strip('"')
                break
    
    if not title:
        print(f"❌ Could not extract title from story")
        return None
    
    print(f"📝 Title: {title}")
    
    # Parse thumbnail concept
    thumbnail_concept = None
    for line in youtube_metadata.split('\n'):
        if '**Thumbnail Concept**:' in line:
            # Get this line and next few lines
            idx = youtube_metadata.index(line)
            concept_section = youtube_metadata[idx:idx+300]
            thumbnail_concept = concept_section.split('**Target Keywords**:')[0]
            thumbnail_concept = thumbnail_concept.replace('**Thumbnail Concept**:', '').strip()
            break
    
    if thumbnail_concept:
        print(f"💡 Concept: {thumbnail_concept[:100]}...")
    
    # Initialize generator
    generator = WhiteboardThumbnailGenerator()
    
    # Prepare video data (for generate_thumbnail it expects story_data, language, video_id)
    video_data = {
        'story_number': story_id.split('_')[0],
        'title': title,
        'youtube_title': title,
        'description': youtube_metadata,
        'language': 'en',
        'category': 'personal_transformation',
        'themes': ['transformation', 'inspiration', 'real_stories'],
        'thumbnail_concept': thumbnail_concept,
        'is_short': is_short,
        'short_type': short_type
    }
    
    print(f"\n🎬 Generating thumbnail...")
    print(f"📐 Size: 1280x720")
    print(f"🎯 Style: Whiteboard sketch with human face")
    print(f"💰 Cost: ~$0.04 (DALL-E 3 standard quality)")
    
    # Generate thumbnail (correct signature: story_data, language, video_id)
    thumbnail_path = generator.generate_thumbnail(
        story_data=video_data,
        language='en',
        video_id=story_id
    )
    
    if thumbnail_path:
        print(f"\n✅ SUCCESS!")
        print(f"📁 {thumbnail_path}")
        print(f"📊 File size: {Path(thumbnail_path).stat().st_size / 1024:.2f} KB")
        return thumbnail_path
    else:
        print(f"\n❌ Failed to generate thumbnail")
        return None

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python generate_thumbnail.py <story_id> [--short <type>]")
        print("\nExamples:")
        print("  python generate_thumbnail.py 004_sarah_nurse_story_en")
        print("  python generate_thumbnail.py 004_sarah_short_hook --short hook")
        sys.exit(1)
    
    story_id = sys.argv[1]
    
    # Check if this is a short
    is_short = '--short' in sys.argv or '_short_' in story_id
    short_type = None
    
    if '--short' in sys.argv:
        short_idx = sys.argv.index('--short')
        if short_idx + 1 < len(sys.argv):
            short_type = sys.argv[short_idx + 1]
    elif '_short_' in story_id:
        # Extract short type from ID
        if '_short_hook' in story_id:
            short_type = 'hook'
        elif '_short_wisdom' in story_id:
            short_type = 'wisdom'
        elif '_short_crisis' in story_id:
            short_type = 'crisis'
    
    generate_thumbnail(story_id, is_short, short_type)

if __name__ == "__main__":
    main()
