#!/usr/bin/env python3
"""
Video File Naming Convention Manager
Provides consistent, simple naming for video files based on story content and language.
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime
import hashlib

class VideoNamingManager:
    """Manages consistent video file naming across all languages."""
    
    def __init__(self, base_path: str = None):
        """Initialize naming manager."""
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent.parent
        self.stories_path = self.base_path / "data" / "stories"
        
        # Story naming mapping
        self.story_mappings = {}
        self._load_story_mappings()
    
    def _load_story_mappings(self):
        """Load and create story ID mappings from existing stories."""
        story_count = 1
        
        # Scan all language directories for unique stories
        unique_stories = set()
        
        for lang_dir in self.stories_path.iterdir():
            if lang_dir.is_dir() and lang_dir.name in ['en', 'es', 'fr', 'ur', 'ar']:
                for story_file in lang_dir.glob("*.json"):
                    # Extract base story name (remove language suffix)
                    story_name = story_file.stem
                    if story_name.endswith(f"_{lang_dir.name}"):
                        base_name = story_name[:-3]  # Remove _en, _es, etc.
                        unique_stories.add(base_name)
        
        # Create simple numeric mappings
        for story_name in sorted(unique_stories):
            story_id = f"story_{story_count:03d}"
            self.story_mappings[story_name] = story_id
            story_count += 1
    
    def get_story_id_from_filename(self, filename: str) -> str:
        """Extract story ID from filename."""
        # Remove file extension and language suffix
        base_name = Path(filename).stem
        
        # Handle both JSON and TXT files
        for suffix in ['_en', '_es', '_fr', '_ur', '_ar']:
            if base_name.endswith(suffix):
                base_name = base_name[:-3]
                break
        
        # Handle script files
        if base_name.endswith('_SCRIPT'):
            base_name = base_name[:-7]
        
        # Map to story ID or create new one
        if base_name in self.story_mappings:
            return self.story_mappings[base_name]
        else:
            # Create new mapping
            story_count = len(self.story_mappings) + 1
            story_id = f"story_{story_count:03d}"
            self.story_mappings[base_name] = story_id
            return story_id
    
    def generate_video_filename(self, story_file_path: str, language: str, 
                              include_timestamp: bool = False) -> str:
        """Generate consistent video filename."""
        story_id = self.get_story_id_from_filename(story_file_path)
        
        if include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d")
            return f"{story_id}_{language}_{timestamp}.mp4"
        else:
            return f"{story_id}_{language}.mp4"
    
    def generate_batch_filenames(self, include_timestamp: bool = False) -> Dict[str, str]:
        """Generate filenames for all stories in current batch."""
        filenames = {}
        
        for lang_dir in self.stories_path.iterdir():
            if lang_dir.is_dir() and lang_dir.name in ['en', 'es', 'fr', 'ur', 'ar']:
                language = lang_dir.name
                
                for story_file in lang_dir.glob("*.json"):
                    story_id = self.get_story_id_from_filename(str(story_file))
                    video_filename = self.generate_video_filename(
                        str(story_file), language, include_timestamp
                    )
                    
                    key = f"{story_id}_{language}"
                    filenames[key] = {
                        'video_filename': video_filename,
                        'story_id': story_id,
                        'language': language,
                        'story_file': str(story_file),
                        'video_path': f"data/videos/production/{language}/{video_filename}"
                    }
        
        return filenames
    
    def get_story_info_from_file(self, story_file_path: str) -> Dict:
        """Extract story information from JSON file."""
        try:
            with open(story_file_path, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
            
            return {
                'title': story_data.get('title', 'Unknown Title'),
                'youtube_title': story_data.get('youtube_title', story_data.get('title', '')),
                'duration': story_data.get('estimated_duration', 180),
                'description': story_data.get('description', ''),
                'generated_at': story_data.get('generated_at', ''),
                'translation_metadata': story_data.get('translation_metadata', {})
            }
        except Exception as e:
            return {'title': 'Unknown', 'duration': 180}
    
    def export_naming_reference(self) -> str:
        """Export naming reference for all stories."""
        batch_filenames = self.generate_batch_filenames(include_timestamp=False)
        
        report = """# Video File Naming Reference

## Current Story Mappings:
"""
        
        # Group by story ID
        by_story = {}
        for key, info in batch_filenames.items():
            story_id = info['story_id']
            if story_id not in by_story:
                by_story[story_id] = []
            by_story[story_id].append(info)
        
        for story_id in sorted(by_story.keys()):
            story_versions = by_story[story_id]
            
            # Get title from English version if available
            title = "Unknown Title"
            for version in story_versions:
                if version['language'] == 'en':
                    story_info = self.get_story_info_from_file(version['story_file'])
                    title = story_info['title']
                    break
            
            report += f"\n### {story_id}: {title}\n"
            
            for version in sorted(story_versions, key=lambda x: x['language']):
                lang = version['language'].upper()
                filename = version['video_filename']
                report += f"- **{lang}**: `{filename}`\n"
        
        report += f"""

## Naming Convention:
- **Pattern**: `story_XXX_<lang>.mp4`
- **story_XXX**: Sequential 3-digit story number (001, 002, etc.)
- **<lang>**: Language code (en, es, fr, ur, ar)
- **Extension**: Always .mp4

## Examples:
- `story_001_en.mp4` - English version of first story
- `story_001_es.mp4` - Spanish version of first story
- `story_002_fr.mp4` - French version of second story

## Benefits:
- ✅ Simple and predictable
- ✅ Easy to sort and organize
- ✅ Language clearly identified
- ✅ Sequential numbering for growth tracking
- ✅ No timestamp clutter (unless needed for versioning)

## File Paths:
All videos saved to: `data/videos/production/<lang>/<filename>`
"""
        
        return report

def main():
    """Demo the naming system."""
    naming_manager = VideoNamingManager()
    
    print("📁 Video File Naming System")
    print("=" * 50)
    
    # Show current mappings
    batch_filenames = naming_manager.generate_batch_filenames()
    
    print(f"📊 Found {len(batch_filenames)} videos to name:")
    
    for key, info in sorted(batch_filenames.items()):
        print(f"  {info['language'].upper()}: {info['video_filename']}")
    
    print("\n🔍 Example naming:")
    
    # Show example for seeing_signs story
    example_file = "data/stories/en/seeing_signs_a_journey_to_inner_strength_en.json"
    if Path(example_file).exists():
        story_id = naming_manager.get_story_id_from_filename(example_file)
        filename = naming_manager.generate_video_filename(example_file, "en", False)
        filename_with_date = naming_manager.generate_video_filename(example_file, "en", True)
        
        print(f"Story file: seeing_signs_a_journey_to_inner_strength_en.json")
        print(f"Story ID: {story_id}")
        print(f"Video filename (simple): {filename}")
        print(f"Video filename (with date): {filename_with_date}")
    
    # Export reference
    reference = naming_manager.export_naming_reference()
    reference_file = naming_manager.base_path / "docs" / "VIDEO_NAMING_REFERENCE.md"
    
    with open(reference_file, 'w', encoding='utf-8') as f:
        f.write(reference)
    
    print(f"\n📋 Naming reference saved to: {reference_file}")

if __name__ == "__main__":
    main()