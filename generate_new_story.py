"""
Generate a new story from an unused learning in the database.
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.llm_tools import generate_story_from_learning

def load_learnings():
    """Load all learnings from the JSONL file."""
    learnings = []
    learnings_file = Path("data/learnings/learnings.jsonl")
    
    with open(learnings_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                learnings.append(json.loads(line))
    
    return learnings

def get_used_learning_ids():
    """Check which learnings have already been used for story generation."""
    used_ids = set()
    stories_dir = Path("data/stories")
    
    # Check all story JSON files
    for story_file in stories_dir.rglob("*.json"):
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
                if 'source_learning_id' in story_data:
                    used_ids.add(story_data['source_learning_id'])
        except Exception as e:
            print(f"Warning: Could not read {story_file}: {e}")
    
    return used_ids

def main():
    print("=" * 60)
    print("GENERATING NEW STORY FROM LEARNING")
    print("=" * 60)
    
    # Load all learnings
    learnings = load_learnings()
    print(f"\n✓ Loaded {len(learnings)} learnings from database")
    
    # Check which learnings have been used
    used_ids = get_used_learning_ids()
    print(f"✓ Found {len(used_ids)} learnings already used for stories")
    
    # Find unused learnings
    unused_learnings = [l for l in learnings if l['id'] not in used_ids]
    
    if not unused_learnings:
        print("\n❌ No unused learnings available!")
        print("All learnings have been used for story generation.")
        return
    
    print(f"\n✓ Found {len(unused_learnings)} unused learnings available\n")
    
    # Display unused learnings
    print("AVAILABLE LEARNINGS:")
    print("-" * 60)
    for i, learning in enumerate(unused_learnings, 1):
        print(f"\n{i}. ID: {learning['id']}")
        print(f"   Chapter: {learning['chapter_name']} (Verse {learning['verse_number']})")
        print(f"   Application: {learning['practical_application'][:80]}...")
        print(f"   Themes: {learning['main_themes']}")
        print(f"   Audience: {', '.join(learning['audience_groups'])}")
    
    # Select the first unused learning (learning_2_1)
    selected_learning = unused_learnings[0]
    print(f"\n{'=' * 60}")
    print(f"SELECTED LEARNING: {selected_learning['id']}")
    print(f"{'=' * 60}")
    print(f"Chapter: {selected_learning['chapter_name']}")
    print(f"Application: {selected_learning['practical_application']}")
    print(f"Themes: {selected_learning['main_themes']}")
    print(f"\nGenerating story...\n")
    
    # Generate the story
    try:
        story_data = generate_story_from_learning(selected_learning)
        
        # Save the story
        output_dir = Path("data/stories/en")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename from title
        filename = story_data['title'].lower()
        filename = filename.replace(" ", "_").replace(":", "").replace("?", "")
        filename = ''.join(c for c in filename if c.isalnum() or c in ['_', '-'])
        filename = f"{filename}_en.json"
        
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'=' * 60}")
        print(f"✅ STORY GENERATED SUCCESSFULLY!")
        print(f"{'=' * 60}")
        print(f"\nTitle: {story_data['title']}")
        print(f"YouTube Title: {story_data['youtube_title']}")
        print(f"Duration: {story_data['estimated_duration']} seconds")
        print(f"Category: {story_data['category']}")
        print(f"Output: {output_path}")
        print(f"\nGeneration Cost: ${story_data['generation_metadata']['total_cost']:.5f}")
        print(f"Model: {story_data['generation_metadata']['model_used']}")
        
        print(f"\n{'=' * 60}")
        print("NEXT STEPS:")
        print("1. Review the generated story")
        print("2. Translate to other languages if needed")
        print("3. Generate video using video production tools")
        print("4. Create thumbnail")
        print("5. Upload to YouTube")
        print(f"{'=' * 60}")
        
    except Exception as e:
        print(f"\n❌ Error generating story: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
