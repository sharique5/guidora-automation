#!/usr/bin/env python3
"""
YouTube Shorts Generator - Create 30-60 second vertical shorts from stories
Generates multiple short variants: Hook, Wisdom, and optional Crisis

Usage:
    python generate_shorts.py <story_id>
    python generate_shorts.py youtube_optimized_learning_4_1_91b588ac_7ac9e43b
    
    # Generate specific type only
    python generate_shorts.py <story_id> --type hook
    python generate_shorts.py <story_id> --type wisdom
    python generate_shorts.py <story_id> --type crisis
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import hashlib

# Add lib to path
sys.path.append(str(Path(__file__).parent / "lib"))
from llm_tools import create_default_manager

# Import centralized utilities
sys.path.append(str(Path(__file__).parent))
from config.paths import PROMPTS_DIR, STORY_DIRS, DEFAULT_MODELS
from lib.story_utils import find_story, save_story

# Short type definitions
SHORT_TYPES = {
    'hook': {
        'name': 'Hook/Teaser',
        'description': 'Creates maximum curiosity - teases the story without revealing outcome',
        'instructions': """
HOOK/TEASER SHORT:
Your goal: Make them NEED to watch the full video.

Structure:
- 0-3 sec: Shocking moment/question
- 3-20 sec: Build the problem/crisis (but DON'T resolve it)
- 20-25 sec: Hint at what's coming ("But then...")
- 25-30 sec: CLIFFHANGER + CTA to full video

Key principle: MAXIMUM CURIOSITY GAP
- Show the stakes
- Show the crisis
- DON'T show the solution
- End on "You won't believe what happened next..."

This Short's job: Drive traffic TO the long-form video.
"""
    },
    'wisdom': {
        'name': 'Wisdom/Insight',
        'description': 'Delivers the key lesson - standalone value that makes them follow for more',
        'instructions': """
WISDOM/INSIGHT SHORT:
Your goal: Deliver IMMEDIATE value. Make them think "I need more of this."

Structure:
- 0-3 sec: The insight/lesson stated boldly
- 3-15 sec: Quick story context (why it matters)
- 15-40 sec: The transformation/application
- 40-45 sec: Powerful closing + CTA

Key principle: STANDALONE VALUE
- They should learn something even without full video
- The insight should be memorable
- Make them want to save/share
- End with "More stories like this in my videos"

This Short's job: Build authority + followers.
"""
    },
    'crisis': {
        'name': 'Crisis/Dramatic',
        'description': 'The most intense moment - pure emotion and tension',
        'instructions': """
CRISIS/DRAMATIC SHORT:
Your goal: Maximum emotional impact. Make them FEEL it.

Structure:
- 0-3 sec: Drop into the crisis moment
- 3-25 sec: Build the emotional intensity
- 25-40 sec: The turning point/realization
- 40-45 sec: Emotional resolution + CTA

Key principle: EMOTION OVER EXPLANATION
- Focus on feelings, not facts
- Use powerful imagery
- Short, punchy sentences
- Music is key here
- End with "Full story will make you cry - link in bio"

This Short's job: Viral potential through emotion.
"""
    }
}

def generate_short(story_data: dict, short_type: str) -> tuple:
    """
    Generate a YouTube Short script from a story.
    
    Args:
        story_data: The full story data
        short_type: Type of short ('hook', 'wisdom', 'crisis')
    
    Returns:
        Tuple of (short_content, cost)
    """
    story_content = story_data.get('story_content', '')
    
    if not story_content:
        print(f"❌ No story content found!")
        return None, 0.0
    
    # Load prompt template
    prompt_file = PROMPTS_DIR / "short_script_youtube.txt"
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    # Get short type info
    type_info = SHORT_TYPES[short_type]
    
    # Fill in prompt
    prompt = prompt_template.replace("{short_type}", type_info['name'])
    prompt = prompt.replace("{short_type_instructions}", type_info['instructions'])
    prompt = prompt.replace("{story_content}", story_content)
    
    # Generate short
    llm = create_default_manager()
    
    print(f"\n⏳ Generating {type_info['name']} Short...")
    response = llm.generate(prompt=prompt)
    
    print(f"   ✅ Generated (${response.cost_estimate:.4f})")
    
    return response.content, response.cost_estimate

def main():
    parser = argparse.ArgumentParser(description='Generate YouTube Shorts from stories')
    parser.add_argument('story_id', help='Story ID to generate shorts from')
    parser.add_argument('--type', choices=['hook', 'wisdom', 'crisis', 'all'], 
                       default='all', help='Type of short to generate')
    
    args = parser.parse_args()
    
    print("🎬 YOUTUBE SHORTS GENERATOR")
    print("=" * 70)
    print(f"Story ID: {args.story_id}")
    print(f"Short Type(s): {args.type}")
    print("=" * 70)
    
    # Find the story
    print(f"\n🔍 Searching for story...")
    story_file, story_data = find_story(args.story_id)
    
    if not story_data:
        print(f"❌ Story not found: {args.story_id}")
        sys.exit(1)
    
    print(f"✅ Found: {story_file}")
    
    # Determine which shorts to generate
    if args.type == 'all':
        types_to_generate = ['hook', 'wisdom']  # Generate 2 by default
    else:
        types_to_generate = [args.type]
    
    print(f"\n📹 Generating {len(types_to_generate)} Short(s):")
    for st in types_to_generate:
        print(f"   • {SHORT_TYPES[st]['name']}: {SHORT_TYPES[st]['description']}")
    
    # Generate shorts
    total_cost = 0.0
    generated_shorts = []
    
    for short_type in types_to_generate:
        print(f"\n{'=' * 70}")
        print(f"🎯 {SHORT_TYPES[short_type]['name'].upper()}")
        print(f"{'=' * 70}")
        
        short_content, cost = generate_short(story_data, short_type)
        total_cost += cost
        
        if short_content:
            # Create short data
            short_id = f"{args.story_id}_short_{short_type}_{hashlib.md5(short_content.encode()).hexdigest()[:8]}"
            
            short_data = {
                "id": short_id,
                "parent_story_id": args.story_id,
                "short_type": short_type,
                "short_type_name": SHORT_TYPES[short_type]['name'],
                "short_content": short_content,
                "format": "vertical_9_16",
                "target_duration": "30-60 seconds",
                "generation_metadata": {
                    "cost": cost,
                    "model_used": DEFAULT_MODELS['short_script'],
                    "template": "short_script_youtube"
                },
                "generated_at": datetime.now().isoformat()
            }
            
            # Save short
            shorts_dir = STORY_DIRS['youtube_optimized'].parent / "shorts"
            shorts_dir.mkdir(parents=True, exist_ok=True)
            
            short_file = shorts_dir / f"{short_id}.json"
            save_story(short_file, short_data)
            
            print(f"   💾 Saved: {short_file.name}")
            
            generated_shorts.append({
                'type': short_type,
                'file': short_file,
                'id': short_id
            })
            
            # Show preview
            print(f"\n{'─' * 70}")
            print(f"📺 PREVIEW:")
            print(f"{'─' * 70}")
            preview = short_content[:400] + "..." if len(short_content) > 400 else short_content
            print(preview)
    
    # Summary
    print(f"\n{'=' * 70}")
    print(f"✅ SHORTS GENERATION COMPLETE")
    print(f"{'=' * 70}")
    print(f"💰 Total Cost: ${total_cost:.4f}")
    print(f"📹 Generated {len(generated_shorts)} Short(s):")
    
    for short in generated_shorts:
        print(f"   • {SHORT_TYPES[short['type']]['name']}: {short['file'].name}")
    
    print(f"\n{'=' * 70}")
    print(f"NEXT STEPS:")
    print(f"1. Review shorts in: data/stories/shorts/")
    print(f"2. Create vertical videos (9:16 aspect ratio)")
    print(f"3. Add text overlays (most viewers watch muted)")
    print(f"4. Upload as YouTube Shorts")
    print(f"5. Link to full video in description")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()
