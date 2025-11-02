"""
Natural Language Translator for Mindfulness Stories

This module provides AI-powered translation that focuses on natural, conversational 
language with cultural adaptation and regional slang instead of literal translation.

Key Features:
- Conversational translation with daily communication slang
- Cultural adaptation for different regions
- Maintains storytelling flow and emotional impact
- Preserves narrative structure while adapting to local context
"""

import json
import logging
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NaturalTranslator:
    """
    AI-powered natural language translator for mindfulness stories.
    Converts English content to conversational, culturally-adapted translations.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Natural Translator with OpenAI API."""
        # Get API key from parameter or environment
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=api_key)
        
        # Supported languages with cultural context
        self.supported_languages = {
            'es': {
                'name': 'Spanish',
                'region': 'Latin America',
                'cultural_context': 'familia-oriented, community-focused, warm expressions',
                'common_phrases': ['que tal', 'vale', 'che', 'oye', 'sabes que']
            },
            'fr': {
                'name': 'French',
                'region': 'France/Francophone',
                'cultural_context': 'intellectual, refined, philosophical approach',
                'common_phrases': ['tu sais', 'bon', 'eh bien', 'alors', 'quand même']
            },
            'ur': {
                'name': 'Urdu',
                'region': 'Pakistan/India/Global',
                'cultural_context': 'poetic expressions, respectful language, spiritual wisdom',
                'common_phrases': ['acha', 'theek hai', 'kya baat hai', 'mashallah', 'subhanallah', 'yaar', 'bilkul']
            },
            'ar': {
                'name': 'Arabic',
                'region': 'Middle East/North Africa',
                'cultural_context': 'community bonds, respectful, faith-integrated',
                'common_phrases': ['habibi', 'yalla', 'inshallah', 'mashallah', 'khalas']
            }
        }
    
    def get_translation_prompt(self, language_code: str, content: dict) -> str:
        """Generate whiteboard-optimized translation prompt for specific language."""
        
        lang_info = self.supported_languages.get(language_code, {})
        lang_name = lang_info.get('name', 'Unknown')
        cultural_context = lang_info.get('cultural_context', '')
        common_phrases = lang_info.get('common_phrases', [])
        
        # Extract clean story content from nested format if needed
        story_content = content.get('story_content', '')
        if isinstance(story_content, str) and '```json' in story_content:
            # Extract content from nested JSON format
            try:
                import re
                json_match = re.search(r'```json\s*\n(.*?)\n```', story_content, re.DOTALL)
                if json_match:
                    nested_content = json.loads(json_match.group(1))
                    story_content = nested_content.get('Story Content', story_content)
            except:
                pass  # Use original content if parsing fails
        
        prompt = f"""
You are an expert translator specializing in whiteboard explainer video scripts. Create natural, conversational {lang_name} optimized for visual storytelling.

TARGET LANGUAGE: {lang_name} ({language_code})
CULTURAL CONTEXT: {cultural_context}
NATURAL EXPRESSIONS TO USE: {', '.join(common_phrases)}

WHITEBOARD VIDEO SCRIPT REQUIREMENTS:
1. SHORT SENTENCES: 10-15 words maximum for visual pacing
2. CLEAR NARRATION: Easy to follow when watching drawings
3. CONVERSATIONAL TONE: How people actually speak, not formal translation
4. EMOTIONAL BEATS: Clear moments where visuals can emphasize feelings
5. CULTURAL AUTHENTICITY: Use regional expressions that feel natural
6. VISUAL LANGUAGE: Descriptions that easily translate to simple drawings
7. SMOOTH FLOW: Natural transitions between ideas

ORIGINAL STORY:
Title: {content.get('title', '')}
Description: {content.get('description', '')}
Story Content: {story_content}
YouTube Title: {content.get('youtube_title', '')}
YouTube Description: {content.get('youtube_description', '')}
Tags: {', '.join(content.get('youtube_tags', []))}

RESPONSE FORMAT - Return ONLY valid JSON with these exact fields:
{{
  "title": "Translated title in {lang_name}",
  "description": "Translated description in {lang_name}",
  "script": "Clean narration script optimized for whiteboard video - just the story text, no formatting",
  "youtube_title": "Engaging YouTube title in {lang_name}",
  "youtube_description": "YouTube description with call-to-action in {lang_name}",
  "tags": "Relevant tags for {lang_name} audience, comma separated",
  "language": "{language_code}",
  "cultural_adaptations": "Brief note about cultural changes made",
  "estimated_duration": 180,
  "readability_score": 9
}}

CRITICAL INSTRUCTIONS:
- Return pure JSON only, no markdown code blocks
- Make script flow naturally for native {lang_name} speakers
- Use these expressions naturally: {', '.join(common_phrases[:5])}
- Optimize for clear, engaging narration over visuals
- Keep the inspirational tone while making it culturally authentic
"""
        return prompt
    
    def translate_story(self, story_data: dict, target_language: str) -> dict:
        """
        Translate a story to target language with cultural adaptation.
        
        Args:
            story_data: Dictionary containing story content and metadata
            target_language: Language code (es, fr, ur, ar)
            
        Returns:
            Dictionary with translated content
        """
        if target_language not in self.supported_languages:
            raise ValueError(f"Language {target_language} not supported. Available: {list(self.supported_languages.keys())}")
        
        logger.info(f"Translating story to {self.supported_languages[target_language]['name']}")
        
        try:
            # Generate translation prompt
            prompt = self.get_translation_prompt(target_language, story_data)
            
            # Call OpenAI API for natural translation
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert cultural translator who creates natural, conversational translations with local slang and expressions. Never do literal translation - always adapt for native speakers."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.7,  # Some creativity for natural language
                max_tokens=3000
            )
            
            # Extract translated content
            translated_content = response.choices[0].message.content.strip()
            
            # Try to parse as JSON, fallback to manual parsing if needed
            try:
                translated_data = json.loads(translated_content)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON response, using fallback parsing")
                translated_data = self._parse_translation_fallback(translated_content, story_data)
            
            # Add translation metadata
            translated_data['translation_metadata'] = {
                'target_language': target_language,
                'language_name': self.supported_languages[target_language]['name'],
                'translated_at': datetime.now().isoformat(),
                'translation_model': 'gpt-4-turbo-preview',
                'cultural_adaptation': True,
                'original_language': 'en'
            }
            
            # Calculate translation cost
            input_tokens = len(prompt.split()) * 1.3  # Rough estimate
            output_tokens = len(translated_content.split()) * 1.3
            estimated_cost = (input_tokens * 0.01 + output_tokens * 0.03) / 1000  # GPT-4 Turbo pricing
            
            translated_data['translation_metadata']['estimated_cost'] = estimated_cost
            
            logger.info(f"Translation completed. Estimated cost: ${estimated_cost:.4f}")
            
            return translated_data
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise
    
    def _parse_translation_fallback(self, content: str, original_data: dict) -> dict:
        """Enhanced fallback parser for clean script format."""
        # Try to extract clean script from response
        script_content = content.strip()
        
        # Remove any markdown formatting if present
        if script_content.startswith('```'):
            lines = script_content.split('\n')
            script_content = '\n'.join(lines[1:-1]) if len(lines) > 2 else content
        
        # Create clean translation with new format
        return {
            'title': original_data.get('title', 'Translated Story'),
            'description': original_data.get('description', 'Translated Description'),
            'script': script_content,  # Clean script ready for narration
            'youtube_title': original_data.get('youtube_title', 'Translated Title'),
            'youtube_description': original_data.get('youtube_description', 'Translated Description'),
            'tags': ', '.join(original_data.get('youtube_tags', [])),
            'language': 'unknown',
            'cultural_adaptations': 'Fallback parsing used',
            'estimated_duration': 180,
            'readability_score': 7
        }
    
    def extract_clean_script(self, story_data: dict) -> str:
        """
        Extract clean script from story data, handling nested JSON formats.
        
        Args:
            story_data: Story data that might contain nested JSON
            
        Returns:
            Clean script text ready for narration
        """
        # Try to get script from new format first
        if 'script' in story_data:
            return story_data['script']
        
        # Handle legacy format with nested JSON
        story_content = story_data.get('story_content', '')
        
        # If story_content is a JSON string, try to parse it
        if isinstance(story_content, str):
            # Check for nested JSON with markdown formatting
            if '```json' in story_content:
                try:
                    import re
                    json_match = re.search(r'```json\s*\n(.*?)\n```', story_content, re.DOTALL)
                    if json_match:
                        nested_content = json.loads(json_match.group(1))
                        return nested_content.get('story_content', nested_content.get('Story Content', story_content))
                except:
                    pass
            
            # Check if it's a direct JSON string
            elif story_content.strip().startswith('{') and story_content.strip().endswith('}'):
                try:
                    parsed = json.loads(story_content)
                    if isinstance(parsed, dict):
                        # Extract story content from parsed JSON
                        content = parsed.get('story_content', '')
                        if not content:
                            # Try alternative key patterns
                            content = parsed.get('Story Content', '')
                            if not content:
                                # Find the longest text value (likely the story)
                                longest_text = ''
                                for value in parsed.values():
                                    if isinstance(value, str) and len(value) > len(longest_text):
                                        longest_text = value
                                content = longest_text if len(longest_text) > 100 else story_content
                        return content
                except json.JSONDecodeError:
                    pass
        
        return story_content
    
    def validate_script_quality(self, script: str, language: str) -> dict:
        """
        Validate script quality for whiteboard video narration.
        
        Args:
            script: Script text to validate
            language: Language code
            
        Returns:
            Dictionary with quality metrics
        """
        metrics = {
            'word_count': len(script.split()),
            'sentence_count': len([s for s in script.split('.') if s.strip()]),
            'avg_sentence_length': 0,
            'estimated_duration': 0,
            'readability_score': 0,
            'whiteboard_ready': False
        }
        
        if metrics['sentence_count'] > 0:
            metrics['avg_sentence_length'] = metrics['word_count'] / metrics['sentence_count']
            
        # Estimate duration based on language (words per minute varies by language)
        wpm_rates = {'es': 180, 'fr': 160, 'ur': 150, 'ar': 140, 'en': 170}
        wpm = wpm_rates.get(language, 160)
        metrics['estimated_duration'] = int((metrics['word_count'] / wpm) * 60)
        
        # Simple readability score (10 = perfect for whiteboard)
        if metrics['avg_sentence_length'] <= 15:
            metrics['readability_score'] = 10
        elif metrics['avg_sentence_length'] <= 20:
            metrics['readability_score'] = 8
        else:
            metrics['readability_score'] = 6
            
        # Check if ready for whiteboard video
        metrics['whiteboard_ready'] = (
            metrics['readability_score'] >= 8 and 
            metrics['estimated_duration'] <= 240 and  # Max 4 minutes
            metrics['word_count'] >= 50  # Minimum content
        )
        
        return metrics
        """
        Translate multiple stories to multiple languages.
        
        Args:
            stories: List of story dictionaries
            target_languages: List of language codes
            
        Returns:
            Dictionary with language codes as keys and translated stories as values
        """
        results = {lang: [] for lang in target_languages}
        total_cost = 0.0
        
        for story in stories:
            story_title = story.get('title', 'Unknown Story')
            logger.info(f"Translating '{story_title}' to {len(target_languages)} languages")
            
            for lang in target_languages:
                try:
                    translated = self.translate_story(story, lang)
                    results[lang].append(translated)
                    
                    # Track cost
                    cost = translated.get('translation_metadata', {}).get('estimated_cost', 0)
                    total_cost += cost
                    
                except Exception as e:
                    logger.error(f"Failed to translate '{story_title}' to {lang}: {str(e)}")
                    continue
        
        logger.info(f"Batch translation completed. Total estimated cost: ${total_cost:.4f}")
        return results
    
    def save_translated_stories(self, translated_stories: Dict[str, List[dict]], base_path: str = "data/stories"):
        """
        Save translated stories to language-specific directories.
        
        Args:
            translated_stories: Dictionary with language codes and story lists
            base_path: Base directory path for saving
        """
        base_dir = Path(base_path)
        base_dir.mkdir(parents=True, exist_ok=True)
        
        for lang_code, stories in translated_stories.items():
            lang_dir = base_dir / lang_code
            lang_dir.mkdir(exist_ok=True)
            
            for i, story in enumerate(stories, 1):
                # Generate filename from title or use index
                title = story.get('title', f'story_{i}')
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_title = safe_title.replace(' ', '_').lower()
                
                filename = f"{safe_title}_{lang_code}.json"
                filepath = lang_dir / filename
                
                # Save with pretty formatting
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(story, f, ensure_ascii=False, indent=2)
                
                logger.info(f"Saved translated story: {filepath}")
        
        logger.info(f"All translated stories saved to {base_path}")
    
    def get_supported_languages(self) -> Dict[str, Dict[str, str]]:
        """Return dictionary of supported languages and their info."""
        return self.supported_languages


def main():
    """Example usage of the Natural Translator."""
    # Example Maya story for testing
    sample_story = {
        "title": "Seeing Signs: A Journey to Inner Strength",
        "description": "Discover how everyday challenges can reveal unexpected paths to personal growth and resilience.",
        "story_content": """
        Meet Maya, a software developer in her early thirties, living in a bustling city. She's dedicated and talented but recently has been feeling lost in the sea of daily demands and competitive pressures at work.

        On this particularly crucial morning, when she has the final interview for a job she's been eyeing at a prestigious startup, her car fails to start. She feels the panic rise, her breath quickens, and a sense of defeat looms over her.

        Maya's immediate reaction is frustration mixed with despair. Her mind races through the consequences of missing this interview. However, as she stands beside her motionless car, her mind starts replaying other recent setbacks: her broken laptop last week, her lost phone, a misunderstanding with a close friend.

        As Maya waits for the tow truck, she scrolls absently through her phone and stumbles upon a video about finding strength and guidance through recognizing life's subtle signs. The message strikes a chord.

        With time to think as she rides the bus to her interview, Maya contemplates her relentless pursuit of career advancement at the expense of her health and happiness. She realizes these disruptions could be nudges towards a more balanced life.

        Maya walks into the interview with a newfound sense of calm and perspective. She answers questions with honesty, expressing not only her skills but also her desire for a work environment that values well-being and creativity.

        Maya's story reminds us to stay open to the signs life offers us, often hidden in disruptions or challenges. Next time you face a setback, take a moment to look deeper. What could life be trying to tell you?
        """,
        "youtube_title": "How Missing My Interview Revealed My True Path",
        "youtube_description": "Discover Maya's transformative journey when a broken car leads her to uncover the hidden signs in life's challenges.",
        "youtube_tags": ["personal growth", "inner strength", "resilience", "life transformation", "career stress", "spiritual journey"]
    }
    
    # Initialize translator
    translator = NaturalTranslator()
    
    # Test translation to Spanish
    try:
        spanish_story = translator.translate_story(sample_story, 'es')
        print("✅ Spanish translation completed!")
        print(f"Title: {spanish_story.get('title', 'N/A')}")
        print(f"Cost: ${spanish_story.get('translation_metadata', {}).get('estimated_cost', 0):.4f}")
        
        # Save test translation
        translator.save_translated_stories({'es': [spanish_story]})
        
    except Exception as e:
        print(f"❌ Translation failed: {e}")


if __name__ == "__main__":
    main()