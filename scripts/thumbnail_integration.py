#!/usr/bin/env python3
"""
Thumbnail Integration for Final Video Manager
Adds thumbnail generation capabilities to the video production workflow.
"""

import sys
from pathlib import Path

# Add the lib directory to the path
sys.path.append(str(Path(__file__).parent.parent / "lib"))

from video_tools.thumbnail_generator import ThumbnailGenerator, ThumbnailConfig
from video_tools.video_naming import VideoNamingManager
import json

def add_thumbnail_commands(parser):
    """Add thumbnail-related commands to the argument parser."""
    thumbnail_parser = parser.add_parser('thumbnail', help='Generate video thumbnails')
    thumbnail_subparsers = thumbnail_parser.add_subparsers(dest='thumbnail_action', help='Thumbnail actions')
    
    # Generate thumbnail for specific video
    generate_parser = thumbnail_subparsers.add_parser('generate', help='Generate thumbnail for specific video')
    generate_parser.add_argument('video_id', help='Video ID (e.g., story_001_en)')
    generate_parser.add_argument('--provider', choices=['openai', 'stability', 'gemini'], 
                                default='openai', help='AI provider to use')
    generate_parser.add_argument('--style', choices=['photorealistic', 'illustration', 'cartoon', 'minimalist'],
                                default='photorealistic', help='Visual style')
    generate_parser.add_argument('--no-text', action='store_true', help='Generate without title overlay')
    
    # Generate batch thumbnails
    batch_parser = thumbnail_subparsers.add_parser('batch', help='Generate thumbnails for current batch')
    batch_parser.add_argument('--provider', choices=['openai', 'stability', 'gemini'], 
                             default='openai', help='Primary AI provider')
    batch_parser.add_argument('--style', choices=['photorealistic', 'illustration', 'cartoon', 'minimalist'],
                             default='photorealistic', help='Visual style for all thumbnails')
    
    # Check provider status
    status_parser = thumbnail_subparsers.add_parser('status', help='Check thumbnail provider status')
    
    # Configure thumbnail settings
    config_parser = thumbnail_subparsers.add_parser('config', help='Configure thumbnail settings')
    config_parser.add_argument('--primary-provider', choices=['openai', 'stability', 'gemini'],
                              help='Set primary provider')
    config_parser.add_argument('--style', choices=['photorealistic', 'illustration', 'cartoon', 'minimalist'],
                              help='Set default style')
    config_parser.add_argument('--include-text', action='store_true', help='Include title overlay')
    config_parser.add_argument('--no-text', action='store_true', help='Disable title overlay')

def handle_thumbnail_commands(args):
    """Handle thumbnail-related commands."""
    
    if args.thumbnail_action == 'status':
        print("🎨 THUMBNAIL PROVIDER STATUS")
        print("=" * 60)
        
        generator = ThumbnailGenerator()
        provider_status = generator.get_provider_status()
        
        for provider, status in provider_status.items():
            available = "✅" if status['available'] else "❌"
            recommended = "⭐" if status['recommended'] else "  "
            cost = f"${status['cost_per_image']:.3f}/image"
            print(f"{recommended} {available} {provider.upper()}: {cost} - {status['best_for']}")
        
        print(f"\n💰 Cost per 5-video batch:")
        print(f"   OpenAI only: $0.20")
        print(f"   Stability only: $0.10") 
        print(f"   Mixed strategy: $0.15")
        
        # Check for missing API keys
        missing_keys = []
        if not status.get('available'):
            if provider == 'openai' and not generator.openai_api_key:
                missing_keys.append('OPENAI_API_KEY')
            elif provider == 'stability' and not generator.stability_api_key:
                missing_keys.append('STABILITY_API_KEY')
            elif provider == 'gemini' and not generator.gemini_api_key:
                missing_keys.append('GEMINI_API_KEY')
        
        if missing_keys:
            print(f"\n⚠️  Missing API keys: {', '.join(missing_keys)}")
            print("   Add them to your .env file to enable those providers")
        
        return
    
    elif args.thumbnail_action == 'generate':
        print(f"🎨 Generating thumbnail for {args.video_id}")
        print("=" * 60)
        
        # Parse video ID to get story info
        parts = args.video_id.split('_')
        if len(parts) < 3:
            print("❌ Invalid video ID format. Use: story_001_en")
            return
        
        story_id = '_'.join(parts[:-1])  # story_001
        language = parts[-1]             # en
        
        # Find story file
        naming_manager = VideoNamingManager()
        stories_path = Path(__file__).parent.parent / "data" / "stories" / language
        
        story_file = None
        for file in stories_path.glob("*.json"):
            if naming_manager.get_story_id_from_filename(str(file)) == story_id:
                story_file = file
                break
        
        if not story_file:
            print(f"❌ Story file not found for {args.video_id}")
            return
        
        # Load story data
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load story data: {e}")
            return
        
        # Configure thumbnail generation
        config = ThumbnailConfig(
            style=args.style,
            primary_provider=args.provider,
            include_title_overlay=not args.no_text
        )
        
        generator = ThumbnailGenerator(config)
        
        # Generate thumbnail
        print(f"🔄 Generating {args.style} thumbnail using {args.provider}...")
        thumbnail_path = generator.generate_thumbnail(story_data, language, args.video_id)
        
        if thumbnail_path:
            print(f"✅ Thumbnail generated: {thumbnail_path}")
            
            # Calculate cost
            cost = generator.providers[args.provider]['cost_per_image']
            print(f"💰 Cost: ${cost:.3f}")
            
            print(f"\n📋 Next steps:")
            print(f"   1. Review thumbnail: {thumbnail_path}")
            print(f"   2. Use for video upload or replace if needed")
            print(f"   3. Update video status: python scripts/final_video_manager.py update-status {args.video_id} thumbnail_ready")
        else:
            print("❌ Thumbnail generation failed")
    
    elif args.thumbnail_action == 'batch':
        print("🎨 BATCH THUMBNAIL GENERATION")
        print("=" * 60)
        
        # Get current production batch
        from video_tools.video_tracker import VideoTracker
        tracker = VideoTracker()
        batch = tracker.get_next_production_batch()
        
        if not batch:
            print("❌ No videos ready for thumbnail generation")
            return
        
        print(f"📦 Generating thumbnails for {len(batch)} videos using {args.provider}")
        
        # Configure thumbnail generation
        config = ThumbnailConfig(
            style=args.style,
            primary_provider=args.provider,
            include_title_overlay=True
        )
        
        generator = ThumbnailGenerator(config)
        naming_manager = VideoNamingManager()
        
        # Prepare batch data
        stories_batch = []
        total_cost = 0
        
        for video_meta in batch:
            # Load story data
            try:
                with open(video_meta.script_path, 'r', encoding='utf-8') as f:
                    story_data = json.load(f)
                
                video_id = f"{naming_manager.get_story_id_from_filename(video_meta.script_path)}_{video_meta.language}"
                
                stories_batch.append({
                    'story_data': story_data,
                    'language': video_meta.language,
                    'video_id': video_id
                })
                
                cost = generator.providers[args.provider]['cost_per_image']
                total_cost += cost
                
            except Exception as e:
                print(f"❌ Failed to load {video_meta.script_path}: {e}")
        
        print(f"💰 Estimated total cost: ${total_cost:.3f}")
        
        # Generate batch
        results = generator.generate_batch_thumbnails(stories_batch)
        
        print(f"\n✅ Generated {len(results)} thumbnails:")
        for video_id, thumbnail_path in results.items():
            print(f"   {video_id}: {thumbnail_path}")
        
        if len(results) < len(stories_batch):
            failed = len(stories_batch) - len(results)
            print(f"\n⚠️  {failed} thumbnails failed to generate")
    
    elif args.thumbnail_action == 'config':
        print("🔧 THUMBNAIL CONFIGURATION")
        print("=" * 60)
        
        # Load current config or create new
        config_file = Path(__file__).parent.parent / "config" / "thumbnail_config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_file, 'r') as f:
                current_config = json.load(f)
        except:
            current_config = {}
        
        # Update config based on arguments
        if args.primary_provider:
            current_config['primary_provider'] = args.primary_provider
        if args.style:
            current_config['style'] = args.style
        if args.include_text:
            current_config['include_title_overlay'] = True
        if args.no_text:
            current_config['include_title_overlay'] = False
        
        # Save updated config
        with open(config_file, 'w') as f:
            json.dump(current_config, f, indent=2)
        
        print("✅ Configuration updated:")
        for key, value in current_config.items():
            print(f"   {key}: {value}")

def main():
    """Demo thumbnail integration."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Thumbnail Generation Testing')
    add_thumbnail_commands(parser)
    
    args = parser.parse_args()
    
    if not args.command:
        # Show help for thumbnail commands
        print("🎨 Thumbnail Generation Commands:")
        print("=" * 50)
        print("python scripts/final_video_manager.py thumbnail status")
        print("python scripts/final_video_manager.py thumbnail generate story_001_en")
        print("python scripts/final_video_manager.py thumbnail batch")
        return
    
    handle_thumbnail_commands(args)

if __name__ == "__main__":
    main()