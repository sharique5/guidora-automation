#!/usr/bin/env python3
"""
Story Generator - Week 2 MVP
Converts practical Islamic wisdom into modern, engaging stories for YouTube content
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

# Import our LLM tools (handle import path)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.llm_tools import LLMManager, create_default_manager, LLMResponse

@dataclass
class Story:
    """Represents a generated story from a learning."""
    id: str
    source_learning_id: str
    title: str
    description: str
    content: str
    category: str  # spiritual_practice, faith_recognition, ethical_relationships
    target_audience: str  # universal, muslim_community, spiritual_seekers
    estimated_duration: int  # seconds
    themes: List[str]
    characters: List[str]
    setting: str
    youtube_title: str
    youtube_description: str
    youtube_tags: List[str]
    thumbnail_concept: str
    target_keywords: List[str]
    generation_metadata: Dict
    generated_at: str
    quality_score: float = 0.0

class StoryGenerator:
    """Generates stories from learnings using LLM integration."""
    
    def __init__(self, 
                 learnings_file: str = "data/learnings/learnings.jsonl",
                 output_dir: str = "data/stories",
                 llm_manager: Optional[LLMManager] = None):
        self.learnings_file = learnings_file
        self.output_dir = output_dir
        self.llm_manager = llm_manager or create_default_manager()
        
        # Load prompt templates
        self.prompts = self._load_prompts()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        for subdir in ["by_category", "by_audience"]:
            os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)
    
    def _load_prompts(self) -> Dict[str, str]:
        """Load all prompt templates with enhanced branding support."""
        prompts = {}
        prompt_files = {
            'universal': 'prompts/story_universal_enhanced.txt',
            'universal_fallback': 'prompts/story_universal.txt',
            'muslim': 'prompts/story_muslim.txt',
            'spiritual': 'prompts/story_spiritual.txt',
            'metadata': 'prompts/youtube_metadata_enhanced.txt',
            'metadata_fallback': 'prompts/youtube_metadata.txt'
        }
        
        for key, filepath in prompt_files.items():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    prompts[key] = f.read().strip()
                    if 'enhanced' in key:
                        print(f"✅ Loaded enhanced prompt: {key}")
            except FileNotFoundError:
                if 'enhanced' in key:
                    # Try fallback to original prompt
                    fallback_key = key.replace('_enhanced', '_fallback')
                    if fallback_key in prompt_files:
                        try:
                            with open(prompt_files[fallback_key], 'r', encoding='utf-8') as f:
                                prompts[key] = f.read().strip()
                                print(f"⚠️ Using fallback prompt for {key}")
                        except FileNotFoundError:
                            print(f"❌ Neither enhanced nor fallback prompt found for {key}")
                            prompts[key] = "Generate enhanced content for: {practical_application}"
                    else:
                        print(f"⚠️ Warning: Enhanced prompt file {filepath} not found")
                        prompts[key] = "Generate enhanced content for: {practical_application}"
                else:
                    print(f"⚠️ Warning: Prompt file {filepath} not found")
                    prompts[key] = "Generate a story for: {practical_application}"
        
        return prompts
    
    def _categorize_learning(self, learning: Dict) -> str:
        """Determine story category based on learning content."""
        practical_app = learning.get('practical_application', '').lower()
        themes = str(learning.get('main_themes', [])).lower()
        
        # Categorization logic based on content analysis
        if any(word in practical_app for word in ['prayer', 'remembrance', 'reciting', 'spiritual']):
            return 'spiritual_practice'
        elif any(word in practical_app for word in ['faith', 'divine', 'signs', 'god']):
            return 'faith_recognition'
        elif any(word in practical_app for word in ['relationship', 'taqwa', 'ethical', 'social']):
            return 'ethical_relationships'
        else:
            return 'general_wisdom'
    
    def _select_target_audience(self, learning: Dict) -> str:
        """Select primary target audience based on learning audience groups."""
        audiences = learning.get('audience_groups', [])
        
        # Priority order for audience selection
        if 'Universal/All Humanity' in audiences:
            return 'universal'
        elif 'Non-Muslims' in audiences or 'Truth & Meaning Seekers' in audiences:
            return 'universal'
        elif 'Spiritual Seekers' in audiences:
            return 'spiritual_seekers'
        elif 'General Muslim Community' in audiences:
            return 'muslim_community'
        else:
            return 'universal'  # Default to universal appeal
    
    def _extract_characters(self, story_content: str) -> List[str]:
        """Extract character names/types from story content."""
        # Simple extraction - look for common patterns
        characters = []
        
        # Look for names (capitalized words that aren't common nouns)
        name_pattern = r'\b([A-Z][a-z]+)\b'
        potential_names = re.findall(name_pattern, story_content)
        
        # Filter common non-names
        common_words = {'The', 'This', 'That', 'When', 'She', 'He', 'Her', 'His', 'But', 'And', 'Or'}
        names = [name for name in potential_names if name not in common_words]
        
        # Add character types mentioned
        character_types = ['professional', 'student', 'parent', 'teacher', 'manager', 'colleague']
        for char_type in character_types:
            if char_type in story_content.lower():
                characters.append(char_type)
        
        return list(set(characters))[:3]  # Limit to 3 main characters
    
    def _extract_setting(self, story_content: str) -> str:
        """Extract primary setting from story content."""
        settings = {
            'office': ['office', 'workplace', 'meeting', 'desk', 'computer'],
            'home': ['home', 'kitchen', 'bedroom', 'living room', 'house'],
            'school': ['school', 'classroom', 'university', 'campus', 'library'],
            'public': ['park', 'street', 'cafe', 'restaurant', 'store'],
            'nature': ['mountain', 'forest', 'beach', 'garden', 'outdoors']
        }
        
        content_lower = story_content.lower()
        for setting, keywords in settings.items():
            if any(keyword in content_lower for keyword in keywords):
                return setting
        
        return 'general'
    
    def _estimate_duration(self, content: str) -> int:
        """Estimate video duration based on word count."""
        words = len(content.split())
        # Assume ~150 words per minute for comfortable narration
        duration_minutes = words / 150
        return int(duration_minutes * 60)  # Convert to seconds
    
    def _parse_llm_story_response(self, response_content: str) -> Dict:
        """Parse structured story response from LLM."""
        parsed = {
            'title': '',
            'description': '',
            'content': '',
            'themes': []
        }
        
        # Try to extract structured sections
        sections = {
            'title': r'(?i)\*\*TITLE\*\*[:\s]*([^\n]*)',
            'description': r'(?i)\*\*DESCRIPTION\*\*[:\s]*([^\n]*(?:\n[^\*][^\n]*)*)',
            'content': r'(?i)\*\*STORY CONTENT\*\*[:\s]*(.*?)(?=\*\*|$)',
        }
        
        for key, pattern in sections.items():
            match = re.search(pattern, response_content, re.DOTALL)
            if match:
                parsed[key] = match.group(1).strip()
        
        # If no structured format, use entire response as content
        if not parsed['content']:
            parsed['content'] = response_content
            
            # Try to extract a title from the first line
            lines = response_content.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('**'):
                    parsed['title'] = line.strip()[:60]  # Limit title length
                    break
        
        return parsed
    
    def _parse_metadata_response(self, response_content: str) -> Dict:
        """Parse YouTube metadata from LLM response."""
        metadata = {
            'youtube_title': '',
            'youtube_description': '',
            'youtube_tags': [],
            'thumbnail_concept': '',
            'target_keywords': []
        }
        
        # Parse structured metadata
        patterns = {
            'youtube_title': r'(?i)\*\*TITLE\*\*[:\s]*([^\n]*)',
            'youtube_description': r'(?i)\*\*DESCRIPTION\*\*[:\s]*([^\n]*(?:\n[^\*][^\n]*)*)',
            'youtube_tags': r'(?i)\*\*TAGS\*\*[:\s]*([^\n]*(?:\n[^\*][^\n]*)*)',
            'thumbnail_concept': r'(?i)\*\*THUMBNAIL CONCEPT\*\*[:\s]*([^\n]*(?:\n[^\*][^\n]*)*)',
            'target_keywords': r'(?i)\*\*TARGET KEYWORDS\*\*[:\s]*([^\n]*(?:\n[^\*][^\n]*)*)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, response_content, re.DOTALL)
            if match:
                value = match.group(1).strip()
                if key in ['youtube_tags', 'target_keywords']:
                    # Parse comma-separated lists
                    metadata[key] = [tag.strip() for tag in value.replace('\n', ',').split(',') if tag.strip()]
                else:
                    metadata[key] = value
        
        return metadata
    
    def generate_story(self, learning: Dict, target_audience: Optional[str] = None) -> Story:
        """Generate a single story from a learning."""
        print(f"🎬 Generating story for learning: {learning['id']}")
        
        # Determine category and audience
        category = self._categorize_learning(learning)
        audience = target_audience or self._select_target_audience(learning)
        
        # Select appropriate prompt
        prompt_key = {
            'universal': 'universal',
            'muslim_community': 'muslim',
            'spiritual_seekers': 'spiritual'
        }.get(audience, 'universal')
        
        # Generate story content
        story_prompt = self.prompts[prompt_key].format(
            practical_application=learning['practical_application']
        )
        
        print(f"   📝 Using {prompt_key} template for {audience} audience")
        story_response = self.llm_manager.generate(story_prompt)
        
        # Parse story structure
        story_data = self._parse_llm_story_response(story_response.content)
        
        # Generate YouTube metadata
        metadata_prompt = self.prompts['metadata'].format(
            story_content=story_data['content']
        )
        
        metadata_response = self.llm_manager.generate(metadata_prompt)
        metadata = self._parse_metadata_response(metadata_response.content)
        
        # Extract story elements
        characters = self._extract_characters(story_data['content'])
        setting = self._extract_setting(story_data['content'])
        duration = self._estimate_duration(story_data['content'])
        
        # Create story ID
        story_id = f"story_{learning['chapter_id']}_{learning['verse_number']}_{audience}_{hashlib.md5(story_data['content'].encode()).hexdigest()[:8]}"
        
        # Create story object
        story = Story(
            id=story_id,
            source_learning_id=learning['id'],
            title=story_data['title'] or metadata['youtube_title'],
            description=story_data['description'] or metadata['youtube_description'][:200],
            content=story_data['content'],
            category=category,
            target_audience=audience,
            estimated_duration=duration,
            themes=learning['main_themes'],
            characters=characters,
            setting=setting,
            youtube_title=metadata['youtube_title'],
            youtube_description=metadata['youtube_description'],
            youtube_tags=metadata['youtube_tags'],
            thumbnail_concept=metadata['thumbnail_concept'],
            target_keywords=metadata['target_keywords'],
            generation_metadata={
                'story_tokens': story_response.tokens_used,
                'metadata_tokens': metadata_response.tokens_used,
                'total_cost': story_response.cost_estimate + metadata_response.cost_estimate,
                'model_used': story_response.model,
                'prompt_type': prompt_key
            },
            generated_at=datetime.now().isoformat()
        )
        
        print(f"   ✅ Generated {duration}s story with {story_response.tokens_used + metadata_response.tokens_used} tokens")
        return story
    
    def generate_enhanced_story_with_branding(self, learning: Dict, target_audience: Optional[str] = None) -> Story:
        """Generate enhanced story with integrated branding and CTA elements."""
        print(f"🎬 Generating ENHANCED story with branding for learning: {learning['id']}")
        
        # Determine category and audience
        category = self._categorize_learning(learning)
        audience = target_audience or self._select_target_audience(learning)
        
        # Use enhanced prompts if available
        prompt_key = {
            'universal': 'universal',
            'muslim_community': 'muslim',
            'spiritual_seekers': 'spiritual'
        }.get(audience, 'universal')
        
        # Generate enhanced story content with branding
        story_prompt = self.prompts[prompt_key].format(
            practical_application=learning['practical_application']
        )
        
        print(f"   🎨 Using ENHANCED {prompt_key} template for {audience} audience")
        print(f"   ✨ Including: CTA slide + Branding outro + Visual instructions")
        
        story_response = self.llm_manager.generate(story_prompt)
        
        # Parse enhanced story structure
        story_data = self._parse_llm_story_response(story_response.content)
        
        # Generate enhanced YouTube metadata with branding
        metadata_prompt = self.prompts['metadata'].format(
            story_content=story_data['content']
        )
        
        print(f"   📊 Generating enhanced metadata with production timeline...")
        metadata_response = self.llm_manager.generate(metadata_prompt)
        metadata = self._parse_metadata_response(metadata_response.content)
        
        # Enhanced duration calculation (includes CTA + branding)
        base_duration = self._estimate_duration(story_data['content'])
        enhanced_duration = base_duration + 7 + 5  # Main story + CTA slide + Branding outro
        
        # Create enhanced story ID
        story_id = f"enhanced_story_{learning.get('chapter_id', 'unknown')}_{learning.get('verse_number', '000')}_{audience}_{hashlib.md5(story_data['content'].encode()).hexdigest()[:8]}"
        
        # Create enhanced story with all production elements
        story = Story(
            id=story_id,
            source_learning_id=learning['id'],
            title=story_data['title'],
            description=story_data['description'],
            content=story_data['content'],
            category=category,
            target_audience=audience,
            estimated_duration=enhanced_duration,
            themes=story_data.get('themes', ['wisdom', 'personal_growth']),
            characters=story_data.get('characters', ['professional']),
            setting=story_data.get('setting', 'modern_urban'),
            youtube_title=metadata['youtube_title'],
            youtube_description=metadata['youtube_description'],
            youtube_tags=metadata['youtube_tags'],
            thumbnail_concept=metadata['thumbnail_concept'],
            target_keywords=metadata['target_keywords'],
            generation_metadata={
                'story_tokens': story_response.tokens_used,
                'metadata_tokens': metadata_response.tokens_used,
                'total_cost': story_response.cost_estimate + metadata_response.cost_estimate,
                'model_used': story_response.model,
                'prompt_type': prompt_key,
                'enhanced_features': True,
                'branding_integration': True,
                'video_structure': {
                    'main_story_duration': base_duration,
                    'cta_slide_duration': 7,
                    'branding_outro_duration': 5,
                    'total_duration': enhanced_duration
                },
                'production_elements': {
                    'cta_slide_included': True,
                    'branding_outro_included': True,
                    'visual_instructions_included': True,
                    'engagement_optimization': True
                }
            },
            generated_at=datetime.now().isoformat()
        )
        
        print(f"   ✅ Generated ENHANCED {enhanced_duration}s story:")
        print(f"      📺 Main story: {base_duration}s")
        print(f"      👍 CTA slide: 7s (like, subscribe, share)")
        print(f"      🏷️ Branding outro: 5s (channel tagline)")
        print(f"      🎯 Total tokens: {story_response.tokens_used + metadata_response.tokens_used}")
        print(f"      💰 Cost: ${story_response.cost_estimate + metadata_response.cost_estimate:.4f}")
        
        return story
    
    def save_story(self, story: Story):
        """Save story to JSONL files."""
        story_json = json.dumps(asdict(story), ensure_ascii=False)
        
        # Save to main stories file
        main_file = os.path.join(self.output_dir, "stories.jsonl")
        with open(main_file, 'a', encoding='utf-8') as f:
            f.write(story_json + '\n')
        
        # Save to category file
        category_file = os.path.join(self.output_dir, "by_category", f"{story.category}.jsonl")
        with open(category_file, 'a', encoding='utf-8') as f:
            f.write(story_json + '\n')
        
        # Save to audience file
        audience_file = os.path.join(self.output_dir, "by_audience", f"{story.target_audience}.jsonl")
        with open(audience_file, 'a', encoding='utf-8') as f:
            f.write(story_json + '\n')
        
        print(f"💾 Saved story to {main_file}")
    
    def generate_stories_from_learnings(self, limit: Optional[int] = None) -> List[Story]:
        """Generate stories from all available learnings."""
        stories = []
        
        print(f"🚀 Generating stories from {self.learnings_file}")
        
        with open(self.learnings_file, 'r', encoding='utf-8') as f:
            learnings = []
            for line in f:
                if line.strip():
                    learnings.append(json.loads(line))
        
        print(f"📚 Found {len(learnings)} learnings to process")
        
        for i, learning in enumerate(learnings):
            if limit and i >= limit:
                break
            
            try:
                story = self.generate_story(learning)
                self.save_story(story)
                stories.append(story)
                
            except Exception as e:
                print(f"❌ Failed to generate story for {learning['id']}: {e}")
                continue
        
        # Show generation summary
        total_cost = sum(story.generation_metadata['total_cost'] for story in stories)
        total_tokens = sum(story.generation_metadata['story_tokens'] + story.generation_metadata['metadata_tokens'] for story in stories)
        
        print(f"\n🎉 Generated {len(stories)} stories")
        print(f"💰 Total cost: ${total_cost:.4f}")
        print(f"🔢 Total tokens: {total_tokens}")
        
        return stories
    
    def generate_enhanced_stories_from_learnings(self, limit: Optional[int] = None) -> List[Story]:
        """Generate enhanced stories with branding from all available learnings."""
        stories = []
        
        print(f"🚀 Generating ENHANCED stories with branding from {self.learnings_file}")
        
        with open(self.learnings_file, 'r', encoding='utf-8') as f:
            learnings = []
            for line in f:
                if line.strip():
                    learnings.append(json.loads(line))
        
        print(f"📚 Found {len(learnings)} learnings to process with enhanced features")
        
        if limit:
            learnings = learnings[:limit]
            print(f"🎯 Processing first {limit} learnings for enhanced generation")
        
        for i, learning in enumerate(learnings, 1):
            print(f"\n📖 Processing learning {i}/{len(learnings)}: {learning.get('title', 'Untitled')}")
            
            try:
                # Generate enhanced story with branding
                story = self.generate_enhanced_story_with_branding(learning)
                self.save_story(story)
                stories.append(story)
                
                print(f"   ✅ Enhanced story saved with:")
                print(f"      🎬 Main content: {story.generation_metadata['video_structure']['main_story_duration']}s")
                print(f"      👍 CTA slide: {story.generation_metadata['video_structure']['cta_slide_duration']}s")
                print(f"      🏷️ Branding outro: {story.generation_metadata['video_structure']['branding_outro_duration']}s")
                print(f"      💰 Cost: ${story.generation_metadata['total_cost']:.4f}")
                
            except Exception as e:
                print(f"   ❌ Error generating enhanced story: {e}")
                continue
        
        # Show enhanced generation summary
        total_cost = sum(story.generation_metadata['total_cost'] for story in stories)
        total_tokens = sum(story.generation_metadata['story_tokens'] + story.generation_metadata['metadata_tokens'] for story in stories)
        total_duration = sum(story.estimated_duration for story in stories)
        
        print(f"\n🎉 Generated {len(stories)} ENHANCED stories with branding!")
        print(f"💰 Total cost: ${total_cost:.4f}")
        print(f"🔢 Total tokens: {total_tokens}")
        print(f"⏱️ Total video time: {total_duration/60:.1f} minutes")
        print(f"✨ Enhanced features: CTA slides + Branding outros + Visual guides")
        
        return stories
    
    def get_generation_stats(self) -> Dict:
        """Get statistics about generated stories."""
        stats = {
            'total_stories': 0,
            'by_category': {},
            'by_audience': {},
            'total_duration': 0,
            'avg_duration': 0
        }
        
        stories_file = os.path.join(self.output_dir, "stories.jsonl")
        if not os.path.exists(stories_file):
            return stats
        
        durations = []
        with open(stories_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    story = json.loads(line)
                    stats['total_stories'] += 1
                    
                    # Count by category
                    category = story['category']
                    stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
                    
                    # Count by audience
                    audience = story['target_audience']
                    stats['by_audience'][audience] = stats['by_audience'].get(audience, 0) + 1
                    
                    # Duration stats
                    duration = story['estimated_duration']
                    durations.append(duration)
                    stats['total_duration'] += duration
        
        if durations:
            stats['avg_duration'] = sum(durations) / len(durations)
        
        return stats

def main():
    """Main function for testing story generation."""
    print("🎬 Guidora Story Generation MVP - Enhanced with Branding")
    print("=" * 60)
    
    # Initialize generator
    generator = StoryGenerator()
    
    # Ask user for generation type
    print("\n🎯 Choose generation mode:")
    print("1. Standard story generation (original)")
    print("2. Enhanced story generation (with CTA + branding)")
    
    choice = input("\nEnter choice (1 or 2) [default: 2]: ").strip() or "2"
    
    if choice == "2":
        print("\n🚀 Using ENHANCED generation with branding integration...")
        # Generate enhanced stories with branding
        stories = generator.generate_enhanced_stories_from_learnings(limit=4)
        print(f"\n✨ Enhanced Features Included:")
        print(f"   • Professional call-to-action slides")
        print(f"   • Branded outros with channel taglines")
        print(f"   • Visual instruction guidelines")
        print(f"   • Production timeline breakdowns")
        print(f"   • Engagement optimization notes")
    else:
        print("\n🚀 Using STANDARD generation...")
        # Generate standard stories
        stories = generator.generate_stories_from_learnings(limit=4)
    
    # Show generation statistics
    stats = generator.get_generation_stats()
    print(f"\n📊 Generation Statistics:")
    print(f"   Total stories: {stats['total_stories']}")
    print(f"   By category: {stats['by_category']}")
    print(f"   By audience: {stats['by_audience']}")
    print(f"   Total video time: {stats['total_duration']/60:.1f} minutes")
    
    # Show LLM usage stats
    llm_stats = generator.llm_manager.get_usage_stats()
    print(f"\n🤖 LLM Usage:")
    print(f"   Total requests: {llm_stats['total_requests']}")
    print(f"   Total cost: ${llm_stats['total_cost']:.4f}")
    
    if choice == "2":
        print(f"\n🎬 Enhanced Video Production Ready:")
        print(f"   - Stories include complete production guidelines")
        print(f"   - CTA slides with like/subscribe/share prompts")
        print(f"   - Professional branding outros")
        print(f"   - Visual instruction sets for Instadoodle")
        print(f"   - Optimized for maximum engagement")
    
    print(f"\n🎯 Next Steps:")
    print(f"   - Review generated stories in data/stories/")
    print(f"   - Test story quality and engagement")
    print(f"   - Use enhanced production elements for video creation")
    print(f"   - Ready for professional video production!")

def main_enhanced_only():
    """Generate only enhanced stories with branding."""
    print("🎬 Enhanced Video Generation with Integrated Branding")
    print("=" * 60)
    
    generator = StoryGenerator()
    
    # Generate enhanced stories only
    stories = generator.generate_enhanced_stories_from_learnings(limit=4)
    
    # Show statistics
    stats = generator.get_generation_stats()
    llm_stats = generator.llm_manager.get_usage_stats()
    
    print(f"\n✅ Enhanced Generation Complete!")
    print(f"📊 Generated {stats['total_stories']} stories with full branding")
    print(f"💰 Total cost: ${llm_stats['total_cost']:.4f}")
    print(f"🎬 Total video time: {stats['total_duration']/60:.1f} minutes")
    print(f"\n🚀 Ready for professional video production with:")
    print(f"   • Complete production timelines")
    print(f"   • Professional CTA slides")
    print(f"   • Branded channel outros")
    print(f"   • Visual instruction guidelines")

if __name__ == "__main__":
    main()