#!/usr/bin/env python3
"""
Generate a HIGH-RETENTION YouTube-optimized story from learnings database.
Uses pattern interruption, curiosity-driven titles, and diverse characters.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import hashlib

# Add lib to path
sys.path.append(str(Path(__file__).parent / "lib"))
from llm_tools import create_default_manager

# Import centralized utilities
sys.path.append(str(Path(__file__).parent))
from config.paths import LEARNINGS_FILE, STORY_DIRS, PROMPTS, OPTIMIZATION_FEATURES
from lib.story_utils import extract_used_characters, get_character_exclusion_text, get_story_count, save_story

def load_random_learning():
    """Load a random unused learning from the database."""
    with open(LEARNINGS_FILE, 'r', encoding='utf-8') as f:
        learnings = [json.loads(line) for line in f if line.strip()]
    
    # Get next unused learning based on story count
    story_count = get_story_count()
    
    # Use different learning each time
    learning_index = min(story_count, len(learnings) - 1)
    return learnings[learning_index] if learnings else None

def generate_youtube_optimized_story():
    """Generate story with YouTube optimization principles."""
    
    print("🎬 GENERATING YOUTUBE-OPTIMIZED STORY")
    print("Using: Pattern Interruption + Curiosity-Driven Titles + Diverse Characters")
    print("=" * 70)
    
    # Load learning
    learning = load_random_learning()
    if not learning:
        print("❌ No learnings found!")
        return
    
    print(f"\n📚 Learning Source:")
    print(f"   ID: {learning['id']}")
    print(f"   Practical Application: {learning['practical_application'][:80]}...")
    
    # Load the YouTube-optimized prompt
    with open(PROMPTS['story_youtube_optimized'], 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    # Fill in the practical application
    story_prompt = prompt_template.replace("{practical_application}", learning['practical_application'])
    
    # Check for used characters
    used_chars = extract_used_characters()
    
    print(f"\n🎯 Generating with YouTube Best Practices:")
    print(f"   ✓ Hook with pattern interruption (first 3 seconds)")
    print(f"   ✓ Curiosity-driven title (tension + stakes)")
    print(f"   ✓ Diverse character backgrounds")
    print(f"   ✓ Crisis point (not just challenges)")
    print(f"   ✓ Retention hooks throughout")
    
    if used_chars:
        print(f"\n⚠️  Characters already used (MUST use different):")
        for char in used_chars:
            print(f"   ❌ {char}")
        
        # Add exclusion to prompt using utility function
        story_prompt = story_prompt + get_character_exclusion_text(used_chars)
    
    # Generate story
    llm = create_default_manager()
    
    print(f"\n⏳ Generating story...")
    story_response = llm.generate(prompt=story_prompt)
    
    story_content = story_response.content
    story_cost = story_response.cost_estimate
    
    print(f"   ✅ Story generated (${story_cost:.4f})")
    
    # Generate YouTube metadata
    with open(PROMPTS['metadata_youtube_optimized'], 'r', encoding='utf-8') as f:
        metadata_template = f.read()
    
    metadata_prompt = metadata_template.replace("{story_content}", story_content)
    
    print(f"\n⏳ Generating YouTube metadata...")
    metadata_response = llm.generate(prompt=metadata_prompt)
    
    metadata_content = metadata_response.content
    metadata_cost = metadata_response.cost_estimate
    
    print(f"   ✅ Metadata generated (${metadata_cost:.4f})")
    
    # Save the story
    story_id = f"youtube_optimized_{learning['id']}_{hashlib.md5(story_content.encode()).hexdigest()[:8]}"
    
    story_data = {
        "id": story_id,
        "source_learning_id": learning['id'],
        "story_content": story_content,
        "youtube_metadata": metadata_content,
        "generation_metadata": {
            "story_cost": story_cost,
            "metadata_cost": metadata_cost,
            "total_cost": story_cost + metadata_cost,
            "model_used": "gpt-4-turbo",
            "template": "youtube_optimized",
            "optimization_features": OPTIMIZATION_FEATURES
        },
        "generated_at": datetime.now().isoformat()
    }
    
    # Save to file using utility function
    output_dir = STORY_DIRS['youtube_optimized']
    output_file = output_dir / f"{story_id}.json"
    save_story(output_file, story_data)
    
    print(f"\n💾 Saved to: {output_file}")
    print(f"\n{'=' * 70}")
    print(f"📊 GENERATION COMPLETE")
    print(f"{'=' * 70}")
    print(f"💰 Total Cost: ${story_cost + metadata_cost:.4f}")
    print(f"📝 Story ID: {story_id}")
    
    # Display preview
    print(f"\n{'=' * 70}")
    print(f"📺 STORY PREVIEW")
    print(f"{'=' * 70}")
    print(story_content[:500] + "...")
    
    print(f"\n{'=' * 70}")
    print(f"🎯 YOUTUBE METADATA PREVIEW")
    print(f"{'=' * 70}")
    print(metadata_content[:500] + "...")
    
    print(f"\n{'=' * 70}")
    print(f"NEXT STEPS:")
    print(f"1. Review the full story in: {output_file}")
    print(f"2. Check if title creates curiosity gap (not just describes)")
    print(f"3. Verify hook interrupts pattern in first 3 seconds")
    print(f"4. Confirm diverse character background")
    print(f"5. Translate to 4 languages")
    print(f"6. Generate YouTube-optimized thumbnail")
    print(f"7. Create video and publish")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    generate_youtube_optimized_story()
