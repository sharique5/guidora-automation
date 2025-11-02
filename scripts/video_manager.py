#!/usr/bin/env python3
"""
Video Production Management CLI
Command-line interface for managing video production workflow.
"""

import sys
import os
from pathlib import Path
import argparse
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lib.video_tools.video_tracker import VideoTracker, VideoStatus
from lib.video_tools.batch_manager import ProductionBatchManager
from lib.translators.natural_translator import NaturalTranslator

class VideoManagementCLI:
    """Command-line interface for video production management."""
    
    def __init__(self):
        """Initialize CLI with managers."""
        self.tracker = VideoTracker()
        self.batch_manager = ProductionBatchManager()
        self.translator = NaturalTranslator()
    
    def register_translated_stories(self, stories_dir: str = "data/stories"):
        """
        Register all translated stories as scripts ready for production.
        
        Args:
            stories_dir: Directory containing translated stories
        """
        stories_path = Path(stories_dir)
        if not stories_path.exists():
            print(f"❌ Stories directory not found: {stories_path}")
            return False
        
        registered_count = 0
        
        # Process each language directory
        for lang_dir in stories_path.iterdir():
            if not lang_dir.is_dir() or lang_dir.name.startswith('.'):
                continue
            
            language = lang_dir.name
            print(f"\n📁 Processing {language.upper()} stories...")
            
            # Process each story file
            for story_file in lang_dir.glob("*.json"):
                try:
                    with open(story_file, 'r', encoding='utf-8') as f:
                        story_data = json.load(f)
                    
                    # Extract story information
                    story_id = story_file.stem.replace(f"_{language}", "")
                    title = story_data.get('title', story_file.stem)
                    duration = story_data.get('estimated_duration')
                    
                    # Check if already registered
                    video_id = f"{story_id}_{language}"
                    if video_id in self.tracker.videos:
                        print(f"   ⚠️  Already registered: {title}")
                        continue
                    
                    # Register with tracker
                    registered_id = self.tracker.register_script(
                        story_id=story_id,
                        language=language,
                        script_path=str(story_file),
                        title=title,
                        duration_seconds=duration
                    )
                    
                    print(f"   ✅ Registered: {title} ({registered_id})")
                    registered_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Failed to register {story_file.name}: {e}")
        
        print(f"\n🎉 Registered {registered_count} new scripts for production!")
        return registered_count > 0
    
    def show_status(self):
        """Display current production status."""
        dashboard = self.batch_manager.get_production_dashboard()
        
        print("🎬 Video Production Dashboard")
        print("=" * 50)
        
        # Overview
        overview = dashboard['overview']
        print(f"📊 OVERVIEW")
        print(f"   Total Videos: {overview['total_videos']}")
        print(f"   Ready for Production: {dashboard['next_production_batch']['total_videos']}")
        print(f"   Ready to Publish: {overview['ready_to_publish']}")
        print(f"   Scheduled (Next 7 Days): {dashboard['publishing_schedule']['total_scheduled']}")
        
        # Status breakdown
        print(f"\n📈 STATUS BREAKDOWN")
        for status, count in overview['by_status'].items():
            if count > 0:
                status_display = status.replace('_', ' ').title()
                print(f"   {status_display}: {count}")
        
        # Language distribution
        print(f"\n🌍 BY LANGUAGE")
        for language, count in overview['by_language'].items():
            if count > 0:
                print(f"   {language.upper()}: {count}")
        
        # Next production batch
        next_batch = dashboard['next_production_batch']
        if next_batch['total_videos'] > 0:
            print(f"\n🎯 NEXT PRODUCTION BATCH ({next_batch['total_videos']} videos)")
            for lang, count in next_batch['by_language'].items():
                print(f"   {lang.upper()}: {count} videos")
        
        # Publishing schedule
        schedule = dashboard['publishing_schedule']['by_date']
        if schedule:
            print(f"\n📅 PUBLISHING SCHEDULE")
            for date, count in list(schedule.items())[:7]:  # Next 7 days
                print(f"   {date}: {count} videos")
    
    def get_next_batch(self):
        """Show next production batch details."""
        next_batch = self.batch_manager.get_next_production_batch()
        
        if not next_batch:
            print("📭 No videos ready for production batch")
            return
        
        total_videos = sum(len(videos) for videos in next_batch.values())
        print(f"🎬 Next Production Batch - {total_videos} Videos")
        print("=" * 50)
        
        for lang, videos in next_batch.items():
            print(f"\n🗣️  {lang.upper()} - {len(videos)} videos:")
            for video in videos:
                duration = f"{video.duration_seconds}s" if video.duration_seconds else "Unknown"
                created = datetime.fromisoformat(video.created_at).strftime("%m/%d")
                print(f"   • {video.title} ({duration}) - Created: {created}")
        
        # Ask if user wants to mark as in production
        response = input(f"\n📤 Mark these {total_videos} videos as 'In Production'? (y/n): ")
        if response.lower() == 'y':
            if self.batch_manager.mark_batch_in_production(next_batch):
                print("✅ Batch marked as in production!")
            else:
                print("❌ Failed to mark batch as in production")
    
    def schedule_videos(self, days: int = 14):
        """Auto-schedule ready videos for publishing."""
        print(f"📅 Auto-scheduling videos for next {days} days...")
        
        if self.batch_manager.auto_schedule_videos(days):
            print("✅ Videos scheduled successfully!")
            
            # Show schedule
            schedule = self.batch_manager.get_publishing_queue(7)
            scheduled_videos = [s for s in schedule if s["assigned_video"]]
            
            if scheduled_videos:
                print(f"\n📺 Scheduled {len(scheduled_videos)} videos:")
                for slot in scheduled_videos[:10]:  # Show first 10
                    video = slot["assigned_video"]
                    date_time = slot["datetime"].strftime("%Y-%m-%d %H:%M")
                    print(f"   {date_time}: {video['language'].upper()} - {video['title'][:50]}...")
        else:
            print("❌ No videos were scheduled")
    
    def update_video_status(self, video_id: str, status: str):
        """Update status of a specific video."""
        try:
            video_status = VideoStatus(status)
            self.tracker.update_status(video_id, video_status)
            print(f"✅ Updated {video_id} status to {status}")
        except ValueError:
            print(f"❌ Invalid status: {status}")
            print(f"Valid statuses: {[s.value for s in VideoStatus]}")
        except Exception as e:
            print(f"❌ Failed to update status: {e}")
    
    def export_report(self, output_file: str = None):
        """Export production report."""
        report = self.batch_manager.export_batch_report()
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 Report exported to: {output_file}")
        else:
            print(report)
    
    def translate_new_stories(self, languages: list = None):
        """Translate new English stories to target languages."""
        languages = languages or ['es', 'fr', 'ur']
        
        # Check for new English stories
        english_stories_dir = Path("data/videos") / "videos.jsonl"  # Adjust path as needed
        
        if not english_stories_dir.exists():
            print("❌ No English stories found to translate")
            return
        
        print(f"🌍 Translating stories to: {', '.join(lang.upper() for lang in languages)}")
        # Implementation would go here to read new stories and translate them
        print("⚠️  Translation feature not yet implemented - use existing translator scripts")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Video Production Management CLI")
    
    parser.add_argument('command', choices=[
        'status', 'register', 'batch', 'schedule', 'update', 'report', 'translate'
    ], help='Command to execute')
    
    parser.add_argument('--video-id', help='Video ID for update command')
    parser.add_argument('--status', help='New status for update command')
    parser.add_argument('--days', type=int, default=14, help='Days ahead for scheduling')
    parser.add_argument('--output', help='Output file for report')
    parser.add_argument('--languages', nargs='+', default=['es', 'fr', 'ur'], 
                       help='Languages for translation')
    
    args = parser.parse_args()
    
    cli = VideoManagementCLI()
    
    try:
        if args.command == 'status':
            cli.show_status()
        elif args.command == 'register':
            cli.register_translated_stories()
        elif args.command == 'batch':
            cli.get_next_batch()
        elif args.command == 'schedule':
            cli.schedule_videos(args.days)
        elif args.command == 'update':
            if not args.video_id or not args.status:
                print("❌ --video-id and --status required for update command")
                return
            cli.update_video_status(args.video_id, args.status)
        elif args.command == 'report':
            cli.export_report(args.output)
        elif args.command == 'translate':
            cli.translate_new_stories(args.languages)
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main() or 0)