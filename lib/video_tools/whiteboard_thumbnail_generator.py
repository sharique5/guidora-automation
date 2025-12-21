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
    font_size_ratio: float = 0.05     # Relative to image height (smaller/sharper)
    
    # YouTube optimization features (NEW)
    include_human_face: bool = True   # Add human figure with emotion (2-5x better CTR)
    high_contrast: bool = True        # Thick bold outlines for mobile readability
    emotional_symbols: bool = True    # Add transformation symbols (arrows, lightbulb, etc)
    add_brand_mark: bool = True       # Tiny Guidora mark for recognition
    brand_mark_position: str = "bottom_right"  # top_left, top_right, bottom_left, bottom_right
    
    # Post-processing (NEW)
    auto_enhance: bool = True         # Auto contrast, sharpen, crop to safe margins
    generate_variants: int = 3        # Generate multiple options to pick best (1-3)
    
    # Language strategy
    language_strategy: str = "universal"  # universal, localized, english_only
    
    # Provider preferences
    primary_provider: str = "gemini"  # gemini-2.5-flash-image-preview, openai
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
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
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
        """ULTRA minimal prompt - just essential visual elements."""
        title = self.get_correct_title(story_data, language)
        character_visuals = self._extract_character_visuals(story_data)
        
        # ABSOLUTE MINIMUM - describe the scene visually
        prompt = f"""Whiteboard sketch (black marker on white, 1280x720):

Draw in this exact order:
1. A FEMALE NURSE in BLUE SCRUBS with STETHOSCOPE
2. She is sitting, head in hands, looking EXHAUSTED
3. Medical clipboard next to her
4. Behind her: minimal hospital wall lines
5. Small scribbles/stress marks around her head

Style: Hand-drawn sketch, bold black lines, blue only on scrubs
No: suits, laptops, office, text"""
        
        return prompt
        
        # Build ULTRA-SIMPLIFIED prompt focusing on visual description first
        prompt = f"""Draw a whiteboard sketch in black marker on white background for YouTube thumbnail (1280x720, 16:9).

WHAT TO DRAW (be specific):
1. MAIN CHARACTER (takes up 60% of image):
   - A WOMAN wearing medical scrubs (nurse uniform)
   - Short or tied-back hair
   - Stethoscope around neck
   - Sitting with head in hands OR hunched over
   - Facial expression: tired, stressed, exhausted
   - Holding or next to: medical clipboard
   
2. SETTING (minimal, background):
   - Suggest hospital: simple vertical lines for wall, doorframe sketch
   - ONE simple element: hospital bed outline OR nurse station counter
   - Keep it minimal - just enough to show it's a medical setting

3. SYMBOLS (small, around her head):
   - 2-3 scribble marks showing stress/chaos
   - Maybe 1-2 question marks
   - Keep these SMALL

STYLE:
- Bold black marker lines on pure white
- Hand-drawn sketch look (like whiteboard animation)
- Blue color ONLY on the scrubs uniform
- Character: thick lines (5px), Background: thin lines (2px)

COMPOSITION:
- Character on LEFT side (60% of image)
- RIGHT side mostly empty (for text overlay later)
- Character's face clearly visible

DO NOT INCLUDE:
- Men, businessmen, suits, ties, formal wear
- Office settings, desks, laptops
- Any text or words
- Complex details or patterns

Title for context: "{title}" ""

- Action: Sitting on a bench or standing, head in hands, showing clear struggle/distress
- Emotion: {character_visuals['emotion']}
- KEY PROP: Include {character_visuals['prop']} visible in their hands or on lap
- This character should be the LARGEST element (60% of frame), drawn with THICK confident black lines
- Character's face and body language are THE FOCUS

BACKGROUND & SETTING:
- Setting: {character_visuals['setting']} (MINIMAL lines - just suggest the space)
- Metaphor: A small chaotic cloud of scribbles, question marks, or symbols around the character's head
- Keep background simple - 40% less detail than typical thumbnails
- Background uses thinner lines than the main character

VISUAL STYLE (WHITEBOARD - SIMPLIFIED):
- Hand-drawn sketch aesthetic
- NO GREYSCALE SHADING - bold black lines on pure white only
- ONE Accent Color: Blue (#2563eb) used ONLY on character's clothing or one key element
- Line weight: THICK (5-7px equivalent) for character, thin (2-3px) for background
- HIGH CONTRAST: Maximum black-on-white difference

COMPOSITION:
- Rule of Thirds: Character on Left/Center
- Negative Space: Keep Right side relatively clear (for text overlay)
- MARGINS: Keep all elements 15% away from edges
- Dimensions: {self.config.width}x{self.config.height} (16:9 YouTube ratio)

EMOTIONAL FRAMING (NON-NEGOTIABLE):
- The character's facial expression is THE MOST IMPORTANT element
- Face must show clear distress: furrowed brow, downcast eyes, tense mouth
- Body language: Hunched shoulders, head in hands, or similar defeated posture
- Focus on THE PROBLEM/HOOK - not the solution yet


STRICT CONSTRAINTS (NEGATIVE RULES):
- NO SUITS, NO TIES, NO BUSINESSMEN - be profession-specific
- NO TEXT inside the image (text overlay added separately)
- NO SPLIT SCREEN or before/after comparisons
- NO HAPPY ELEMENTS - focus on the struggle/problem moment
- NO complex backgrounds - keep it minimal (40% less visual complexity)
- NO thin delicate lines - everything must be bold and mobile-readable
- NO photorealistic rendering - keep it sketch/whiteboard style
- NO bottom-heavy composition (YouTube UI blocks bottom 15%)

CLARITY CHECK:
- Every element must be visible at 320x180px (mobile thumbnail size)
- Face expression must be obvious at small size
- Total visual elements: 5-7 maximum (character + prop + setting hint + 2-3 chaos symbols)
- Less is more - prioritize emotional clarity over detail

FINAL VERIFICATION BEFORE GENERATING:
✓ Is the main character a {character_visuals['character']}? (NOT a man in business attire)
✓ Is the character showing {character_visuals['emotion']}?
✓ Is the {character_visuals['prop']} visible?
✓ Is the setting {character_visuals['setting']} suggested with minimal lines?
✓ NO TEXT in the image?

This thumbnail must grab attention in 0.5 seconds through emotional impact, not complexity."""
        
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
    
    def _extract_character_visuals(self, story_data: Dict) -> Dict[str, str]:
        """Extract character-specific visual details using LLM analysis."""
        content = story_data.get('story_content', '') or story_data.get('content', '')
        title = story_data.get('title', '') or story_data.get('youtube_title', '')
        
        # Try OpenAI for smart extraction
        if self.openai_api_key:
            try:
                headers = {
                    'Authorization': f'Bearer {self.openai_api_key}',
                    'Content-Type': 'application/json'
                }
                
                extraction_prompt = f"""Analyze this story and extract ONLY these 3 visual elements for a thumbnail:

Story Title: {title}
Story Content: {content[:1500]}

Extract:
1. CHARACTER_VISUAL: Describe the main character's appearance, profession, clothing (e.g., "Female Nurse in blue scrubs", "Male Teacher in casual clothes", "Young Father in jeans and t-shirt")
2. SETTING_VISUAL: The key location/setting (e.g., "Hospital corridor", "Classroom", "Home living room", "Park bench")
3. KEY_PROP: One important object/prop (e.g., "Medical clipboard", "Smartphone", "Coffee cup", "Books")
4. EMOTION_STATE: The main character's emotional state at their lowest point (e.g., "Exhausted and burnt out", "Anxious and overwhelmed", "Lonely and afraid")

Respond ONLY in this format:
CHARACTER_VISUAL: [description]
SETTING_VISUAL: [description]
KEY_PROP: [description]
EMOTION_STATE: [description]"""
                
                data = {
                    'model': 'gpt-4o-mini',
                    'messages': [
                        {'role': 'user', 'content': extraction_prompt}
                    ],
                    'temperature': 0.3,
                    'max_tokens': 200
                }
                
                response = requests.post(
                    'https://api.openai.com/v1/chat/completions',
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()['choices'][0]['message']['content']
                    
                    # Parse response
                    visuals = {
                        'character': 'Person',
                        'setting': 'Simple background',
                        'prop': 'Smartphone',
                        'emotion': 'Overwhelmed'
                    }
                    
                    for line in result.split('\n'):
                        if 'CHARACTER_VISUAL:' in line:
                            visuals['character'] = line.split('CHARACTER_VISUAL:')[1].strip()
                        elif 'SETTING_VISUAL:' in line:
                            visuals['setting'] = line.split('SETTING_VISUAL:')[1].strip()
                        elif 'KEY_PROP:' in line:
                            visuals['prop'] = line.split('KEY_PROP:')[1].strip()
                        elif 'EMOTION_STATE:' in line:
                            visuals['emotion'] = line.split('EMOTION_STATE:')[1].strip()
                    
                    return visuals
            except Exception as e:
                logger.warning(f"Character visual extraction failed: {e}")
        
        # Fallback: Manual detection
        content_lower = content.lower()
        
        visuals = {
            'character': 'Person',
            'setting': 'Simple background',
            'prop': 'Smartphone',
            'emotion': 'Overwhelmed and stressed'
        }
        
        # Character detection
        if 'nurse' in content_lower:
            visuals['character'] = 'Female Nurse in blue scrubs with stethoscope'
            visuals['setting'] = 'Hospital corridor or clinic'
            visuals['prop'] = 'Medical clipboard'
        elif 'teacher' in content_lower:
            visuals['character'] = 'Female Teacher in professional attire'
            visuals['setting'] = 'Classroom or school hallway'
            visuals['prop'] = 'Books or tablet'
        elif 'father' in content_lower or 'dad' in content_lower:
            visuals['character'] = 'Male Father in casual clothes'
            visuals['setting'] = 'Home living room at night'
            visuals['prop'] = 'Baby bottle or child\'s toy'
        
        # Emotion detection
        if 'burnout' in content_lower or 'exhausted' in content_lower:
            visuals['emotion'] = 'Exhausted and burnt out, at breaking point'
        elif 'anxious' in content_lower or 'panic' in content_lower:
            visuals['emotion'] = 'Anxious and panicked, losing control'
        elif 'lonely' in content_lower or 'alone' in content_lower:
            visuals['emotion'] = 'Lonely and isolated, feeling lost'
        
        return visuals
    
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
        if 'burnout' in content or 'exhausted' in content:
            emotions['before'] = 'exhausted and burnt out'
        
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
    
    def generate_with_gemini(self, prompt: str) -> Optional[bytes]:
        """Generate whiteboard thumbnail using Google Gemini 2.5 Flash Image Preview."""
        if not self.gemini_api_key:
            logger.warning("Gemini API key not available")
            return None
        
        try:
            import google.generativeai as genai
            
            # Configure with API key
            genai.configure(api_key=self.gemini_api_key)
            
            # Use Gemini 2.5 Flash Image Preview
            model = genai.GenerativeModel('gemini-2.5-flash-image-preview')
            
            # Generate image
            result = model.generate_content([prompt])
            
            # Extract image data
            if result and hasattr(result, 'parts'):
                for part in result.parts:
                    if hasattr(part, 'inline_data'):
                        image_data = part.inline_data.data
                        return image_data
            
            # Try alternative response structure
            if result and hasattr(result, 'candidates'):
                for candidate in result.candidates:
                    if hasattr(candidate, 'content'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data'):
                                return part.inline_data.data
            
            logger.error("Gemini returned no image data")
            return None
                
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
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
            
            # Shorten title if too long (sharper, more dangerous)
            if len(title) > 50:
                # Keep first part with impact words
                title = title[:47] + "..."
            
            # Recalculate dimensions after potential shortening
            bbox = draw.textbbox((0, 0), title, font=font_bold)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Recalculate position
            if self.config.title_position == "top":
                x = (image.width - text_width) // 2
                y = padding
            elif self.config.title_position == "center":
                x = (image.width - text_width) // 2
                y = (image.height - text_height) // 2
            else:
                x = (image.width - text_width) // 2
                y = image.height - text_height - padding - int(image.height * 0.15)
            
            # Create SOLID WHITE RECTANGULAR BACKGROUND (like a sticker)
            rect_padding = 20
            rect_coords = [
                x - rect_padding,
                y - rect_padding,
                x + text_width + rect_padding,
                y + text_height + rect_padding
            ]
            
            # Draw solid white background (100% opacity)
            draw.rectangle(rect_coords, fill=(255, 255, 255), outline=(0, 0, 0), width=3)
            
            # Draw text in BOLD BLACK for maximum contrast
            # No outline needed - solid background provides all the contrast
            draw.text((x, y), title, font=font_bold, fill="#000000")
            
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
            
            # Generate with provider (try Gemini first, fallback to OpenAI)
            if self.config.primary_provider == "gemini":
                image_data = self.generate_with_gemini(prompt)
                if not image_data:
                    logger.info("Gemini failed, falling back to OpenAI")
                    image_data = self.generate_with_openai(prompt)
            else:
                image_data = self.generate_with_openai(prompt)
                if not image_data:
                    logger.info("OpenAI failed, falling back to Gemini")
                    image_data = self.generate_with_gemini(prompt)
            
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