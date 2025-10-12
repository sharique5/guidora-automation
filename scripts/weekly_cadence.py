#!/usr/bin/env python3
"""
Weekly Cadence Manager for Guidora Automation
Processes content in manageable weekly chunks
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
from learning_extractor import LearningExtractor
from story_generator import StoryGenerator

class WeeklyCadenceManager:
    """Manages weekly processing of content generation."""
    
    def __init__(self):
        self.state_file = "data/weekly_state.json"
        self.verses_per_week = 200  # Configurable batch size
        self.load_state()
    
    def load_state(self):
        """Load current processing state."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
                
            # Migrate old state format to include story generation
            if "total_stories_generated" not in self.state:
                self.state["total_stories_generated"] = 0
                print("🔄 Migrating state to include story generation tracking")
        else:
            self.state = {
                "current_week": 1,
                "last_processed_verse": 0,
                "total_learnings_generated": 0,
                "total_stories_generated": 0,
                "last_run_date": None,
                "weeks_completed": []
            }
    
    def save_state(self):
        """Save current processing state."""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def should_run_this_week(self) -> bool:
        """Check if we should run processing this week."""
        if not self.state["last_run_date"]:
            return True
        
        last_run = datetime.fromisoformat(self.state["last_run_date"])
        week_ago = datetime.now() - timedelta(days=7)
        
        return last_run < week_ago
    
    def run_weekly_processing(self):
        """Run this week's processing batch."""
        if not self.should_run_this_week():
            print("⏰ Weekly processing already completed this week")
            return
        
        print(f"🚀 Starting Week {self.state['current_week']} Processing")
        print(f"📊 Processing verses {self.state['last_processed_verse'] + 1} to {self.state['last_processed_verse'] + self.verses_per_week}")
        
        # Step 1: Learning Extraction
        print(f"\n📚 Step 1: Learning Extraction")
        extractor = LearningExtractor(
            data_file="data/tafsir/quran_filtered.jsonl",
            output_file="data/learnings/learnings.jsonl"
        )
        
        learnings = self._process_batch(extractor)
        print(f"✅ Extracted {len(learnings)} new learnings")
        
        # Step 2: Story Generation (only if we have new learnings)
        stories_generated = 0
        if learnings:
            print(f"\n🎬 Step 2: Story Generation")
            try:
                story_generator = StoryGenerator()
                
                # Generate stories for each new learning
                for learning_data in learnings:
                    try:
                        # Generate universal story
                        story = story_generator.generate_story(learning_data.__dict__ if hasattr(learning_data, '__dict__') else learning_data, target_audience='universal')
                        story_generator.save_story(story)
                        stories_generated += 1
                        print(f"   ✅ Generated story: {story.title[:50]}...")
                        
                    except Exception as e:
                        print(f"   ⚠️ Failed to generate story for learning: {e}")
                        
            except Exception as e:
                print(f"   ⚠️ Story generation not available (likely missing API key): {e}")
                print(f"   💡 Set OPENAI_API_KEY or ANTHROPIC_API_KEY to enable story generation")
        else:
            print(f"\n🎬 Step 2: Story Generation - Skipped (no new learnings)")
        
        # Update state
        self.state["last_processed_verse"] += self.verses_per_week
        self.state["total_learnings_generated"] += len(learnings)
        self.state["total_stories_generated"] += stories_generated
        self.state["last_run_date"] = datetime.now().isoformat()
        self.state["weeks_completed"].append({
            "week": self.state["current_week"],
            "learnings_extracted": len(learnings),
            "stories_generated": stories_generated,
            "date": datetime.now().isoformat()
        })
        self.state["current_week"] += 1
        
        self.save_state()
        
        print(f"\n✅ Week {self.state['current_week'] - 1} completed!")
        print(f"📈 Total learnings generated: {self.state['total_learnings_generated']}")
        print(f"🎬 Total stories generated: {self.state['total_stories_generated']}")
        print(f"📊 Pipeline: Verses → Learnings → Stories → Ready for TTS (Week 3)")
    
    def _process_batch(self, extractor: LearningExtractor) -> List:
        """Process a batch of verses."""
        # This is a simplified version - in real implementation,
        # you'd skip to the correct starting position in the file
        learnings = extractor.process_verses(limit=self.verses_per_week)
        
        if learnings:
            extractor.save_learnings(learnings)
        
        return learnings
    
    def get_progress_report(self) -> Dict:
        """Get current progress statistics."""
        total_verses = 6236  # Your total verse count
        progress_percentage = (self.state["last_processed_verse"] / total_verses) * 100
        
        estimated_weeks_remaining = max(0, 
            (total_verses - self.state["last_processed_verse"]) // self.verses_per_week
        )
        
        return {
            "current_week": self.state["current_week"],
            "verses_processed": self.state["last_processed_verse"],
            "total_verses": total_verses,
            "progress_percentage": round(progress_percentage, 1),
            "learnings_generated": self.state["total_learnings_generated"],
            "stories_generated": self.state["total_stories_generated"],
            "estimated_weeks_remaining": estimated_weeks_remaining,
            "weeks_completed": len(self.state["weeks_completed"])
        }


def main():
    """Main function for weekly cadence management."""
    print("📅 Guidora Weekly Cadence Manager")
    print("=" * 40)
    
    manager = WeeklyCadenceManager()
    
    # Show current progress
    progress = manager.get_progress_report()
    print(f"📊 Current Progress:")
    print(f"   Week: {progress['current_week']}")
    print(f"   Verses Processed: {progress['verses_processed']}/{progress['total_verses']} ({progress['progress_percentage']}%)")
    print(f"   Learnings Generated: {progress['learnings_generated']}")
    print(f"   Stories Generated: {progress['stories_generated']}")
    print(f"   Estimated Weeks Remaining: {progress['estimated_weeks_remaining']}")
    print(f"   📋 Full Pipeline: Verses → Learnings → Stories → TTS → Video → YouTube")
    
    # Run weekly processing
    manager.run_weekly_processing()


if __name__ == "__main__":
    main()