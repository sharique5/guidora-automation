#!/usr/bin/env python3
"""
Updated Enhanced Video Manager with Smart Naming
Integrates video naming system for clean, consistent file management.
"""

import argparse
import sys
from pathlib import Path

# Add the lib directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / "lib"))

from video_tools.video_tracker import VideoTracker, VideoStatus
from video_tools.batch_manager import ProductionBatchManager
from video_tools.branding_outro import BrandingOutro
from video_tools.video_naming import VideoNamingManager

def add_naming_commands(parser):
    """Add naming-related commands to the argument parser."""
    naming_parser = parser.add_parser('naming', help='Manage video file naming')
    naming_subparsers = naming_parser.add_subparsers(dest='naming_action', help='Naming actions')
    
    # Show naming reference
    reference_parser = naming_subparsers.add_parser('reference', help='Show video naming reference')
    
    # Generate filename for specific story
    filename_parser = naming_subparsers.add_parser('filename', help='Generate filename for story')
    filename_parser.add_argument('story_file', help='Path to story JSON file')
    filename_parser.add_argument('--language', '-l', required=True, help='Language code')
    filename_parser.add_argument('--with-date', action='store_true', help='Include date in filename')
    
    # Show batch filenames
    batch_parser = naming_subparsers.add_parser('batch', help='Show all batch filenames')
    batch_parser.add_argument('--with-date', action='store_true', help='Include dates in filenames')

def handle_naming_commands(args):
    """Handle naming-related commands."""
    naming_manager = VideoNamingManager()
    
    if args.naming_action == 'reference':
        print("📁 VIDEO NAMING REFERENCE")
        print("=" * 60)
        reference = naming_manager.export_naming_reference()
        print(reference)
    
    elif args.naming_action == 'filename':
        print(f"📝 Generating filename for: {args.story_file}")
        print("=" * 60)
        
        if not Path(args.story_file).exists():
            print(f"❌ File not found: {args.story_file}")
            return
        
        story_id = naming_manager.get_story_id_from_filename(args.story_file)
        filename = naming_manager.generate_video_filename(
            args.story_file, args.language, args.with_date
        )
        
        story_info = naming_manager.get_story_info_from_file(args.story_file)
        
        print(f"📚 Story ID: {story_id}")
        print(f"🎬 Video filename: {filename}")
        print(f"📂 Full path: data/videos/production/{args.language}/{filename}")
        print(f"🎯 Title: {story_info['title']}")
        print(f"⏱️ Duration: ~{story_info['duration']}s")
    
    elif args.naming_action == 'batch':
        print("📦 BATCH FILENAME GENERATION")
        print("=" * 60)
        
        batch_filenames = naming_manager.generate_batch_filenames(args.with_date)
        
        if not batch_filenames:
            print("❌ No stories found for naming")
            return
        
        # Group by story
        by_story = {}
        for key, info in batch_filenames.items():
            story_id = info['story_id']
            if story_id not in by_story:
                by_story[story_id] = []
            by_story[story_id].append(info)
        
        for story_id in sorted(by_story.keys()):
            versions = by_story[story_id]
            
            # Get title from English version
            title = "Unknown Title"
            for version in versions:
                if version['language'] == 'en':
                    story_info = naming_manager.get_story_info_from_file(version['story_file'])
                    title = story_info['title']
                    break
            
            print(f"\n🎬 {story_id}: {title}")
            print("-" * 40)
            
            for version in sorted(versions, key=lambda x: x['language']):
                lang = version['language'].upper()
                filename = version['video_filename']
                path = version['video_path']
                
                print(f"  {lang}: {filename}")
                print(f"      → {path}")

def enhanced_batch_command():
    """Enhanced batch command with naming integration."""
    tracker = VideoTracker()
    batch_manager = ProductionBatchManager()
    naming_manager = VideoNamingManager()
    
    print("🎬 ENHANCED PRODUCTION BATCH")
    print("=" * 60)
    
    batch = batch_manager.get_next_production_batch()
    
    if not batch:
        print("❌ No videos ready for production.")
        return
    
    print(f"📦 Next batch ready: {len(batch)} videos\n")
    
    for i, video in enumerate(batch, 1):
        # Generate proper filename
        filename = naming_manager.generate_video_filename(
            video.script_path, video.language, False
        )
        
        story_id = naming_manager.get_story_id_from_filename(video.script_path)
        
        print(f"{i}. 🌍 {video.language.upper()}: {video.title}")
        print(f"   📝 Script: {video.script_path}")
        print(f"   🎬 Video file: {filename}")
        print(f"   📂 Save to: data/videos/production/{video.language}/{filename}")
        print(f"   ⏱️ Duration: ~{video.duration_seconds}s")
        print(f"   🆔 Story ID: {story_id}")
        print()
    
    print("💡 PRODUCTION WORKFLOW:")
    print("1. Create main content in Instadoodle using scripts above")
    print("2. Generate outro: python scripts/enhanced_video_manager.py outro generate <story_id>_<lang>")
    print("3. Add 6-second outro to end of video in Instadoodle")
    print("4. Export and save with exact filenames shown above")
    print("5. Update tracking: python scripts/enhanced_video_manager.py update-status <video_id> video_ready")

def add_update_commands(parser):
    """Add video status update commands."""
    update_parser = parser.add_parser('update-status', help='Update video production status')
    update_parser.add_argument('video_id', help='Video ID (e.g., story_001_en)')
    update_parser.add_argument('status', help='New status (script_ready, in_production, video_ready, etc.)')
    update_parser.add_argument('--video-path', help='Path to video file')
    update_parser.add_argument('--duration', type=int, help='Video duration in seconds')
    update_parser.add_argument('--file-size', type=float, help='File size in MB')

def handle_update_commands(args):
    """Handle video status update commands."""
    tracker = VideoTracker()
    
    # Convert string status to VideoStatus enum
    status_map = {
        'script_ready': VideoStatus.SCRIPT_READY,
        'in_production': VideoStatus.IN_PRODUCTION,
        'video_ready': VideoStatus.VIDEO_READY,
        'thumbnail_needed': VideoStatus.THUMBNAIL_NEEDED,
        'ready_to_publish': VideoStatus.READY_TO_PUBLISH,
        'scheduled': VideoStatus.SCHEDULED,
        'published': VideoStatus.PUBLISHED,
        'failed': VideoStatus.FAILED
    }
    
    if args.status not in status_map:
        print(f"❌ Invalid status. Valid options: {', '.join(status_map.keys())}")
        return
    
    status = status_map[args.status]
    
    # Prepare update kwargs
    update_kwargs = {}
    if args.video_path:
        update_kwargs['video_path'] = args.video_path
    if args.duration:
        update_kwargs['duration_seconds'] = args.duration
    if args.file_size:
        update_kwargs['file_size_mb'] = args.file_size
    
    try:
        tracker.update_status(args.video_id, status, **update_kwargs)
        print(f"✅ Updated {args.video_id} status to {args.status}")
        
        if update_kwargs:
            print("📊 Updated metadata:")
            for key, value in update_kwargs.items():
                print(f"   {key}: {value}")
    
    except ValueError as e:
        print(f"❌ Error: {e}")

def main():
    """Enhanced video manager with naming and update capabilities."""
    parser = argparse.ArgumentParser(description='Enhanced Video Production Manager')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Existing commands
    register_parser = subparsers.add_parser('register', help='Register translated stories')
    status_parser = subparsers.add_parser('status', help='Show production status')
    batch_parser = subparsers.add_parser('batch', help='Get enhanced production batch')
    schedule_parser = subparsers.add_parser('schedule', help='Auto-schedule videos')
    report_parser = subparsers.add_parser('report', help='Generate production report')
    
    # Add new command groups
    add_outro_commands(subparsers)
    add_naming_commands(subparsers)
    add_update_commands(subparsers)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Handle new command types
    if args.command == 'outro':
        if not args.outro_action:
            print("Available outro actions: generate, export, checklist, update")
            return
        handle_outro_commands(args)
        return
    
    elif args.command == 'naming':
        if not args.naming_action:
            print("Available naming actions: reference, filename, batch")
            return
        handle_naming_commands(args)
        return
    
    elif args.command == 'update-status':
        handle_update_commands(args)
        return
    
    # Handle existing commands with enhancements
    tracker = VideoTracker()
    batch_manager = ProductionBatchManager()
    
    if args.command == 'register':
        print("🔄 Registering all translated stories...")
        register_translated_stories(tracker)
    
    elif args.command == 'status':
        print("📊 Production Status")
        print("=" * 50)
        show_status(tracker)
    
    elif args.command == 'batch':
        enhanced_batch_command()  # Use enhanced version
    
    elif args.command == 'schedule':
        print("📅 Auto-scheduling videos...")
        auto_schedule_videos(batch_manager)
    
    elif args.command == 'report':
        print("📈 Production Report")
        print("=" * 50)
        generate_report(tracker)

# Copy existing functions from previous file
def add_outro_commands(parser):
    """Add outro-related commands to the argument parser."""
    outro_parser = parser.add_parser('outro', help='Manage video outros and branding')
    outro_subparsers = outro_parser.add_subparsers(dest='outro_action', help='Outro actions')
    
    # Generate outro for specific video
    generate_parser = outro_subparsers.add_parser('generate', help='Generate outro for specific video')
    generate_parser.add_argument('video_id', help='Video ID to generate outro for')
    generate_parser.add_argument('--language', '-l', default='en', help='Language code (en, es, fr, ur, ar)')
    
    # Export all outros
    export_parser = outro_subparsers.add_parser('export', help='Export all outro configurations')
    
    # Show assets checklist
    checklist_parser = outro_subparsers.add_parser('checklist', help='Show branding assets checklist')
    
    # Update outro messages
    update_parser = outro_subparsers.add_parser('update', help='Update outro messages for language')
    update_parser.add_argument('language', help='Language code to update')
    update_parser.add_argument('--main-text', help='Main thank you message')
    update_parser.add_argument('--subscribe-text', help='Subscribe call-to-action text')
    update_parser.add_argument('--channel-name', help='Channel name')

def handle_outro_commands(args):
    """Handle outro-related commands."""
    outro_system = BrandingOutro()
    
    if args.outro_action == 'generate':
        print(f"🎨 Generating outro for {args.video_id} ({args.language})")
        print("=" * 60)
        
        outro_package = outro_system.get_outro_for_video(args.video_id, args.language)
        
        print("📝 OUTRO SCRIPT:")
        print(outro_package["script"])
        
        print("\n🎬 INSTADOODLE INSTRUCTIONS:")
        instructions = outro_package["instadoodle_instructions"]
        print(f"Duration: {instructions['duration']}")
        print(f"\nScene Description:\n{instructions['scene_description']}")
        print(f"\nVoice Script: {instructions['voice_script']}")
        
        print(f"\n📦 Required Assets:")
        for asset in outro_package["assets_needed"]:
            print(f"  - {asset}")
    
    elif args.outro_action == 'export':
        print("📤 Exporting all outro configurations...")
        all_outros = outro_system.export_all_outros()
        print(f"✅ Exported outros for {len(all_outros)} languages:")
        for lang in all_outros.keys():
            print(f"  - {lang.upper()}")
        print(f"\n💾 Saved to: data/outro_exports.json")
    
    elif args.outro_action == 'checklist':
        print("📋 BRANDING ASSETS CHECKLIST")
        print("=" * 60)
        checklist = outro_system.create_assets_checklist()
        print(checklist)
    
    elif args.outro_action == 'update':
        print(f"🔄 Updating outro messages for {args.language}")
        
        updates = {}
        if args.main_text:
            updates['main_text'] = args.main_text
        if args.subscribe_text:
            updates['subscribe_text'] = args.subscribe_text
        if args.channel_name:
            updates['channel_name'] = args.channel_name
        
        if updates:
            outro_system.update_outro_messages(args.language, updates)
            print(f"✅ Updated {len(updates)} fields for {args.language}")
        else:
            print("❌ No updates specified. Use --main-text, --subscribe-text, or --channel-name")

# Include other existing functions...
def register_translated_stories(tracker):
    """Register all translated stories from the stories directory."""
    base_path = Path(__file__).parent.parent
    stories_path = base_path / "data" / "stories"
    naming_manager = VideoNamingManager()
    
    registered_count = 0
    
    # Process each language directory
    for lang_dir in stories_path.iterdir():
        if lang_dir.is_dir() and lang_dir.name in ['en', 'es', 'fr', 'ur', 'ar']:
            language = lang_dir.name
            
            # Look for JSON files (more reliable than script files)
            for story_file in lang_dir.glob("*.json"):
                try:
                    # Get story info and generate proper IDs
                    story_info = naming_manager.get_story_info_from_file(str(story_file))
                    story_id = naming_manager.get_story_id_from_filename(str(story_file))
                    
                    # Create proper video ID
                    video_id = f"{story_id}_{language}"
                    
                    # Register with tracker
                    tracker.register_script(
                        story_id=story_id.replace('story_', ''),  # Remove prefix for internal ID
                        language=language,
                        script_path=str(story_file),
                        title=story_info['title'],
                        duration_seconds=story_info['duration']
                    )
                    
                    print(f"✅ Registered {video_id}: {story_info['title']}")
                    registered_count += 1
                    
                except Exception as e:
                    print(f"❌ Failed to register {story_file}: {e}")
    
    print(f"\n📊 Total registered: {registered_count} videos")

def show_status(tracker):
    """Show current production status."""
    summary = tracker.get_production_summary()
    
    print(f"Total Videos: {summary['total_videos']}")
    print(f"Ready for Production: {summary['next_batch_ready']}")
    print(f"Ready to Publish: {summary['ready_to_publish']}")
    
    print("\n📈 Status Breakdown:")
    for status, count in summary['by_status'].items():
        if count > 0:
            print(f"  {status.replace('_', ' ').title()}: {count}")
    
    print("\n🌍 Language Distribution:")
    for language, count in summary['by_language'].items():
        if count > 0:
            print(f"  {language.upper()}: {count}")

def auto_schedule_videos(batch_manager):
    """Auto-schedule ready videos."""
    scheduled = batch_manager.auto_schedule_videos()
    
    if scheduled:
        print(f"📅 Scheduled {len(scheduled)} videos:")
        for video, publish_time in scheduled:
            print(f"  {video.language.upper()}: {video.title} → {publish_time}")
    else:
        print("No videos ready for scheduling.")

def generate_report(tracker):
    """Generate comprehensive production report."""
    report = tracker.export_production_report()
    print(report)

if __name__ == "__main__":
    main()