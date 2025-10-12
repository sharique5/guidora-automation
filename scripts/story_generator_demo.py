#!/usr/bin/env python3
"""
Story Generation Demo - Shows story generation process without requiring API keys
"""

import json
import os
from datetime import datetime

def load_sample_stories():
    """Create sample stories to demonstrate the output format."""
    
    # Load our actual learnings
    with open('data/learnings/learnings.jsonl', 'r', encoding='utf-8') as f:
        learnings = [json.loads(line) for line in f if line.strip()]
    
    sample_stories = []
    
    # Sample story 1: Universal audience - Spiritual Practice
    story1 = {
        "id": "story_1_1_universal_demo001",
        "source_learning_id": learnings[0]['id'],
        "title": "The Five-Minute Morning That Changed Everything",
        "description": "A busy executive discovers how brief moments of reflection transform her entire day and relationships.",
        "content": """Maya's alarm buzzed at 5:30 AM, same as every morning for the past five years. Coffee, emails, meetings, deadlines—the cycle never stopped. But today felt different.

Yesterday, her grandmother had mentioned something simple: "Start each day by remembering what matters most." Maya had brushed it off then, but now, sitting in her kitchen before the chaos began, those words echoed.

She set down her phone and closed her eyes for just five minutes. No meditation app, no special technique—just breathing and thinking about the day ahead with intention. She thought about her team, her family, the projects that could make a real difference.

When she opened her eyes, something had shifted. The same challenges awaited, but her perspective had changed. In meetings, she found herself truly listening instead of planning her next response. During lunch, she called her grandmother instead of scrolling social media.

That evening, her daughter noticed. "Mom, you seem... happier today." Maya smiled, realizing that five minutes of intentional reflection had created ripples throughout her entire day.

The practice became her secret weapon—not because it made problems disappear, but because it helped her remember what truly mattered. In a world demanding constant motion, she had discovered the power of momentary stillness.""",
        "category": "spiritual_practice",
        "target_audience": "universal",
        "estimated_duration": 165,
        "themes": ["Faith", "Worship", "Guidance"],
        "characters": ["Maya", "executive", "grandmother", "daughter"],
        "setting": "home",
        "youtube_title": "The 5-Minute Morning Habit That Transforms Your Entire Day",
        "youtube_description": "Discover how one busy executive found peace and clarity through a simple daily practice. This isn't about meditation—it's about intentional living. Watch to learn the exact 5-minute routine that changed everything.",
        "youtube_tags": ["morning routine", "mindfulness", "productivity", "work-life balance", "daily habits", "stress relief", "intentional living", "executive life", "busy professionals"],
        "thumbnail_concept": "Professional woman with peaceful expression, sunrise lighting, subtle clock showing 5:30 AM",
        "target_keywords": ["morning routine", "daily reflection", "work-life balance", "mindful living", "executive wellness"],
        "generation_metadata": {
            "story_tokens": 450,
            "metadata_tokens": 120,
            "total_cost": 0.0285,
            "model_used": "demo-gpt-4",
            "prompt_type": "universal"
        },
        "generated_at": datetime.now().isoformat(),
        "quality_score": 0.0
    }
    
    # Sample story 2: Muslim community - Faith Recognition
    story2 = {
        "id": "story_3_1_muslim_demo002",
        "source_learning_id": learnings[2]['id'],
        "title": "Signs in the Storm",
        "description": "A young Muslim engineer finds divine guidance in unexpected places during a career crisis.",
        "content": """Ahmed stared at the termination letter, his hands trembling slightly. After three years of dedication, budget cuts had claimed his position at the tech startup. His wife was expecting their first child in two months.

"Allah has a plan," his mother had always said, but right now, that felt like empty comfort. As he walked home through the city, doubt clouded his thoughts. Had he made the right choices? Was he on the correct path?

At the bus stop, he noticed an elderly man struggling with heavy groceries. Without thinking, Ahmed helped him to a nearby bench. "You're very kind," the man said in accented English. "I'm new here from Syria. People like you remind me that goodness exists everywhere."

As they talked, Ahmed learned the man was a retired engineer who had lost everything in the war but rebuilt his life through determination and faith. "I see Allah's guidance in the smallest moments," the elder shared. "Even in difficulties, there are signs pointing us toward something better."

That evening, Ahmed received an unexpected call. A former colleague had recommended him for a position at a company developing clean energy solutions—work that aligned with his deepest values. The salary was better, the mission meaningful.

Later, during Maghrib prayer, Ahmed reflected on the day's events. The job loss that felt like a disaster had led him to help someone in need, which had somehow renewed his own faith and hope. In the most challenging moment, signs of divine guidance had appeared through human connection and unexpected opportunities.

"Subhan'Allah," he whispered, finally understanding what his mother meant. The path forward was becoming clear, one sign at a time.""",
        "category": "faith_recognition",
        "target_audience": "muslim_community",
        "estimated_duration": 185,
        "themes": ["Faith", "Guidance", "Psychology"],
        "characters": ["Ahmed", "engineer", "elderly man", "colleague"],
        "setting": "public",
        "youtube_title": "When I Lost Everything, I Found These Divine Signs",
        "youtube_description": "A young Muslim professional discovers how Allah's guidance appears in the most unexpected moments. This story shows how faith and action work together, even during life's biggest challenges. For anyone seeking signs of divine wisdom in difficult times.",
        "youtube_tags": ["Islamic inspiration", "faith journey", "divine guidance", "Muslim professionals", "career struggles", "signs from Allah", "spiritual growth", "Islamic stories"],
        "thumbnail_concept": "Young Muslim man in thoughtful pose, warm golden lighting, subtle geometric Islamic patterns",
        "target_keywords": ["Islamic guidance", "faith in difficulty", "divine signs", "Muslim inspiration", "spiritual resilience"],
        "generation_metadata": {
            "story_tokens": 485,
            "metadata_tokens": 135,
            "total_cost": 0.0310,
            "model_used": "demo-gpt-4",
            "prompt_type": "muslim"
        },
        "generated_at": datetime.now().isoformat(),
        "quality_score": 0.0
    }
    
    return [story1, story2]

def save_demo_stories():
    """Save demo stories to show the complete pipeline."""
    
    print("🎬 Generating Demo Stories")
    print("=" * 40)
    
    # Ensure directories exist
    os.makedirs("data/stories", exist_ok=True)
    os.makedirs("data/stories/by_category", exist_ok=True)
    os.makedirs("data/stories/by_audience", exist_ok=True)
    
    stories = load_sample_stories()
    
    for i, story in enumerate(stories, 1):
        print(f"\n📝 Demo Story {i}: {story['title']}")
        print(f"   Category: {story['category']}")
        print(f"   Audience: {story['target_audience']}")
        print(f"   Duration: {story['estimated_duration']}s ({story['estimated_duration']/60:.1f} min)")
        print(f"   Characters: {', '.join(story['characters'])}")
        print(f"   Setting: {story['setting']}")
        print(f"   YouTube Title: {story['youtube_title']}")
        print(f"   Tags: {len(story['youtube_tags'])} tags")
        print(f"   Cost: ${story['generation_metadata']['total_cost']:.4f}")
        
        # Save to files (demo mode)
        story_json = json.dumps(story, ensure_ascii=False, indent=2)
        
        # Save to demo file
        demo_file = f"data/stories/demo_story_{i}.json"
        with open(demo_file, 'w', encoding='utf-8') as f:
            f.write(story_json)
        
        print(f"   💾 Saved demo to: {demo_file}")
    
    # Show what the actual generation would look like
    total_cost = sum(s['generation_metadata']['total_cost'] for s in stories)
    total_tokens = sum(s['generation_metadata']['story_tokens'] + s['generation_metadata']['metadata_tokens'] for s in stories)
    total_duration = sum(s['estimated_duration'] for s in stories)
    
    print(f"\n🎉 Demo Generation Complete!")
    print(f"📊 Statistics:")
    print(f"   Stories generated: {len(stories)}")
    print(f"   Total video time: {total_duration/60:.1f} minutes")
    print(f"   Total tokens: {total_tokens}")
    print(f"   Total cost: ${total_cost:.4f}")
    
    print(f"\n📋 Sample Story Content Preview:")
    print(f"   Title: {stories[0]['title']}")
    print(f"   Content: {stories[0]['content'][:150]}...")
    
    print(f"\n🚀 Ready for Production!")
    print(f"   1. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
    print(f"   2. Run: python scripts/story_generator.py") 
    print(f"   3. Stories will be generated for all 4 learnings")
    print(f"   4. Estimated cost for 4 stories: ~$0.25")

if __name__ == "__main__":
    save_demo_stories()