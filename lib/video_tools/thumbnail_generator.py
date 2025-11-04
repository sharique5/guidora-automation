#!/usr/bin/env python3
"""
Multi-Language Thumbnail Generator
Creates compelling thumbnails using multiple AI providers with language-specific visual elements.
Supports OpenAI DALL-E, Stability AI, and Google Gemini for optimal results and cost efficiency.
"""

import os
import json
import base64
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from PIL import Image, ImageDraw, ImageFont
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class ThumbnailConfig:
    """Configuration for thumbnail generation."""
    width: int = 1280
    height: int = 720
    quality: int = 95
    format: str = "PNG"
    
    # Style preferences
    style: str = "photorealistic"  # photorealistic, illustration, cartoon, minimalist
    mood: str = "inspirational"    # inspirational, calm, energetic, dramatic
    color_scheme: str = "warm"     # warm, cool, vibrant, muted, brand
    
    # Text overlay settings
    include_title_overlay: bool = True
    title_position: str = "bottom"  # top, bottom, center, none
    title_style: str = "bold"       # bold, elegant, modern, handwritten
    
    # Provider preferences
    primary_provider: str = "openai"     # openai, stability, gemini
    fallback_providers: List[str] = None
    max_retries: int = 3

class ThumbnailGenerator:
    """Multi-provider AI thumbnail generator for video content."""
    
    def __init__(self, config: ThumbnailConfig = None):
        """Initialize thumbnail generator with multi-provider support."""
        self.config = config or ThumbnailConfig()
        self.base_path = Path(__file__).parent.parent.parent
        self.thumbnails_path = self.base_path / "assets" / "thumbnails"
        self.thumbnails_path.mkdir(parents=True, exist_ok=True)
        
        # API keys from environment
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.stability_api_key = os.getenv('STABILITY_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Language-specific visual elements
        self.language_styles = {
            "en": {
                "font_style": "modern",
                "color_preference": "blue_orange",
                "cultural_elements": "universal symbols",
                "text_position": "bottom_center"
            },
            "es": {
                "font_style": "warm",
                "color_preference": "orange_red",
                "cultural_elements": "warm tones",
                "text_position": "bottom_center"
            },
            "fr": {
                "font_style": "elegant",
                "color_preference": "blue_gold",
                "cultural_elements": "sophisticated",
                "text_position": "center"
            },
            "ur": {
                "font_style": "ornate",
                "color_preference": "green_gold",
                "cultural_elements": "geometric patterns",
                "text_position": "top_center"
            }
        }
        
        # Provider configurations
        self.providers = {
            "openai": {
                "available": bool(self.openai_api_key),
                "cost_per_image": 0.040,  # DALL-E 3 standard
                "quality": "high",
                "best_for": "photorealistic, detailed"
            },
            "stability": {
                "available": bool(self.stability_api_key),
                "cost_per_image": 0.020,  # Stable Diffusion
                "quality": "good",
                "best_for": "artistic, illustrations"
            },
            "gemini": {
                "available": bool(self.gemini_api_key),
                "cost_per_image": 0.000,  # Free tier available
                "quality": "medium",
                "best_for": "simple, concept-based"
            }
        }
    
    def generate_thumbnail_prompt(self, story_data: Dict, language: str) -> str:
        """Generate optimized prompt for thumbnail creation."""
        title = story_data.get('title', 'Inspirational Story')
        description = story_data.get('description', '')
        themes = story_data.get('themes', [])
        characters = story_data.get('characters', [])
        setting = story_data.get('setting', 'general')
        
        # Get language-specific styling
        lang_style = self.language_styles.get(language, self.language_styles['en'])
        
        # Extract key visual elements from story
        visual_elements = self._extract_visual_elements(story_data)
        
        prompt = f"""Create a compelling YouTube thumbnail for a {self.config.mood} story titled "{title}".

VISUAL REQUIREMENTS:
- Dimensions: {self.config.width}x{self.config.height} (YouTube thumbnail ratio)
- Style: {self.config.style} with {lang_style['font_style']} aesthetic
- Mood: {self.config.mood} and engaging
- Color scheme: {lang_style['color_preference']} tones

STORY ELEMENTS:
- Main theme: {', '.join(themes) if themes else 'personal growth'}
- Characters: {', '.join(characters) if characters else 'relatable person'}
- Setting: {setting}
- Key visuals: {visual_elements}

COMPOSITION:
- Eye-catching central focal point
- Clear visual hierarchy
- High contrast for readability
- Emotional expression that conveys {self.config.mood}
- Cultural sensitivity for {language} audience
- Include subtle {lang_style['cultural_elements']}

TECHNICAL:
- High resolution and sharp details
- Bright, vibrant colors that stand out
- Optimized for small display sizes (mobile thumbnails)
- Professional, polished appearance
- No text overlay (will be added separately)

The thumbnail should immediately convey the transformative and inspiring nature of the story while being culturally appropriate for {language} speakers."""
        
        return prompt
    
    def _extract_visual_elements(self, story_data: Dict) -> str:
        """Extract key visual elements from story content."""
        # Try to get story content
        story_content = story_data.get('story_content', '')
        description = story_data.get('description', '')
        
        # Look for visual keywords
        visual_keywords = []
        
        # Common visual elements in inspirational stories
        keywords_to_check = [
            'car', 'city', 'office', 'journey', 'path', 'light', 'mountain',
            'road', 'sunrise', 'sunset', 'bridge', 'door', 'window', 'mirror',
            'book', 'tree', 'flower', 'ocean', 'sky', 'star', 'moon'
        ]
        
        text_to_search = (story_content + ' ' + description).lower()
        
        for keyword in keywords_to_check:
            if keyword in text_to_search:
                visual_keywords.append(keyword)
        
        if visual_keywords:
            return ', '.join(visual_keywords[:3])  # Limit to top 3
        else:
            return 'person in contemplative moment, soft lighting, hopeful atmosphere'
    
    def generate_with_openai(self, prompt: str) -> Optional[bytes]:
        """Generate thumbnail using OpenAI DALL-E 3."""
        if not self.openai_api_key:
            logger.warning("OpenAI API key not available")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'dall-e-3',
                'prompt': prompt,
                'n': 1,
                'size': '1792x1024',  # Close to 16:9 ratio
                'quality': 'hd',
                'response_format': 'b64_json'
            }
            
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_data = base64.b64decode(result['data'][0]['b64_json'])
                return image_data
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            return None
    
    def generate_with_stability(self, prompt: str) -> Optional[bytes]:
        """Generate thumbnail using Stability AI."""
        if not self.stability_api_key:
            logger.warning("Stability AI API key not available")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.stability_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'text_prompts': [{'text': prompt}],
                'cfg_scale': 7,
                'height': 720,
                'width': 1280,
                'samples': 1,
                'steps': 30
            }
            
            response = requests.post(
                'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image',
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_data = base64.b64decode(result['artifacts'][0]['base64'])
                return image_data
            else:
                logger.error(f"Stability AI error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Stability AI generation failed: {e}")
            return None
    
    def generate_with_gemini(self, prompt: str) -> Optional[bytes]:
        """Generate thumbnail using Google Gemini (placeholder - requires implementation)."""
        logger.info("Gemini integration placeholder - implement with Google AI Studio API")
        return None
    
    def add_text_overlay(self, image_bytes: bytes, title: str, language: str) -> bytes:
        """Add text overlay to thumbnail image."""
        if not self.config.include_title_overlay:
            return image_bytes
        
        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            draw = ImageDraw.Draw(image)
            
            # Get language-specific styling
            lang_style = self.language_styles.get(language, self.language_styles['en'])
            
            # Calculate text size and position
            font_size = max(60, min(80, len(title) // 2))  # Adaptive font size
            
            try:
                # Try to load a good font
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
            
            # Get text dimensions
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position based on language preference
            if lang_style['text_position'] == 'bottom_center':
                x = (image.width - text_width) // 2
                y = image.height - text_height - 40
            elif lang_style['text_position'] == 'top_center':
                x = (image.width - text_width) // 2
                y = 40
            else:  # center
                x = (image.width - text_width) // 2
                y = (image.height - text_height) // 2
            
            # Add text with outline for better readability
            outline_width = 3
            
            # Draw outline
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    draw.text((x + adj_x, y + adj_y), title, font=font, fill="black")
            
            # Draw main text
            draw.text((x, y), title, font=font, fill="white")
            
            # Save back to bytes
            output = io.BytesIO()
            image.save(output, format=self.config.format, quality=self.config.quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Text overlay failed: {e}")
            return image_bytes
    
    def generate_thumbnail(self, story_data: Dict, language: str, 
                          video_id: str) -> Optional[str]:
        """Generate thumbnail for story using best available provider."""
        
        # Generate optimized prompt
        prompt = self.generate_thumbnail_prompt(story_data, language)
        
        # Try providers in order of preference
        providers_to_try = [self.config.primary_provider]
        if self.config.fallback_providers:
            providers_to_try.extend(self.config.fallback_providers)
        else:
            # Default fallback order
            all_providers = ['openai', 'stability', 'gemini']
            providers_to_try.extend([p for p in all_providers if p != self.config.primary_provider])
        
        image_data = None
        used_provider = None
        
        for provider in providers_to_try:
            if not self.providers[provider]['available']:
                continue
                
            logger.info(f"Attempting thumbnail generation with {provider}")
            
            try:
                if provider == 'openai':
                    image_data = self.generate_with_openai(prompt)
                elif provider == 'stability':
                    image_data = self.generate_with_stability(prompt)
                elif provider == 'gemini':
                    image_data = self.generate_with_gemini(prompt)
                
                if image_data:
                    used_provider = provider
                    break
                    
            except Exception as e:
                logger.error(f"Provider {provider} failed: {e}")
                continue
        
        if not image_data:
            logger.error("All providers failed to generate thumbnail")
            return None
        
        # Add text overlay if enabled
        title = story_data.get('youtube_title', story_data.get('title', ''))
        if title and self.config.include_title_overlay:
            image_data = self.add_text_overlay(image_data, title, language)
        
        # Save thumbnail
        filename = f"{video_id}_thumbnail.{self.config.format.lower()}"
        filepath = self.thumbnails_path / language / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        # Log generation details
        cost = self.providers[used_provider]['cost_per_image']
        logger.info(f"Thumbnail generated: {filepath} (${cost:.3f} via {used_provider})")
        
        return str(filepath)
    
    def generate_batch_thumbnails(self, stories_batch: List[Dict]) -> Dict[str, str]:
        """Generate thumbnails for a batch of stories."""
        results = {}
        total_cost = 0
        
        for story_info in stories_batch:
            try:
                thumbnail_path = self.generate_thumbnail(
                    story_info['story_data'],
                    story_info['language'],
                    story_info['video_id']
                )
                
                if thumbnail_path:
                    results[story_info['video_id']] = thumbnail_path
                    # Add to cost tracking
                    provider_used = self.config.primary_provider
                    total_cost += self.providers[provider_used]['cost_per_image']
                
            except Exception as e:
                logger.error(f"Failed to generate thumbnail for {story_info['video_id']}: {e}")
        
        logger.info(f"Batch complete: {len(results)} thumbnails generated (${total_cost:.3f} total)")
        return results
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all thumbnail generation providers."""
        status = {}
        
        for provider, config in self.providers.items():
            status[provider] = {
                'available': config['available'],
                'cost_per_image': config['cost_per_image'],
                'quality': config['quality'],
                'best_for': config['best_for'],
                'recommended': provider == self.config.primary_provider
            }
        
        return status

def main():
    """Demo thumbnail generation system."""
    print("🎨 Multi-Language Thumbnail Generator")
    print("=" * 60)
    
    # Check provider availability
    generator = ThumbnailGenerator()
    provider_status = generator.get_provider_status()
    
    print("📊 Provider Status:")
    for provider, status in provider_status.items():
        available = "✅" if status['available'] else "❌"
        recommended = "⭐" if status['recommended'] else "  "
        print(f"{recommended} {available} {provider.upper()}: ${status['cost_per_image']:.3f}/image - {status['best_for']}")
    
    print(f"\n💡 Recommendation: Use OpenAI as primary with Stability AI as fallback")
    print(f"💰 Estimated cost per batch (5 thumbnails): $0.20 - $0.30")

if __name__ == "__main__":
    main()