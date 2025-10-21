#!/usr/bin/env python3
"""
Audio Generator Script for Guidora Stories
Converts JSONL stories to high-quality audio files for YouTube uploads
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Add lib to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lib.tts_manager import create_default_tts_manager, TTSManager
from lib.jsonl_utils import load_jsonl, save_jsonl

class AudioGenerator:
    """Orchestrates the conversion of stories to audio files for the weekly pipeline."""
    
    def __init__(self, 
                 stories_file: str = "data/videos/videos.jsonl",
                 audio_output_dir: str = "data/audio",
                 target_audience: str = "universal"):
        
        self.stories_file = stories_file
        self.audio_output_dir = Path(audio_output_dir)
        self.target_audience = target_audience
        
        # Ensure output directory exists
        self.audio_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("audio_generator")
        
        # Initialize TTS manager
        self.tts_manager = create_default_tts_manager()
        
        self.logger.info(f"Audio Generator initialized")
        self.logger.info(f"Stories: {self.stories_file}")
        self.logger.info(f"Output: {self.audio_output_dir}")
        self.logger.info(f"Audience: {self.target_audience}")
    
    def process_all_stories(self, 
                           force_regenerate: bool = False,
                           preferred_provider: Optional[str] = None) -> Dict:
        """Process all stories in the JSONL file and generate audio."""
        
        self.logger.info("🎵 Starting audio generation pipeline")
        
        # Load stories
        try:
            stories = load_jsonl(self.stories_file)
            self.logger.info(f"Loaded {len(stories)} stories from {self.stories_file}")
        except Exception as e:
            self.logger.error(f"Failed to load stories: {e}")
            return {"error": str(e)}
        
        # Filter stories that need audio
        stories_to_process = self._filter_stories_for_processing(stories, force_regenerate)
        
        if not stories_to_process:
            self.logger.info("No stories need audio generation")
            return {"processed": 0, "skipped": len(stories)}
        
        self.logger.info(f"Processing {len(stories_to_process)} stories")
        
        # Process each story
        results = {
            "processed": 0,
            "failed": 0,
            "skipped": len(stories) - len(stories_to_process),
            "total_cost": 0.0,
            "total_duration": 0.0,
            "files_generated": [],
            "errors": []
        }
        
        for i, story in enumerate(stories_to_process, 1):
            story_id = story.get('id', f'story_{i}')
            
            self.logger.info(f"[{i}/{len(stories_to_process)}] Processing story: {story_id}")
            
            try:
                audio_file = self.tts_manager.generate_audio(
                    story=story,
                    audience=self.target_audience,
                    preferred_provider=preferred_provider
                )
                
                if audio_file:
                    # Save audio file to disk
                    saved_path = self._save_audio_file(audio_file, story_id)
                    
                    # Update story with audio metadata
                    self._update_story_audio_metadata(story, audio_file, saved_path)
                    
                    results["processed"] += 1
                    results["total_cost"] += audio_file.generation_cost
                    results["total_duration"] += audio_file.duration_seconds
                    results["files_generated"].append(saved_path)
                    
                    self.logger.info(f"✅ Generated audio: {saved_path}")
                else:
                    results["failed"] += 1
                    results["errors"].append(f"Audio generation failed for {story_id}")
                    self.logger.error(f"❌ Failed to generate audio for {story_id}")
                    
            except Exception as e:
                results["failed"] += 1
                error_msg = f"Error processing {story_id}: {str(e)}"
                results["errors"].append(error_msg)
                self.logger.error(error_msg)
        
        # Save updated stories back to JSONL
        try:
            save_jsonl(stories, self.stories_file)
            self.logger.info(f"Updated stories saved to {self.stories_file}")
        except Exception as e:
            self.logger.error(f"Failed to save updated stories: {e}")
        
        # Log final results
        self._log_generation_results(results)
        
        return results
    
    def _filter_stories_for_processing(self, stories: List[Dict], force_regenerate: bool) -> List[Dict]:
        """Filter stories that need audio generation."""
        
        if force_regenerate:
            return stories
        
        # Only process stories without audio or with failed audio
        stories_to_process = []
        
        for story in stories:
            audio_metadata = story.get('audio', {})
            
            # Check if audio exists and is valid
            if not audio_metadata:
                stories_to_process.append(story)
                continue
            
            audio_file_path = audio_metadata.get('file_path')
            if not audio_file_path or not os.path.exists(audio_file_path):
                stories_to_process.append(story)
                continue
            
            # Check if audio generation failed previously
            if audio_metadata.get('status') == 'failed':
                stories_to_process.append(story)
                continue
            
            # Story has valid audio, skip
            self.logger.debug(f"Skipping {story.get('id', 'unknown')}: audio exists")
        
        return stories_to_process
    
    def _save_audio_file(self, audio_file, story_id: str) -> str:
        """Save audio file to disk and return the path."""
        
        # The audio file is already saved by the TTS provider
        # Just return the path that was created by the provider
        if hasattr(audio_file, 'file_path') and audio_file.file_path:
            return audio_file.file_path
        
        # Fallback: if no file_path, the TTS provider didn't save it properly
        self.logger.error(f"Audio file for {story_id} has no file_path")
        return ""
    
    def _update_story_audio_metadata(self, story: Dict, audio_file, saved_path: str):
        """Update story with audio generation metadata."""
        
        story['audio'] = {
            "file_path": saved_path,
            "status": "completed",
            "duration_seconds": audio_file.duration_seconds,
            "file_size_bytes": audio_file.file_size_bytes,
            "provider": audio_file.provider,
            "voice_used": audio_file.voice_used,
            "generation_cost": audio_file.generation_cost,
            "sample_rate": audio_file.sample_rate,
            "created_at": audio_file.created_at.isoformat(),
            "audience": self.target_audience
        }
        
        # Update processing status
        if 'processing' not in story:
            story['processing'] = {}
        
        story['processing']['audio_generated'] = True
        story['processing']['audio_generated_at'] = datetime.now().isoformat()
    
    def _log_generation_results(self, results: Dict):
        """Log comprehensive results of the audio generation process."""
        
        self.logger.info("🎵 Audio Generation Complete!")
        self.logger.info("=" * 50)
        self.logger.info(f"✅ Processed: {results['processed']} stories")
        self.logger.info(f"❌ Failed: {results['failed']} stories")
        self.logger.info(f"⏭️ Skipped: {results['skipped']} stories")
        self.logger.info(f"💰 Total cost: ${results['total_cost']:.4f}")
        self.logger.info(f"⏱️ Total duration: {results['total_duration']:.1f} seconds")
        
        if results['files_generated']:
            self.logger.info(f"📁 Generated files:")
            for file_path in results['files_generated']:
                self.logger.info(f"   {file_path}")
        
        if results['errors']:
            self.logger.warning(f"⚠️ Errors encountered:")
            for error in results['errors']:
                self.logger.warning(f"   {error}")
        
        # Show TTS usage statistics
        stats = self.tts_manager.get_usage_stats()
        self.logger.info(f"\n📊 TTS Provider Usage:")
        for provider, usage in stats['provider_usage'].items():
            if usage['requests'] > 0:
                self.logger.info(f"   {provider}: {usage['requests']} requests, ${usage['cost']:.4f}, {usage['duration']:.1f}s")
    
    def get_audio_summary(self) -> Dict:
        """Get summary of all audio files for the current batch."""
        
        try:
            stories = load_jsonl(self.stories_file)
        except Exception as e:
            return {"error": f"Cannot load stories: {e}"}
        
        summary = {
            "total_stories": len(stories),
            "with_audio": 0,
            "without_audio": 0,
            "failed_audio": 0,
            "total_duration": 0.0,
            "total_cost": 0.0,
            "audio_files": []
        }
        
        for story in stories:
            audio_metadata = story.get('audio', {})
            
            if not audio_metadata:
                summary['without_audio'] += 1
                continue
            
            if audio_metadata.get('status') == 'failed':
                summary['failed_audio'] += 1
                continue
            
            if audio_metadata.get('status') == 'completed':
                summary['with_audio'] += 1
                summary['total_duration'] += audio_metadata.get('duration_seconds', 0)
                summary['total_cost'] += audio_metadata.get('generation_cost', 0)
                
                summary['audio_files'].append({
                    "story_id": story.get('id'),
                    "title": story.get('title', 'Untitled'),
                    "duration": audio_metadata.get('duration_seconds', 0),
                    "provider": audio_metadata.get('provider'),
                    "file_path": audio_metadata.get('file_path')
                })
        
        return summary

def main():
    """Command-line interface for audio generation."""
    
    parser = argparse.ArgumentParser(description="Generate audio from Guidora stories")
    parser.add_argument("--stories", default="data/videos/videos.jsonl", 
                       help="Path to stories JSONL file")
    parser.add_argument("--output", default="data/audio", 
                       help="Output directory for audio files")
    parser.add_argument("--audience", default="universal", 
                       choices=["universal", "muslim_community", "spiritual_seekers"],
                       help="Target audience for voice selection")
    parser.add_argument("--provider", 
                       choices=["openai", "google", "elevenlabs"],
                       help="Preferred TTS provider")
    parser.add_argument("--force", action="store_true",
                       help="Force regeneration of existing audio files")
    parser.add_argument("--summary", action="store_true",
                       help="Show audio summary instead of generating")
    
    args = parser.parse_args()
    
    generator = AudioGenerator(
        stories_file=args.stories,
        audio_output_dir=args.output,
        target_audience=args.audience
    )
    
    if args.summary:
        summary = generator.get_audio_summary()
        print("\n🎵 Audio Generation Summary")
        print("=" * 40)
        print(f"Total stories: {summary['total_stories']}")
        print(f"With audio: {summary['with_audio']}")
        print(f"Without audio: {summary['without_audio']}")
        print(f"Failed audio: {summary['failed_audio']}")
        print(f"Total duration: {summary['total_duration']:.1f} seconds")
        print(f"Total cost: ${summary['total_cost']:.4f}")
        
        if summary['audio_files']:
            print(f"\n📁 Audio Files:")
            for audio in summary['audio_files']:
                print(f"   {audio['story_id']}: {audio['duration']:.1f}s ({audio['provider']})")
    else:
        results = generator.process_all_stories(
            force_regenerate=args.force,
            preferred_provider=args.provider
        )
        
        if results.get('error'):
            print(f"❌ Error: {results['error']}")
            sys.exit(1)
        else:
            print(f"\n✅ Audio generation completed!")
            print(f"Processed: {results['processed']}, Failed: {results['failed']}, Skipped: {results['skipped']}")

if __name__ == "__main__":
    main()