#!/usr/bin/env python3
"""
Enhanced Video Manager with Branding Outro Integration
Adds outro management capabilities to the existing video production workflow.
"""

import argparse
import sys
from pathlib import Path

# Add the lib directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / "lib"))

from video_tools.video_tracker import VideoTracker, VideoStatus
from video_tools.batch_manager import ProductionBatchManager
from video_tools.branding_outro import BrandingOutro

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

def main():
    """Enhanced video manager with outro capabilities."""
    parser = argparse.ArgumentParser(description='Video Production Manager with Branding')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Existing commands (keeping them for compatibility)
    register_parser = subparsers.add_parser('register', help='Register translated stories')
    status_parser = subparsers.add_parser('status', help='Show production status')
    batch_parser = subparsers.add_parser('batch', help='Get next production batch')
    schedule_parser = subparsers.add_parser('schedule', help='Auto-schedule videos')
    report_parser = subparsers.add_parser('report', help='Generate production report')
    
    # Add outro commands
    add_outro_commands(subparsers)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Handle outro commands
    if args.command == 'outro':
        if not args.outro_action:
            print("Available outro actions: generate, export, checklist, update")
            return
        handle_outro_commands(args)
        return
    
    # Handle existing commands
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
        print("🎬 Next Production Batch")
        print("=" * 50)
        get_next_batch(batch_manager)
    
    elif args.command == 'schedule':
        print("📅 Auto-scheduling videos...")
        auto_schedule_videos(batch_manager)
    
    elif args.command == 'report':
        print("📈 Production Report")
        print("=" * 50)
        generate_report(tracker)

def register_translated_stories(tracker):
    """Register all translated stories from the stories directory."""
    base_path = Path(__file__).parent.parent
    stories_path = base_path / "data" / "stories"
    
    registered_count = 0
    
    # Process each language directory
    for lang_dir in stories_path.iterdir():
        if lang_dir.is_dir() and lang_dir.name in ['en', 'es', 'fr', 'ur', 'ar']:
            language = lang_dir.name
            
            # Look for script files
            for script_file in lang_dir.glob("*_SCRIPT.txt"):
                try:
                    # Read the script to get title and content
                    with open(script_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract title from filename or content
                    if "ENGLISH" in script_file.name:
                        title = "Seeing Signs: A Journey to Inner Strength"
                    elif "SPANISH" in script_file.name:
                        title = "Ver Señales: Un Viaje hacia la Fortaleza Interior"
                    elif "FRENCH" in script_file.name:
                        title = "Voir les Signes : Un Voyage vers la Force Intérieure"
                    elif "URDU" in script_file.name:
                        title = "نشانیاں دیکھنا: اندرونی طاقت کا سفر"
                    elif "ARABIC" in script_file.name:
                        title = "رؤية العلامات: رحلة إلى القوة الداخلية"
                    else:
                        title = f"Story in {language.upper()}"
                    
                    # Estimate duration (assuming ~150 words per minute)
                    word_count = len(content.split())
                    duration_seconds = int((word_count / 150) * 60)
                    
                    # Register with tracker
                    video_id = tracker.register_script(
                        story_id="story_001",
                        language=language,
                        script_path=str(script_file),
                        title=title,
                        duration_seconds=duration_seconds
                    )
                    
                    print(f"✅ Registered {language.upper()}: {title}")
                    registered_count += 1
                    
                except Exception as e:
                    print(f"❌ Failed to register {script_file}: {e}")
    
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

def get_next_batch(batch_manager):
    """Get and display next production batch."""
    batch = batch_manager.get_next_production_batch()
    
    if not batch:
        print("No videos ready for production.")
        return
    
    print(f"📦 Next batch ready: {len(batch)} videos")
    print("\n🎬 Videos to create:")
    
    for i, video in enumerate(batch, 1):
        print(f"{i}. {video.language.upper()}: {video.title}")
        print(f"   Script: {video.script_path}")
        print(f"   Duration: ~{video.duration_seconds}s")
        print()
    
    print("💡 Next steps:")
    print("1. Create videos in Instadoodle using the scripts")
    print("2. Add branding outro (run: python scripts/enhanced_video_manager.py outro generate story_001_en)")
    print("3. Save videos to data/videos/production/{language}/")
    print("4. Update status: tracker.update_status(video_id, VideoStatus.VIDEO_READY)")

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