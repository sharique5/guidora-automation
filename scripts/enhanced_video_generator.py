#!/usr/bin/env python3
"""
Enhanced Video Story Generator with Integrated Branding
Combines story generation with professional video production elements including
call-to-action slides and branding outros for complete video workflow.
"""

import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional
import json
from datetime import datetime

# Add the lib directory to the path
sys.path.append(str(Path(__file__).parent.parent / "lib"))

from llm_tools import LLMManager
from jsonl_utils import JsonlManager

@dataclass
class EnhancedVideoStory:
    """Enhanced story with integrated video production elements."""
    # Basic story information
    id: str
    source_learning_id: str
    title: str
    description: str
    content: str
    category: str
    target_audience: str
    estimated_duration: int
    themes: List[str]
    characters: List[str]
    setting: str
    
    # YouTube metadata
    youtube_title: str
    youtube_description: str
    youtube_tags: List[str]
    thumbnail_concept: str
    target_keywords: List[str]
    
    # Enhanced video production elements
    main_story_script: Dict[str, str]  # Segmented script for animation
    cta_slide_script: str
    branding_outro_script: str
    visual_instructions: Dict[str, any]
    production_timeline: Dict[str, any]
    engagement_optimization: Dict[str, any]
    
    # Metadata
    generation_metadata: Dict
    generated_at: str
    quality_score: float = 0.0

class EnhancedVideoGenerator:
    """Enhanced video story generator with integrated branding and CTAs."""
    
    def __init__(self, base_path: str = None):
        """Initialize the enhanced video generator."""
        if base_path is None:
            base_path = Path(__file__).parent.parent
        else:
            base_path = Path(base_path)
        
        self.base_path = base_path
        self.stories_path = base_path / "data" / "stories"
        self.learnings_path = base_path / "data" / "learnings"
        
        # Initialize LLM manager
        self.llm_manager = LLMManager()
        
        # Load enhanced prompt templates
        self.prompts = self._load_enhanced_prompts()
        
        # Initialize JSONL manager for learnings
        self.jsonl_manager = JsonlManager(str(self.learnings_path / "learnings.jsonl"))
        
        print("✅ Enhanced Video Generator initialized with branding integration")
    
    def _load_enhanced_prompts(self) -> Dict[str, str]:
        """Load enhanced prompt templates."""
        prompts = {}
        prompt_files = {
            'universal': 'prompts/story_universal_enhanced.txt',
            'muslim': 'prompts/story_muslim.txt',
            'spiritual': 'prompts/story_spiritual.txt',
            'metadata': 'prompts/youtube_metadata_enhanced.txt'
        }
        
        for key, filepath in prompt_files.items():
            full_path = self.base_path / filepath
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    prompts[key] = f.read().strip()
                print(f"✅ Loaded enhanced prompt: {key}")
            except FileNotFoundError:
                print(f"⚠️ Warning: Enhanced prompt file {filepath} not found, using fallback")
                # Fallback to original prompts if enhanced ones don't exist
                fallback_path = str(filepath).replace('_enhanced', '')
                try:
                    with open(self.base_path / fallback_path, 'r', encoding='utf-8') as f:
                        prompts[key] = f.read().strip()
                except FileNotFoundError:
                    prompts[key] = "Generate enhanced content for: {practical_application}"
        
        return prompts
    
    def generate_enhanced_story(self, learning_data: Dict, target_audience: str = 'universal') -> EnhancedVideoStory:
        """Generate an enhanced story with integrated video production elements."""
        
        # Validate learning data
        if not learning_data.get('practical_application'):
            raise ValueError("Learning data must contain 'practical_application' field")
        
        print(f"🎬 Generating enhanced video story for: {learning_data.get('title', 'Unknown')}")
        
        # Select appropriate prompt
        prompt_key = {
            'universal': 'universal',
            'muslim_community': 'muslim',
            'spiritual_seekers': 'spiritual'
        }.get(target_audience, 'universal')
        
        # Generate main story with integrated branding elements
        story_prompt = self.prompts[prompt_key].format(
            practical_application=learning_data['practical_application']
        )
        
        print("🤖 Generating story content with LLM...")
        story_response = self.llm_manager.generate_content(
            prompt=story_prompt,
            max_tokens=1500,  # Increased for enhanced content
            temperature=0.8
        )
        
        # Parse story response (this would need to be enhanced based on the actual LLM response format)
        story_content = self._parse_enhanced_story_response(story_response)
        
        # Generate enhanced YouTube metadata with branding
        metadata_prompt = self.prompts['metadata'].format(
            story_content=story_content['main_content']
        )
        
        print("🎯 Generating enhanced metadata with branding elements...")
        metadata_response = self.llm_manager.generate_content(
            prompt=metadata_prompt,
            max_tokens=800,
            temperature=0.7
        )
        
        # Parse metadata response
        metadata = self._parse_enhanced_metadata_response(metadata_response)
        
        # Calculate enhanced duration (including CTAs and branding)
        base_duration = self._estimate_duration(story_content['main_content'])
        total_duration = base_duration + 7 + 5  # Main + CTA + Branding
        
        # Create enhanced story object
        story_id = self._generate_story_id(learning_data)
        
        enhanced_story = EnhancedVideoStory(
            id=story_id,
            source_learning_id=learning_data.get('id', 'unknown'),
            title=story_content.get('title', 'Untitled Story'),
            description=story_content.get('description', 'A story of wisdom and transformation'),
            content=story_content['main_content'],
            category=self._determine_category(learning_data),
            target_audience=target_audience,
            estimated_duration=total_duration,
            themes=self._extract_themes(story_content['main_content']),
            characters=self._extract_characters(story_content['main_content']),
            setting=self._determine_setting(story_content['main_content']),
            
            # YouTube metadata
            youtube_title=metadata.get('title', story_content.get('title', 'Untitled')),
            youtube_description=metadata.get('description', ''),
            youtube_tags=metadata.get('tags', []),
            thumbnail_concept=metadata.get('thumbnail_concept', ''),
            target_keywords=metadata.get('target_keywords', []),
            
            # Enhanced video production elements
            main_story_script=metadata.get('main_story_script', {}),
            cta_slide_script=metadata.get('cta_slide_script', ''),
            branding_outro_script=metadata.get('branding_outro_script', ''),
            visual_instructions=metadata.get('visual_instructions', {}),
            production_timeline=metadata.get('production_timeline', {}),
            engagement_optimization=metadata.get('engagement_optimization', {}),
            
            generation_metadata={
                'story_tokens': len(story_response.split()) if story_response else 0,
                'metadata_tokens': len(metadata_response.split()) if metadata_response else 0,
                'total_cost': self.llm_manager.get_usage_stats().get('total_cost', 0),
                'model_used': 'gpt-4-turbo',
                'prompt_type': prompt_key,
                'enhanced_features': True,
                'branding_integration': True
            },
            generated_at=datetime.now().isoformat()
        )
        
        print(f"✅ Enhanced story generated: {enhanced_story.title}")
        print(f"   📊 Total duration: {total_duration}s (Story: {base_duration}s + CTA: 7s + Branding: 5s)")
        print(f"   🎯 Target audience: {target_audience}")
        print(f"   🎨 Includes professional branding elements")
        
        return enhanced_story
    
    def _parse_enhanced_story_response(self, response: str) -> Dict[str, str]:
        """Parse the enhanced LLM story response."""
        # This is a simplified parser - in practice, you'd want more robust parsing
        lines = response.split('\n')
        
        story_data = {
            'title': 'Untitled Story',
            'description': 'A story of transformation and wisdom',
            'main_content': response  # Simplified - would need proper parsing
        }
        
        # Extract title if present
        for line in lines[:10]:  # Check first 10 lines
            if line.startswith('**TITLE**') or line.startswith('TITLE:'):
                story_data['title'] = line.split(':', 1)[-1].strip().strip('*').strip()
                break
        
        return story_data
    
    def _parse_enhanced_metadata_response(self, response: str) -> Dict:
        """Parse the enhanced metadata response."""
        # Simplified parser - would need enhancement based on actual LLM output
        return {
            'title': 'Enhanced Video Title',
            'description': 'Enhanced video description with CTAs',
            'tags': ['wisdom', 'inspiration', 'personal growth', 'motivation'],
            'thumbnail_concept': 'Professional thumbnail with branding elements',
            'target_keywords': ['personal growth', 'wisdom', 'inspiration'],
            'main_story_script': {},
            'cta_slide_script': 'Thank you for watching! Please like, subscribe, and share!',
            'branding_outro_script': 'Wisdom for Modern Life - Where insights meet inspiration',
            'visual_instructions': {
                'cta_slide': {
                    'background': 'Soft gradient matching story theme',
                    'logo_placement': 'Center, 25% width',
                    'animations': 'Gentle pulse on subscribe button'
                },
                'branding_slide': {
                    'background': 'Minimalist brand colors',
                    'logo_size': '40% frame width',
                    'effects': 'Gentle fade-in'
                }
            },
            'production_timeline': {
                'main_story': '0:00-2:40',
                'cta_slide': '2:40-2:47',
                'branding_outro': '2:47-2:52',
                'total_length': '2:52'
            },
            'engagement_optimization': {
                'hook_strength': 'High',
                'retention_points': ['0:15', '1:30', '2:15'],
                'cta_placement': 'Natural conclusion'
            }
        }
    
    def save_enhanced_story(self, story: EnhancedVideoStory, language: str = 'en'):
        """Save enhanced story with all production elements."""
        
        # Create language-specific directory
        lang_dir = self.stories_path / language
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        safe_title = "".join(c for c in story.title.lower() if c.isalnum() or c in ' -_').strip()
        safe_title = "_".join(safe_title.split())
        filename = f"{safe_title}_{language}.json"
        
        # Convert to dictionary with enhanced elements
        story_dict = {
            'title': story.title,
            'description': story.description,
            'category': story.category,
            'target_audience': story.target_audience,
            'estimated_duration': story.estimated_duration,
            'themes': story.themes,
            'characters': story.characters,
            'setting': story.setting,
            'story_content': story.content,
            
            # YouTube metadata
            'youtube_title': story.youtube_title,
            'youtube_description': story.youtube_description,
            'youtube_tags': story.youtube_tags,
            'thumbnail_concept': story.thumbnail_concept,
            'target_keywords': story.target_keywords,
            
            # Enhanced video production elements
            'video_production': {
                'main_story_script': story.main_story_script,
                'cta_slide_script': story.cta_slide_script,
                'branding_outro_script': story.branding_outro_script,
                'visual_instructions': story.visual_instructions,
                'production_timeline': story.production_timeline,
                'engagement_optimization': story.engagement_optimization
            },
            
            # Metadata
            'generation_metadata': story.generation_metadata,
            'generated_at': story.generated_at,
            'quality_score': story.quality_score
        }
        
        # Save story
        story_path = lang_dir / filename
        with open(story_path, 'w', encoding='utf-8') as f:
            json.dump(story_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Enhanced story saved: {story_path}")
        print(f"   🎬 Includes: Main story + CTA slide + Branding outro")
        print(f"   📋 Production timeline: {story.estimated_duration}s total")
        
        return str(story_path)
    
    # Include other helper methods from the original generator
    def _estimate_duration(self, content: str) -> int:
        """Estimate video duration based on word count."""
        words = len(content.split())
        duration_minutes = words / 150  # ~150 words per minute
        return int(duration_minutes * 60)
    
    def _generate_story_id(self, learning_data: Dict) -> str:
        """Generate unique story ID."""
        base_id = learning_data.get('id', 'story')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        return f"{base_id}_{timestamp}"
    
    def _determine_category(self, learning_data: Dict) -> str:
        """Determine story category."""
        return learning_data.get('category', 'personal_growth')
    
    def _extract_themes(self, content: str) -> List[str]:
        """Extract themes from story content."""
        return ['wisdom', 'transformation', 'personal_growth']
    
    def _extract_characters(self, content: str) -> List[str]:
        """Extract character types from story."""
        return ['professional']
    
    def _determine_setting(self, content: str) -> str:
        """Determine story setting."""
        return 'modern_urban'

def main():
    """Test the enhanced video generator."""
    print("🎬 Enhanced Video Generator with Integrated Branding")
    print("=" * 60)
    
    generator = EnhancedVideoGenerator()
    
    # Test with sample learning data
    sample_learning = {
        'id': 'enhanced_test_001',
        'title': 'Finding Strength in Setbacks',
        'practical_application': 'When life gives you unexpected challenges, look for the hidden opportunities and lessons that can guide you toward a better path.',
        'category': 'personal_growth'
    }
    
    try:
        # Generate enhanced story
        enhanced_story = generator.generate_enhanced_story(
            sample_learning, 
            target_audience='universal'
        )
        
        # Save the story
        saved_path = generator.save_enhanced_story(enhanced_story, 'en')
        
        print(f"\n✅ Enhanced video story generation complete!")
        print(f"📂 Saved to: {saved_path}")
        print(f"🎯 Features included:")
        print(f"   • Professional story narrative")
        print(f"   • Call-to-action slide with like/subscribe/share")
        print(f"   • Branded outro with channel tagline")
        print(f"   • Complete production timeline")
        print(f"   • Visual instruction guidelines")
        print(f"   • Engagement optimization notes")
        
    except Exception as e:
        print(f"❌ Error generating enhanced story: {e}")

if __name__ == "__main__":
    main()