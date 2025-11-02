#!/usr/bin/env python3
"""
Video Creation and Publishing Tracker
Manages video production workflow across multiple languages and tracks publication status.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class VideoStatus(Enum):
    """Video production status stages."""
    SCRIPT_READY = "script_ready"           # Script translated and ready
    IN_PRODUCTION = "in_production"         # Being created in Instadoodle
    VIDEO_READY = "video_ready"             # Video file ready for upload
    THUMBNAIL_NEEDED = "thumbnail_needed"   # Video ready, thumbnail missing
    READY_TO_PUBLISH = "ready_to_publish"   # All assets ready
    SCHEDULED = "scheduled"                 # Scheduled for publishing
    PUBLISHED = "published"                 # Live on YouTube
    FAILED = "failed"                       # Production failed

class Language(Enum):
    """Supported languages."""
    ENGLISH = "en"
    SPANISH = "es" 
    FRENCH = "fr"
    URDU = "ur"

@dataclass
class VideoMetadata:
    """Video metadata and tracking information."""
    story_id: str
    title: str
    language: str
    status: VideoStatus
    created_at: str
    updated_at: str
    
    # File paths
    script_path: Optional[str] = None
    video_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    
    # Production details
    duration_seconds: Optional[int] = None
    file_size_mb: Optional[float] = None
    instadoodle_project_id: Optional[str] = None
    
    # YouTube details
    youtube_video_id: Optional[str] = None
    youtube_title: Optional[str] = None
    youtube_description: Optional[str] = None
    youtube_tags: Optional[List[str]] = None
    scheduled_publish_time: Optional[str] = None
    actual_publish_time: Optional[str] = None
    
    # Analytics
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    last_analytics_update: Optional[str] = None
    
    # Production notes
    notes: Optional[str] = None
    quality_score: Optional[float] = None

class VideoTracker:
    """Manages video production workflow and status tracking."""
    
    def __init__(self, base_path: str = None):
        """Initialize video tracker."""
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent.parent
        self.data_path = self.base_path / "data"
        self.videos_path = self.data_path / "videos"
        self.tracker_file = self.data_path / "video_tracker.json"
        
        # Ensure directories exist
        self.videos_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing tracker data
        self.videos: Dict[str, VideoMetadata] = self._load_tracker_data()
    
    def _load_tracker_data(self) -> Dict[str, VideoMetadata]:
        """Load video tracking data from JSON file."""
        if not self.tracker_file.exists():
            return {}
        
        try:
            with open(self.tracker_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            videos = {}
            for video_id, video_data in data.items():
                # Convert status string back to enum
                video_data['status'] = VideoStatus(video_data['status'])
                videos[video_id] = VideoMetadata(**video_data)
                
            return videos
            
        except Exception as e:
            logger.error(f"Failed to load tracker data: {e}")
            return {}
    
    def _save_tracker_data(self):
        """Save video tracking data to JSON file."""
        try:
            # Convert VideoMetadata objects to dictionaries
            data = {}
            for video_id, video_meta in self.videos.items():
                video_dict = asdict(video_meta)
                # Convert enum to string
                video_dict['status'] = video_meta.status.value
                data[video_id] = video_dict
            
            with open(self.tracker_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to save tracker data: {e}")
    
    def register_script(self, story_id: str, language: str, script_path: str, 
                       title: str, duration_seconds: int = None) -> str:
        """Register a new translated script ready for video production."""
        video_id = f"{story_id}_{language}"
        
        video_meta = VideoMetadata(
            story_id=story_id,
            title=title,
            language=language,
            status=VideoStatus.SCRIPT_READY,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            script_path=script_path,
            duration_seconds=duration_seconds
        )
        
        self.videos[video_id] = video_meta
        self._save_tracker_data()
        
        logger.info(f"Registered script for {video_id}: {title}")
        return video_id
    
    def update_status(self, video_id: str, status: VideoStatus, **kwargs):
        """Update video status and optional metadata."""
        if video_id not in self.videos:
            raise ValueError(f"Video {video_id} not found in tracker")
        
        video_meta = self.videos[video_id]
        video_meta.status = status
        video_meta.updated_at = datetime.now().isoformat()
        
        # Update any additional metadata
        for key, value in kwargs.items():
            if hasattr(video_meta, key):
                setattr(video_meta, key, value)
        
        self._save_tracker_data()
        logger.info(f"Updated {video_id} status to {status.value}")
    
    def get_videos_by_status(self, status: VideoStatus) -> List[VideoMetadata]:
        """Get all videos with specific status."""
        return [video for video in self.videos.values() if video.status == status]
    
    def get_videos_by_language(self, language: str) -> List[VideoMetadata]:
        """Get all videos for specific language."""
        return [video for video in self.videos.values() if video.language == language]
    
    def get_next_production_batch(self, batch_size: int = 5) -> List[VideoMetadata]:
        """Get next batch of videos ready for production."""
        ready_scripts = self.get_videos_by_status(VideoStatus.SCRIPT_READY)
        
        # Sort by creation date (oldest first)
        ready_scripts.sort(key=lambda v: v.created_at)
        
        return ready_scripts[:batch_size]
    
    def get_ready_to_publish_videos(self) -> List[VideoMetadata]:
        """Get videos ready for publishing."""
        return self.get_videos_by_status(VideoStatus.READY_TO_PUBLISH)
    
    def get_production_summary(self) -> Dict[str, Any]:
        """Get summary of video production pipeline."""
        summary = {
            'total_videos': len(self.videos),
            'by_status': {},
            'by_language': {},
            'next_batch_ready': len(self.get_next_production_batch()),
            'ready_to_publish': len(self.get_ready_to_publish_videos())
        }
        
        # Count by status
        for status in VideoStatus:
            count = len(self.get_videos_by_status(status))
            summary['by_status'][status.value] = count
        
        # Count by language
        for language in Language:
            count = len(self.get_videos_by_language(language.value))
            summary['by_language'][language.value] = count
        
        return summary
    
    def schedule_publishing(self, video_id: str, publish_time: datetime) -> bool:
        """Schedule video for publishing at specific time."""
        if video_id not in self.videos:
            return False
        
        video_meta = self.videos[video_id]
        
        if video_meta.status != VideoStatus.READY_TO_PUBLISH:
            logger.warning(f"Video {video_id} not ready for publishing (status: {video_meta.status})")
            return False
        
        video_meta.scheduled_publish_time = publish_time.isoformat()
        video_meta.status = VideoStatus.SCHEDULED
        video_meta.updated_at = datetime.now().isoformat()
        
        self._save_tracker_data()
        logger.info(f"Scheduled {video_id} for publishing at {publish_time}")
        return True
    
    def get_publishing_schedule(self, days_ahead: int = 7) -> List[VideoMetadata]:
        """Get videos scheduled for publishing in next N days."""
        end_date = datetime.now() + timedelta(days=days_ahead)
        
        scheduled_videos = []
        for video in self.get_videos_by_status(VideoStatus.SCHEDULED):
            if video.scheduled_publish_time:
                scheduled_time = datetime.fromisoformat(video.scheduled_publish_time)
                if scheduled_time <= end_date:
                    scheduled_videos.append(video)
        
        # Sort by scheduled time
        scheduled_videos.sort(key=lambda v: v.scheduled_publish_time)
        return scheduled_videos
    
    def export_production_report(self) -> str:
        """Export detailed production report."""
        summary = self.get_production_summary()
        next_batch = self.get_next_production_batch()
        ready_to_publish = self.get_ready_to_publish_videos()
        upcoming_schedule = self.get_publishing_schedule()
        
        report = f"""
# Video Production Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
- Total Videos: {summary['total_videos']}
- Next Production Batch Ready: {summary['next_batch_ready']}
- Ready to Publish: {summary['ready_to_publish']}

## Status Breakdown
"""
        for status, count in summary['by_status'].items():
            report += f"- {status.replace('_', ' ').title()}: {count}\n"
        
        report += f"\n## Language Distribution\n"
        for language, count in summary['by_language'].items():
            report += f"- {language.upper()}: {count}\n"
        
        if next_batch:
            report += f"\n## Next Production Batch ({len(next_batch)} videos)\n"
            for video in next_batch:
                report += f"- {video.language.upper()}: {video.title}\n"
        
        if ready_to_publish:
            report += f"\n## Ready to Publish ({len(ready_to_publish)} videos)\n"
            for video in ready_to_publish:
                report += f"- {video.language.upper()}: {video.title}\n"
        
        if upcoming_schedule:
            report += f"\n## Publishing Schedule ({len(upcoming_schedule)} videos)\n"
            for video in upcoming_schedule:
                scheduled_time = datetime.fromisoformat(video.scheduled_publish_time)
                report += f"- {scheduled_time.strftime('%Y-%m-%d %H:%M')}: {video.language.upper()} - {video.title}\n"
        
        return report