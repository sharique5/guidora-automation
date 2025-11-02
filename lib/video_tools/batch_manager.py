#!/usr/bin/env python3
"""
Video Production Batch Manager
Integrates with video tracker to manage production queues and publishing schedules.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

from .video_tracker import VideoTracker, VideoStatus, VideoMetadata

logger = logging.getLogger(__name__)

class ProductionBatchManager:
    """Manages video production batches and publishing schedules."""
    
    def __init__(self, base_path: str = None):
        """Initialize batch manager."""
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent.parent
        self.tracker = VideoTracker(base_path)
        self.batch_config_file = self.base_path / "config" / "production_config.json"
        
        # Default production configuration
        self.config = {
            "batch_size": 5,
            "languages_priority": ["en", "es", "fr", "ur"],  # Production priority order
            "daily_upload_limit": 2,  # Max videos per day across all channels
            "upload_schedule": {
                "start_hour": 10,  # 10 AM
                "end_hour": 18,    # 6 PM
                "timezone": "UTC",
                "days_of_week": [1, 2, 3, 4, 5]  # Monday to Friday
            },
            "quality_thresholds": {
                "min_duration": 60,      # Minimum 1 minute
                "max_duration": 300,     # Maximum 5 minutes
                "min_readability": 8,    # Minimum readability score
                "required_assets": ["script", "video", "thumbnail"]
            }
        }
        
        self._load_config()
    
    def _load_config(self):
        """Load production configuration."""
        if self.batch_config_file.exists():
            try:
                with open(self.batch_config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
            except Exception as e:
                logger.warning(f"Failed to load config, using defaults: {e}")
        else:
            self._save_config()
    
    def _save_config(self):
        """Save production configuration."""
        os.makedirs(self.batch_config_file.parent, exist_ok=True)
        with open(self.batch_config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def get_next_production_batch(self, language_priority: List[str] = None) -> Dict[str, List[VideoMetadata]]:
        """
        Get next batch of videos for production, organized by language.
        
        Args:
            language_priority: Custom language priority order
            
        Returns:
            Dictionary with language codes and video lists ready for production
        """
        priorities = language_priority or self.config["languages_priority"]
        batch_size = self.config["batch_size"]
        
        # Get all videos ready for production
        ready_videos = self.tracker.get_videos_by_status(VideoStatus.SCRIPT_READY)
        
        # Organize by language and apply priority
        language_batches = {}
        videos_per_language = max(1, batch_size // len(priorities))
        
        for lang in priorities:
            lang_videos = [v for v in ready_videos if v.language == lang]
            # Sort by creation date (oldest first)
            lang_videos.sort(key=lambda v: v.created_at)
            
            # Take videos for this batch
            batch_videos = lang_videos[:videos_per_language]
            if batch_videos:
                language_batches[lang] = batch_videos
        
        # Fill remaining slots if available
        total_selected = sum(len(videos) for videos in language_batches.values())
        if total_selected < batch_size:
            remaining_slots = batch_size - total_selected
            
            # Get any remaining videos
            all_selected_ids = {v.story_id + "_" + v.language for videos in language_batches.values() for v in videos}
            remaining_videos = [v for v in ready_videos if (v.story_id + "_" + v.language) not in all_selected_ids]
            
            for video in remaining_videos[:remaining_slots]:
                lang = video.language
                if lang not in language_batches:
                    language_batches[lang] = []
                language_batches[lang].append(video)
        
        return language_batches
    
    def mark_batch_in_production(self, batch: Dict[str, List[VideoMetadata]]) -> bool:
        """Mark all videos in batch as in production."""
        try:
            for lang, videos in batch.items():
                for video in videos:
                    video_id = f"{video.story_id}_{video.language}"
                    self.tracker.update_status(
                        video_id,
                        VideoStatus.IN_PRODUCTION,
                        notes=f"Started production batch on {datetime.now().strftime('%Y-%m-%d')}"
                    )
            
            logger.info(f"Marked {sum(len(videos) for videos in batch.values())} videos as in production")
            return True
            
        except Exception as e:
            logger.error(f"Failed to mark batch in production: {e}")
            return False
    
    def get_publishing_queue(self, days_ahead: int = 14) -> List[Dict[str, Any]]:
        """
        Get optimized publishing schedule for next N days.
        
        Args:
            days_ahead: Number of days to schedule ahead
            
        Returns:
            List of publishing slots with video assignments
        """
        # Get videos ready to publish
        ready_videos = self.tracker.get_ready_to_publish_videos()
        
        if not ready_videos:
            return []
        
        # Generate publishing slots
        publishing_slots = self._generate_publishing_slots(days_ahead)
        
        # Assign videos to slots with language distribution
        scheduled_videos = self._assign_videos_to_slots(ready_videos, publishing_slots)
        
        return scheduled_videos
    
    def _generate_publishing_slots(self, days: int) -> List[Dict[str, Any]]:
        """Generate available publishing time slots."""
        slots = []
        start_date = datetime.now().date()
        schedule_config = self.config["upload_schedule"]
        
        for day_offset in range(days):
            current_date = start_date + timedelta(days=day_offset)
            weekday = current_date.weekday() + 1  # Monday = 1
            
            # Skip weekends if not configured
            if weekday not in schedule_config["days_of_week"]:
                continue
            
            # Generate time slots for this day
            daily_limit = self.config["daily_upload_limit"]
            start_hour = schedule_config["start_hour"]
            end_hour = schedule_config["end_hour"]
            
            if daily_limit > 0:
                # Distribute uploads evenly throughout the day
                hours_available = end_hour - start_hour
                hour_interval = max(1, hours_available // daily_limit)
                
                for slot_num in range(daily_limit):
                    slot_hour = start_hour + (slot_num * hour_interval)
                    if slot_hour < end_hour:
                        slot_time = datetime.combine(current_date, datetime.min.time().replace(hour=slot_hour))
                        slots.append({
                            "datetime": slot_time,
                            "date": current_date,
                            "slot_number": slot_num + 1,
                            "assigned_video": None
                        })
        
        return slots
    
    def _assign_videos_to_slots(self, videos: List[VideoMetadata], slots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assign videos to publishing slots with optimal distribution."""
        if not videos or not slots:
            return []
        
        # Sort videos by priority (quality score, creation date)
        sorted_videos = sorted(
            videos,
            key=lambda v: (
                -(v.quality_score or 0),  # Higher quality first
                v.created_at  # Older videos first
            )
        )
        
        # Distribute videos across languages to avoid clustering
        language_distribution = {}
        assigned_slots = []
        
        for i, slot in enumerate(slots):
            if i >= len(sorted_videos):
                break
            
            video = sorted_videos[i]
            
            # Track language distribution
            lang = video.language
            language_distribution[lang] = language_distribution.get(lang, 0) + 1
            
            # Create assignment
            assignment = {
                **slot,
                "assigned_video": {
                    "video_id": f"{video.story_id}_{video.language}",
                    "title": video.title,
                    "language": video.language,
                    "duration": video.duration_seconds,
                    "quality_score": video.quality_score
                }
            }
            
            assigned_slots.append(assignment)
        
        logger.info(f"Scheduled {len(assigned_slots)} videos across {len(language_distribution)} languages")
        return assigned_slots
    
    def auto_schedule_videos(self, days_ahead: int = 14) -> bool:
        """
        Automatically schedule ready videos for publishing.
        
        Args:
            days_ahead: Days to schedule ahead
            
        Returns:
            True if successful, False otherwise
        """
        try:
            publishing_queue = self.get_publishing_queue(days_ahead)
            
            scheduled_count = 0
            for slot in publishing_queue:
                if slot["assigned_video"]:
                    video_id = slot["assigned_video"]["video_id"]
                    publish_time = slot["datetime"]
                    
                    if self.tracker.schedule_publishing(video_id, publish_time):
                        scheduled_count += 1
            
            logger.info(f"Auto-scheduled {scheduled_count} videos for publishing")
            return scheduled_count > 0
            
        except Exception as e:
            logger.error(f"Auto-scheduling failed: {e}")
            return False
    
    def get_production_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive production dashboard data."""
        summary = self.tracker.get_production_summary()
        next_batch = self.get_next_production_batch()
        publishing_queue = self.get_publishing_queue(7)  # Next week
        
        return {
            "overview": summary,
            "next_production_batch": {
                "total_videos": sum(len(videos) for videos in next_batch.values()),
                "languages": list(next_batch.keys()),
                "by_language": {lang: len(videos) for lang, videos in next_batch.items()}
            },
            "publishing_schedule": {
                "total_scheduled": len([s for s in publishing_queue if s["assigned_video"]]),
                "next_7_days": len(publishing_queue),
                "by_date": self._group_schedule_by_date(publishing_queue)
            },
            "production_config": self.config,
            "last_updated": datetime.now().isoformat()
        }
    
    def _group_schedule_by_date(self, schedule: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group scheduled videos by date."""
        by_date = {}
        for slot in schedule:
            if slot["assigned_video"]:
                date_str = slot["date"].strftime("%Y-%m-%d")
                by_date[date_str] = by_date.get(date_str, 0) + 1
        return by_date
    
    def export_batch_report(self) -> str:
        """Export detailed batch production report."""
        dashboard = self.get_production_dashboard()
        
        report = f"""
# Video Production Batch Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Production Overview
- Total Videos in Pipeline: {dashboard['overview']['total_videos']}
- Ready for Production: {dashboard['next_production_batch']['total_videos']}
- Ready to Publish: {dashboard['overview']['ready_to_publish']}
- Scheduled for Next 7 Days: {dashboard['publishing_schedule']['total_scheduled']}

## Next Production Batch
"""
        
        next_batch = self.get_next_production_batch()
        for lang, videos in next_batch.items():
            report += f"\n### {lang.upper()} - {len(videos)} videos\n"
            for video in videos:
                duration = f"{video.duration_seconds}s" if video.duration_seconds else "Unknown"
                report += f"- {video.title} ({duration})\n"
        
        # Publishing schedule
        if dashboard['publishing_schedule']['by_date']:
            report += f"\n## Publishing Schedule (Next 7 Days)\n"
            for date, count in dashboard['publishing_schedule']['by_date'].items():
                report += f"- {date}: {count} videos\n"
        
        # Configuration
        report += f"\n## Production Configuration\n"
        report += f"- Batch Size: {self.config['batch_size']}\n"
        report += f"- Daily Upload Limit: {self.config['daily_upload_limit']}\n"
        report += f"- Language Priority: {', '.join(self.config['languages_priority'])}\n"
        report += f"- Upload Hours: {self.config['upload_schedule']['start_hour']}:00 - {self.config['upload_schedule']['end_hour']}:00\n"
        
        return report