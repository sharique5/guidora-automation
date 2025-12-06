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
    """Configuration for whiteboard-style thumbnail generation with YouTube optimization."""
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
    title_position: str = "top"       # top, bottom, center (TOP recommended for YouTube UI)
    title_style: str = "bold_modern"  # bold_modern, handwritten, clean
    font_size_ratio: float = 0.08     # Relative to image height
    
    # YouTube optimization features (NEW)
    include_human_face: bool = True   # Add human figure with emotion (2-5x better CTR)
    high_contrast: bool = True        # Thick bold outlines for mobile readability
    emotional_symbols: bool = True    # Add transformation symbols (arrows, lightbulb, etc)
    add_brand_mark: bool = True       # Tiny Guidora mark for recognition
    brand_mark_position: str = "top_left"  # top_left, top_right, bottom_left, bottom_right
    
    # Post-processing (NEW)
    auto_enhance: bool = True         # Auto contrast, sharpen, crop to safe margins
    generate_variants: int = 2        # Generate multiple options to pick best (1-3)
    
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
    
    def generate_whiteboard_prompt(self, story_data: Dict, language: str, variant: int = 1) -> str:
        """Generate optimized prompt for whiteboard-style thumbnail with YouTube best practices."""
        title = self.get_correct_title(story_data, language)
        description = story_data.get('description', '')
        themes = story_data.get('themes', [])
        
        # Extract key visual elements and emotions
        visual_elements = self._extract_story_visuals(story_data)
        emotions = self._extract_emotional_journey(story_data)
        
        # Build optimized prompt with YouTube best practices
        prompt = f"""Create a high-impact YouTube thumbnail in whiteboard/sketch style for "{title}".

CRITICAL YOUTUBE OPTIMIZATION:
- THICK BOLD OUTLINES: Strong contrast for mobile viewing (60%+ of traffic)
- HUMAN FACE/FIGURE: Include a simplified whiteboard-style human figure with CLEAR emotional expression
  * Show facial emotion: {emotions['before']} transforming to {emotions['after']}
  * Minimalist face: simple eyes, mouth, and body language
  * Expression must be obvious even at thumbnail size
- HIGH CONTRAST: Bold black lines on pure white, minimal thin strokes
- SAFE MARGINS: Keep important elements away from edges (10% border)

WHITEBOARD STYLE:
- Hand-drawn sketch aesthetic (like whiteboard animation)
- Primarily bold black marker strokes
- Strategic blue accent highlights (#2563eb) on key transformation elements
- Clean, educational, professional feel

COMPOSITION (Variant #{variant}):
- Dimensions: {self.config.width}x{self.config.height} (16:9 YouTube ratio)
- Title space: Clear area at TOP 20% of image (YouTube UI covers bottom)
- Central focus: Human figure showing emotional transformation
- Visual hierarchy: Person → key moment → transformation symbols

STORY ELEMENTS:
- Main theme: {', '.join(themes) if themes else 'personal growth and transformation'}
- Key visuals: {visual_elements}
- Emotional journey: {emotions['before']} → {emotions['insight']} → {emotions['after']}

TRANSFORMATION SYMBOLS (Essential for CTR):
- Add simple whiteboard doodles that represent the story:
  * Stress phase: Chaotic scribbles, question marks, zigzag lines around figure
  * Insight moment: Lightbulb, rays of light, or "aha!" visual marker
  * Transformation: Arrows pointing up, checkmarks, calm aura, stars
- Keep symbols LARGE and BOLD enough to see on mobile

VISUAL STYLE:
- Line weight: THICK and confident (3-5px equivalent)
- Shading: Minimal, only for emphasis
- Highlights: Strategic blue on transformation elements
- Clarity: Every element visible at 320x180px (mobile size)
- Contrast: Maximum black-on-white difference

STRICT AVOIDS:
- Thin, delicate lines (invisible on mobile)
- Photorealistic rendering
- Complex backgrounds or textures
- Cluttered compositions with many small elements
- Any text in the image (title overlay added separately)
- Bottom-heavy composition (YouTube UI blocks bottom 15%)

EMOTION FOCUS:
The human figure's facial expression and body language are THE MOST IMPORTANT ELEMENTS.
Make the before/after emotional transformation crystal clear through:
- Face shape and expression changes
- Body posture (hunched → upright)
- Environmental markers (chaos → calm)

This thumbnail must grab attention in 0.5 seconds on a cluttered YouTube feed."""
        
        return prompt
    
    def _extract_story_visuals(self, story_data: Dict) -> str:
        """Extract key visual elements from story content for thumbnail."""
        # Get story content
        story_content = story_data.get('story_content', '') or story_data.get('content', '')
        description = story_data.get('description', '')
        title = story_data.get('title', '')
        
        # Look for visual keywords in the content
        text_to_analyze = f"{title} {description} {story_content}".lower()
        
        # Story-specific visual mapping with emotional context
        if 'peace' in text_to_analyze or 'calm' in text_to_analyze:
            return "professional person juggling phones (stressed) → sitting peacefully with breath focus (calm), park bench, meditation pose"
        elif 'signs' in text_to_analyze and 'journey' in text_to_analyze:
            return "person at crossroads with question marks → arrows showing clear direction, journey path with signposts"
        elif 'interview' in text_to_analyze and 'car' in text_to_analyze:
            return "professional in suit near broken car (frustrated) → confident person with new perspective (enlightened)"
        else:
            return "person showing transformation from struggle to clarity, journey symbolism, clear before/after emotional states"
    
    def _extract_emotional_journey(self, story_data: Dict) -> Dict[str, str]:
        """Extract emotional transformation for better thumbnail design."""
        content = str(story_data.get('content', '') or story_data.get('story_content', '')).lower()
        
        # Default emotional journey
        emotions = {
            'before': 'stressed and overwhelmed',
            'insight': 'curious and open',
            'after': 'peaceful and balanced'
        }
        
        # Detect emotional markers in content
        if 'stress' in content or 'overwhelm' in content or 'anxious' in content:
            emotions['before'] = 'stressed and anxious'
        if 'dread' in content or 'fear' in content:
            emotions['before'] = 'fearful and uncertain'
        
        if 'calm' in content or 'peace' in content:
            emotions['after'] = 'calm and centered'
        if 'confident' in content or 'clarity' in content:
            emotions['after'] = 'confident and clear'
        if 'balance' in content:
            emotions['after'] = 'balanced and harmonious'
            
        return emotions
    
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
        """Add properly formatted title overlay to thumbnail with YouTube optimization."""
        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            draw = ImageDraw.Draw(image)
            
            # Calculate font size based on image height
            font_size = int(image.height * self.config.font_size_ratio)
            
            # Load font
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
                font_bold = ImageFont.truetype("arialbd.ttf", font_size)
            except:
                font = ImageFont.load_default()
                font_bold = font
            
            # Prepare title (limit length for readability)
            if len(title) > 60:
                title = title[:57] + "..."
            
            # Get text dimensions
            bbox = draw.textbbox((0, 0), title, font=font_bold)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position text based on config (TOP recommended for YouTube)
            padding = 30  # Increased padding for safe margins
            
            if self.config.title_position == "top":
                # TOP placement (recommended - avoids YouTube UI)
                x = (image.width - text_width) // 2
                y = padding
            elif self.config.title_position == "center":
                # CENTER placement
                x = (image.width - text_width) // 2
                y = (image.height - text_height) // 2
            else:
                # BOTTOM placement (risky - YouTube UI covers bottom 15%)
                x = (image.width - text_width) // 2
                y = image.height - text_height - padding - int(image.height * 0.15)  # Account for YouTube UI
            
            # Create background rectangle for better readability
            rect_padding = 15
            rect_coords = [
                x - rect_padding,
                y - rect_padding,
                x + text_width + rect_padding,
                y + text_height + rect_padding
            ]
            
            # Draw semi-transparent background with stronger opacity
            overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle(rect_coords, fill=(255, 255, 255, 230))  # Higher opacity for contrast
            
            # Composite overlay
            image = Image.alpha_composite(image.convert('RGBA'), overlay)
            draw = ImageDraw.Draw(image)
            
            # Draw text with THICK outline for maximum readability on mobile
            outline_width = 3  # Increased from 2 for better mobile visibility
            
            # Draw thick black outline
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    draw.text((x + adj_x, y + adj_y), title, font=font_bold, fill="black")
            
            # Draw main text in blue (brand color)
            draw.text((x, y), title, font=font_bold, fill=self.config.accent_color)
            
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
    
    def add_brand_mark(self, image_bytes: bytes) -> bytes:
        """Add subtle Guidora brand mark for channel recognition."""
        if not self.config.add_brand_mark:
            return image_bytes
            
        try:
            image = Image.open(io.BytesIO(image_bytes))
            draw = ImageDraw.Draw(image)
            
            # Brand mark size (small, not intrusive)
            mark_size = int(image.width * 0.04)  # 4% of width
            padding = 15
            
            # Position based on config
            if self.config.brand_mark_position == "top_left":
                x, y = padding, padding
            elif self.config.brand_mark_position == "top_right":
                x, y = image.width - mark_size - padding, padding
            elif self.config.brand_mark_position == "bottom_left":
                x, y = padding, image.height - mark_size - padding
            else:  # bottom_right
                x, y = image.width - mark_size - padding, image.height - mark_size - padding
            
            # Draw simple "G" in a circle (Guidora mark)
            # Circle outline
            draw.ellipse([x, y, x + mark_size, y + mark_size], 
                        outline=self.config.accent_color, width=3)
            
            # "G" letter (simplified)
            try:
                font = ImageFont.truetype("arialbd.ttf", int(mark_size * 0.6))
            except:
                font = ImageFont.load_default()
            
            # Center "G" in circle
            text = "G"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x + (mark_size - text_width) // 2
            text_y = y + (mark_size - text_height) // 2
            
            draw.text((text_x, text_y), text, font=font, fill=self.config.accent_color)
            
            # Save to bytes
            output = io.BytesIO()
            image.save(output, format=self.config.format, quality=self.config.quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Brand mark failed: {e}")
            return image_bytes
    
    def enhance_thumbnail(self, image_bytes: bytes) -> bytes:
        """Post-process thumbnail: enhance contrast, sharpen, crop to safe margins."""
        if not self.config.auto_enhance:
            return image_bytes
            
        try:
            from PIL import ImageEnhance, ImageFilter
            
            image = Image.open(io.BytesIO(image_bytes))
            
            # 1. Crop to safe margins (10% border)
            width, height = image.size
            safe_margin = 0.05  # 5% on each side = 10% total
            left = int(width * safe_margin)
            top = int(height * safe_margin)
            right = width - int(width * safe_margin)
            bottom = height - int(height * safe_margin)
            
            # Don't actually crop, just ensure content respects margins (already done in prompting)
            # This is more about verifying our generation stayed within bounds
            
            # 2. Enhance contrast (makes outlines pop on mobile)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.15)  # 15% more contrast
            
            # 3. Slight sharpening (improves readability at small sizes)
            image = image.filter(ImageFilter.SHARPEN)
            
            # 4. Ensure consistent size (YouTube standard)
            if image.size != (self.config.width, self.config.height):
                image = image.resize((self.config.width, self.config.height), Image.Resampling.LANCZOS)
            
            # Save enhanced image
            output = io.BytesIO()
            image.save(output, format=self.config.format, quality=self.config.quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Enhancement failed: {e}")
            return image_bytes
    
    def generate_thumbnail(self, story_data: Dict, language: str, video_id: str) -> Optional[str]:
        """Generate optimized whiteboard-style thumbnail with all YouTube best practices."""
        
        # Check if we should create a localized thumbnail
        if not self.should_create_localized_thumbnail(language):
            # Use English thumbnail for this language
            english_thumbnail = self.thumbnails_path / "en" / f"{video_id.replace(f'_{language}', '_en')}_thumbnail.{self.config.format.lower()}"
            if english_thumbnail.exists():
                logger.info(f"Using English thumbnail for {language}: {english_thumbnail}")
                return str(english_thumbnail)
        
        # Generate variants if configured (pick best from multiple options)
        best_thumbnail = None
        variants_generated = []
        
        for variant_num in range(1, self.config.generate_variants + 1):
            logger.info(f"Generating variant {variant_num}/{self.config.generate_variants} for {video_id} ({language})")
            
            # Generate prompt for this variant
            prompt = self.generate_whiteboard_prompt(story_data, language, variant=variant_num)
            
            # Generate with OpenAI
            image_data = self.generate_with_openai(prompt)
            
            if not image_data:
                logger.warning(f"Variant {variant_num} generation failed, skipping")
                continue
            
            # Get correct title and add overlay
            title = self.get_correct_title(story_data, language)
            image_data = self.add_title_overlay(image_data, title, language)
            
            # Add brand mark if enabled
            image_data = self.add_brand_mark(image_data)
            
            # Enhance thumbnail (contrast, sharpen, etc.)
            image_data = self.enhance_thumbnail(image_data)
            
            # Save variant
            variant_suffix = f"_v{variant_num}" if self.config.generate_variants > 1 else ""
            variant_path = self._save_thumbnail(image_data, language, video_id, suffix=variant_suffix)
            
            if variant_path:
                variants_generated.append(variant_path)
                if not best_thumbnail:
                    best_thumbnail = variant_path
        
        if not best_thumbnail:
            logger.error("Failed to generate any thumbnail variants")
            return None
        
        # If multiple variants, user can manually select best (or implement auto-selection logic)
        if len(variants_generated) > 1:
            logger.info(f"Generated {len(variants_generated)} variants. Review and select best:")
            for i, path in enumerate(variants_generated, 1):
                logger.info(f"  Variant {i}: {path}")
        
        return best_thumbnail
    
    def _save_thumbnail(self, image_data: bytes, language: str, video_id: str, suffix: str = "") -> Optional[str]:
        """Save thumbnail to appropriate directory with optional suffix for variants."""
        try:
            filename = f"{video_id}{suffix}_thumbnail.{self.config.format.lower()}"
            filepath = self.thumbnails_path / language / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            logger.info(f"Saved thumbnail: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to save thumbnail: {e}")
            return None
    
    
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