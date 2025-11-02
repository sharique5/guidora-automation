# Video Production Management System - Quick Start Guide

## 🎬 Overview
The video production management system provides comprehensive tracking and batch management for your multi-language Instadoodle video creation workflow.

## 📁 Directory Structure
```
data/
├── videos/
│   ├── production/       # Active video files by language (en, es, fr, ur)
│   ├── drafts/          # Work-in-progress videos
│   └── published/       # Completed, uploaded videos
├── thumbnails/          # Generated thumbnails by language
└── video_tracker.json  # Production database (auto-generated)
```

## 🛠️ Command Line Interface

### Basic Commands
```bash
# Check production status
python scripts/video_manager.py status

# Register translated stories for video production
python scripts/video_manager.py register

# Get next production batch
python scripts/video_manager.py batch

# Auto-schedule videos for publishing
python scripts/video_manager.py schedule --days 14

# Export production report
python scripts/video_manager.py report --output production_report.md

# Update video status
python scripts/video_manager.py update --video-id "story_123_es" --status "video_ready"
```

## 🎯 Production Workflow

### 1. Script Registration
- Automatically detects translated stories in `data/stories/`
- Registers each story/language combination as a video project
- Status: `script_ready`

### 2. Batch Production (Instadoodle)
- Get next batch: `python scripts/video_manager.py batch`
- Create videos manually in Instadoodle using the translated scripts
- Update status to `in_production` → `video_ready`

### 3. Asset Completion
- Add thumbnails to appropriate directories
- Update status to `thumbnail_needed` → `ready_to_publish`

### 4. Publishing Schedule
- Auto-schedule: `python scripts/video_manager.py schedule`
- Uploads distributed across languages and time slots
- Status: `scheduled` → `published`

## 📊 Video Status Lifecycle
1. `script_ready` - Translated script available
2. `in_production` - Being created in Instadoodle
3. `video_ready` - Video file completed
4. `thumbnail_needed` - Video done, needs thumbnail
5. `ready_to_publish` - All assets complete
6. `scheduled` - Scheduled for upload
7. `published` - Live on YouTube
8. `failed` - Production failed

## ⚙️ Configuration

### Production Settings (`config/production_config.json`)
```json
{
  "batch_size": 5,
  "languages_priority": ["en", "es", "fr", "ur"],
  "daily_upload_limit": 2,
  "upload_schedule": {
    "start_hour": 10,
    "end_hour": 18,
    "days_of_week": [1, 2, 3, 4, 5]
  }
}
```

### Quality Thresholds
- Minimum duration: 60 seconds
- Maximum duration: 300 seconds (5 minutes)
- Minimum readability score: 8/10
- Required assets: script, video, thumbnail

## 🎨 Instadoodle Integration

### Recommended Workflow
1. Get batch: `python scripts/video_manager.py batch`
2. Mark as in production (CLI prompt)
3. For each video in batch:
   - Open Instadoodle
   - Create new whiteboard explainer project
   - Copy script from registered file path
   - Create video following script pacing (10-15 words per scene)
   - Export as MP4 (1920x1080)
   - Save to `data/videos/production/{language}/`
   - Update status: `python scripts/video_manager.py update --video-id "{story_id}_{lang}" --status "video_ready"`

### Script Optimization for Instadoodle
- Short sentences (10-15 words) for visual pacing
- Clear emotional beats for drawing emphasis
- Cultural expressions for authentic narration
- Conversational tone optimized for voice-over

## 📈 Monitoring & Reports

### Daily Monitoring
```bash
# Check status
python scripts/video_manager.py status

# Get production report
python scripts/video_manager.py report
```

### Key Metrics
- Videos in pipeline by status
- Production batch readiness
- Publishing schedule for next 7 days
- Language distribution and priority

## 🚀 Next Steps
1. Create videos for current batch (3 ready: ES, FR, UR)
2. Add thumbnail generation system
3. Integrate YouTube API for automated uploads
4. Add analytics tracking for published videos

## 💡 Tips
- Use `register` command after translating new stories
- Process batches by language priority for efficiency
- Schedule uploads during optimal hours (10 AM - 6 PM)
- Monitor quality scores to maintain content standards