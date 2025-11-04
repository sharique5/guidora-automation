#!/usr/bin/env python3
"""
Enhanced Whiteboard Thumbnail Generator
Creates sketch-style thumbnails that match whiteboard video content with proper titles and language considerations.
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

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class WhiteboardThumbnailConfig:
    """Configuration for whiteboard-style thumbnail generation."""
    width: int = 1280
    height: int = 720
    quality: int = 95
    format: str = "PNG"
    
    # Whiteboard-specific styling
    style: str = "whiteboard_sketch"  # whiteboard_sketch, hand_drawn, minimal_sketch
    background_color: str = "white"   # White background like whiteboard
    sketch_color: str = "black"       # Black ink/marker style
    accent_color: str = "#2563eb"     # Blue for highlights
    
    # Text overlay settings
    use_youtube_title: bool = True    # Use YouTube title instead of story title
    title_position: str = "bottom"    # top, bottom, center
    title_style: str = "bold_modern"  # bold_modern, handwritten, clean
    font_size_ratio: float = 0.08     # Relative to image height
    
    # Language strategy
    language_strategy: str = "universal"  # universal, localized, english_only
    
    # Provider preferences
    primary_provider: str = "openai"
    fallback_providers: List[str] = None

class WhiteboardThumbnailGenerator:
    """Enhanced thumbnail generator for whiteboard-style videos."""
    
    def __init__(self, config: WhiteboardThumbnailConfig = None):
        """Initialize whiteboard thumbnail generator."""
        self.config = config or WhiteboardThumbnailConfig()
        self.base_path = Path(__file__).parent.parent.parent
        self.thumbnails_path = self.base_path / "assets" / "thumbnails"
        self.thumbnails_path.mkdir(parents=True, exist_ok=True)
        
        # API keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.stability_api_key = os.getenv('STABILITY_API_KEY')
        
        # Language-specific considerations for thumbnails
        self.language_thumbnail_strategy = {
            "en": {
                "text_needed": True,
                "primary_market": True,
                "style_preference": "modern_clean"
            },
            "es": {
                "text_needed": False,  # Can use English thumbnail
                "primary_market": False,
                "style_preference": "warm_inviting"
            },
            "fr": {
                "text_needed": False,  # Can use English thumbnail  
                "primary_market": False,
                "style_preference": "elegant_minimal"
            },
            "ur": {
                "text_needed": True,   # Different script, needs localized
                "primary_market": False,
                "style_preference": "ornate_respectful"
            }
        }
    
    def get_correct_title(self, story_data: Dict, language: str) -> str:
        """Get the correct title for thumbnail based on configuration."""
        if self.config.use_youtube_title:
            # Try to get language-specific YouTube title from story content
            story_content = story_data.get('story_content', '')
            if isinstance(story_content, str) and 'YouTube Title' in story_content:
                try:
                    # Parse the nested JSON in story_content
                    import re
                    json_match = re.search(r'```json\n(.*?)\n```', story_content, re.DOTALL)
                    if json_match:
                        nested_data = json.loads(json_match.group(1))
                        youtube_title = nested_data.get('YouTube Title', '')
                        if youtube_title:
                            return youtube_title
                except:
                    pass
            
            # Fallback to top-level youtube_title
            youtube_title = story_data.get('youtube_title', '')
            if youtube_title:
                return youtube_title
        
        # Final fallback to story title
        return story_data.get('title', 'Inspirational Story')
    
    def should_create_localized_thumbnail(self, language: str) -> bool:
        """Determine if this language needs its own thumbnail."""
        if self.config.language_strategy == "universal":
            return language == "en"  # Only create English, use for all
        elif self.config.language_strategy == "localized":
            return self.language_thumbnail_strategy[language]["text_needed"]
        else:  # english_only
            return language == "en"
    
    def generate_whiteboard_prompt(self, story_data: Dict, language: str) -> str:
        """Generate optimized prompt for whiteboard-style thumbnail."""
        title = self.get_correct_title(story_data, language)
        description = story_data.get('description', '')
        themes = story_data.get('themes', [])
        
        # Extract key visual elements
        visual_elements = self._extract_story_visuals(story_data)
        
        prompt = f"""Create a compelling YouTube thumbnail in whiteboard/sketch style for the video "{title}".

WHITEBOARD STYLE REQUIREMENTS:
- Style: Hand-drawn sketch on white background (like whiteboard animation)
- Colors: Primarily black ink/markers with blue accent highlights
- Feel: Clean, educational, inspirational
- Technique: Simple line art, not photorealistic
- Background: Pure white or off-white (whiteboard style)

COMPOSITION:
- Dimensions: {self.config.width}x{self.config.height} (YouTube thumbnail ratio)
- Central focus: Key visual element from the story
- Visual hierarchy: Clear focal point with supporting elements
- Space for text: Leave clear area at bottom for title overlay

STORY ELEMENTS TO VISUALIZE:
- Main theme: {', '.join(themes) if themes else 'personal growth and inner strength'}
- Key visuals: {visual_elements}
- Mood: Inspirational, hopeful, educational
- Target: Adults seeking personal development

VISUAL STYLE:
- Line art: Clean, confident strokes
- Shading: Minimal crosshatching or simple shadows
- Highlights: Strategic blue accents on key elements
- Clarity: Must be readable at small thumbnail size
- Professional: YouTube-quality educational content style

AVOID:
- Photorealistic rendering
- Complex backgrounds
- Too many small details
- Dark or cluttered compositions
- Text in the image (will be added separately)

The thumbnail should immediately convey transformation and growth while maintaining the clean, educational whiteboard aesthetic."""
        
        return prompt
    
    def _extract_story_visuals(self, story_data: Dict) -> str:
        """Extract key visual elements from story content for thumbnail."""
        # Get story content
        story_content = story_data.get('story_content', '')
        description = story_data.get('description', '')
        title = story_data.get('title', '')
        
        # Look for visual keywords in the content
        text_to_analyze = f"{title} {description} {story_content}".lower()
        
        # Story-specific visual mapping
        if 'signs' in text_to_analyze and 'journey' in text_to_analyze:
            return "person at crossroads with subtle signs and arrows, journey path, inner strength symbolism"
        elif 'interview' in text_to_analyze and 'car' in text_to_analyze:
            return "professional person, broken car, transformation moment, new perspective"
        else:
            return "person in contemplative moment, journey symbolism, growth and transformation"
    
    def generate_with_openai(self, prompt: str) -> Optional[bytes]:
        """Generate whiteboard thumbnail using OpenAI DALL-E 3."""
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
    
    def add_title_overlay(self, image_bytes: bytes, title: str, language: str) -> bytes:
        """Add properly formatted title overlay to thumbnail."""
        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            draw = ImageDraw.Draw(image)
            
            # Calculate font size based on image height
            font_size = int(image.height * self.config.font_size_ratio)
            
            # Load font
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Prepare title (limit length for readability)
            if len(title) > 60:
                title = title[:57] + "..."
            
            # Get text dimensions
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position text at bottom with padding
            padding = 20
            x = (image.width - text_width) // 2
            y = image.height - text_height - padding
            
            # Create background rectangle for better readability
            rect_padding = 10
            rect_coords = [
                x - rect_padding,
                y - rect_padding,
                x + text_width + rect_padding,
                y + text_height + rect_padding
            ]
            
            # Draw semi-transparent background
            overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle(rect_coords, fill=(255, 255, 255, 200))
            
            # Composite overlay
            image = Image.alpha_composite(image.convert('RGBA'), overlay)
            draw = ImageDraw.Draw(image)
            
            # Draw text with outline for better visibility
            outline_width = 2
            
            # Draw outline
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    draw.text((x + adj_x, y + adj_y), title, font=font, fill="black")
            
            # Draw main text
            draw.text((x, y), title, font=font, fill="#2563eb")  # Blue text
            
            # Convert back to RGB
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            
            # Save to bytes
            output = io.BytesIO()
            image.save(output, format=self.config.format, quality=self.config.quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Title overlay failed: {e}")
            return image_bytes
    
    def generate_thumbnail(self, story_data: Dict, language: str, video_id: str) -> Optional[str]:
        """Generate whiteboard-style thumbnail with proper title."""
        
        # Check if we should create a localized thumbnail
        if not self.should_create_localized_thumbnail(language):
            # Use English thumbnail for this language
            english_thumbnail = self.thumbnails_path / "en" / f"{video_id.replace(f'_{language}', '_en')}_thumbnail.{self.config.format.lower()}"
            if english_thumbnail.exists():
                logger.info(f"Using English thumbnail for {language}: {english_thumbnail}")
                return str(english_thumbnail)
        
        # Generate new thumbnail
        prompt = self.generate_whiteboard_prompt(story_data, language)
        
        logger.info(f"Generating whiteboard thumbnail for {video_id} ({language})")
        
        # Generate with OpenAI
        image_data = self.generate_with_openai(prompt)
        
        if not image_data:
            logger.error("Failed to generate thumbnail image")
            return None
        
        # Get correct title and add overlay
        title = self.get_correct_title(story_data, language)
        image_data = self.add_title_overlay(image_data, title, language)
        
        # Save thumbnail
        filename = f"{video_id}_thumbnail.{self.config.format.lower()}"
        filepath = self.thumbnails_path / language / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        logger.info(f"Whiteboard thumbnail saved: {filepath}")
        logger.info(f"Title used: {title}")
        logger.info(f"Cost: $0.040")
        
        return str(filepath)
    
    def get_thumbnail_strategy_report(self) -> str:
        """Generate report on thumbnail strategy for different languages."""
        report = """# Thumbnail Strategy Report

## Language Strategy: {}

""".format(self.config.language_strategy.title())
        
        for lang, config in self.language_thumbnail_strategy.items():
            lang_name = {"en": "English", "es": "Spanish", "fr": "French", "ur": "Urdu"}[lang]
            
            report += f"### {lang_name} ({lang.upper()})\n"
            
            if self.should_create_localized_thumbnail(lang):
                report += f"- ✅ **Generate localized thumbnail**\n"
                report += f"- Style: {config['style_preference']}\n"
                report += f"- Text: Language-specific title\n"
            else:
                report += f"- 🔄 **Use English thumbnail**\n"
                report += f"- Reason: Visual content is universal\n"
                report += f"- Saves: $0.040 per video\n"
            
            report += f"\n"
        
        if self.config.language_strategy == "universal":
            report += """## Benefits of Universal Strategy:
- ✅ Cost effective: $0.040 instead of $0.160 per story
- ✅ Consistent branding across languages
- ✅ Visual content is universal (whiteboard style)
- ✅ Faster production workflow
- ⚠️ Consider localized for Urdu (different script)

## When to Use Localized:
- Text-heavy thumbnails
- Different cultural contexts
- Script differences (Arabic, Urdu, etc.)
"""
        
        return report

def main():
    """Demo the enhanced whiteboard thumbnail system."""
    print("🎨 ENHANCED WHITEBOARD THUMBNAIL GENERATOR")
    print("=" * 70)
    
    # Test different strategies
    strategies = ["universal", "localized"]
    
    for strategy in strategies:
        config = WhiteboardThumbnailConfig(language_strategy=strategy)
        generator = WhiteboardThumbnailGenerator(config)
        
        print(f"\n📊 {strategy.upper()} STRATEGY:")
        print("-" * 40)
        
        report = generator.get_thumbnail_strategy_report()
        print(report)

if __name__ == "__main__":
    main()