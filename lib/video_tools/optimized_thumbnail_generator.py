#!/usr/bin/env python3
"""
Optimized Whiteboard Thumbnail Generator - Addressing user feedback:
1. Text strategy: Keep engaging text for YouTube CTR
2. Visual tone: Secular, professional, life-coaching (not religious/preachy)
"""

import os
import sys
import json
from typing import Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from dotenv import load_dotenv
import openai

class OptimizedThumbnailConfig:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.use_youtube_title = True
        self.language_strategy = "universal"  # Generate EN, copy to others
        self.include_text_overlay = True      # Keep text for CTR
        self.tone = "secular_professional"    # Not religious/preachy

class OptimizedThumbnailGenerator:
    def __init__(self):
        load_dotenv()
        self.config = OptimizedThumbnailConfig()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Ensure thumbnails directory exists
        self.thumbnail_dir = os.path.join('assets', 'thumbnails')
        os.makedirs(self.thumbnail_dir, exist_ok=True)

    def generate_optimized_prompt(self, story_data: Dict, language: str) -> str:
        """Generate optimized prompt addressing user feedback"""
        
        title = self.get_correct_title(story_data, language)
        
        # Extract themes but keep them secular and professional
        themes = self._extract_secular_themes(story_data)
        visual_elements = self._extract_professional_visuals(story_data)
        
        prompt = f"""Create a compelling YouTube thumbnail in clean whiteboard/sketch style for the video "{title}".

VISUAL TONE - SECULAR & PROFESSIONAL:
- Style: Modern life coaching / professional development
- Feel: Motivational, empowering, business-friendly
- Avoid: Religious imagery, spiritual symbols, preachy elements
- Target: Young professionals seeking personal growth

WHITEBOARD STYLE:
- Hand-drawn sketch on white background
- Colors: Black ink with strategic blue accents
- Clean, minimalist, educational aesthetic
- Simple line art (not photorealistic)

ENGAGING COMPOSITION FOR HIGH CTR:
- Dimensions: {self.config.width}x{self.config.height}
- Central focus: Relatable professional scenario
- Visual metaphors: Growth arrows, lightbulb moments, pathway success
- Clear space at bottom for engaging title text overlay

STORY ELEMENTS TO VISUALIZE:
- Main theme: {', '.join(themes)}
- Key visuals: {visual_elements}
- Mood: Confident, solution-oriented, achievable
- Context: Modern workplace/life challenges and victories

PROFESSIONAL VISUAL ELEMENTS:
- Business casual person(s) in relatable situations
- Modern minimalist icons (arrows, graphs, lightbulbs)
- Clean geometric shapes and lines
- Success/transformation metaphors
- Accessible, non-intimidating imagery

TEXT STRATEGY:
- Reserve clear space for title overlay
- Title will be: "{title}"
- Text should be readable and clickable
- Focus on benefit/outcome rather than process

AVOID COMPLETELY:
- Religious symbols or imagery
- Spiritual/mystical elements
- Preachy or sermon-like visuals
- Dark or heavy emotional themes
- Complex philosophical concepts

The thumbnail should feel like a TED talk or professional development course - inspiring but grounded, motivational but practical."""

        return prompt

    def get_correct_title(self, story_data: Dict, language: str) -> str:
        """Get the correct title for thumbnail"""
        if self.config.use_youtube_title:
            youtube_title = story_data.get('youtube_title', '')
            if youtube_title:
                return youtube_title
        
        # Fallback to story title but make it more engaging
        title = story_data.get('title', 'Transform Your Mindset')
        return self._make_title_engaging(title)

    def _make_title_engaging(self, title: str) -> str:
        """Convert generic titles to engaging, clickable ones"""
        engaging_patterns = {
            'journey': 'The Surprising Path to',
            'strength': 'Build Unshakeable',
            'growth': 'Unlock Your Hidden',
            'signs': 'The Hidden Signs That Changed Everything',
            'morning': 'The 5-Minute Morning Habit That',
            'gratitude': 'Why This Simple Practice'
        }
        
        for pattern, replacement in engaging_patterns.items():
            if pattern.lower() in title.lower():
                return replacement + ' ' + title.split()[-1].capitalize()
        
        return title

    def _extract_secular_themes(self, story_data: Dict) -> list:
        """Extract themes but keep them secular and professional"""
        secular_themes = [
            'professional development',
            'mindset transformation', 
            'workplace success',
            'life optimization',
            'productivity improvement',
            'career advancement',
            'personal effectiveness',
            'goal achievement'
        ]
        
        # Default to professional themes
        return secular_themes[:3]

    def _extract_professional_visuals(self, story_data: Dict) -> str:
        """Extract professional, secular visual elements"""
        return "modern professional in business setting, upward trending arrows, lightbulb insights, clean workspace, success pathway, achievement celebration"

    def generate_thumbnail(self, story_data: Dict, language: str, video_id: str) -> Optional[str]:
        """Generate optimized thumbnail with secular, professional approach"""
        
        try:
            # Generate the optimized prompt
            prompt = self.generate_optimized_prompt(story_data, language)
            
            print(f"🎯 Generating OPTIMIZED thumbnail for {language.upper()}")
            print(f"📝 Style: Secular, professional, engaging")
            
            # Call OpenAI API (using closest supported size)
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1792x1024",  # Closest to 1280x720 ratio
                quality="standard",
                n=1
            )
            
            # Download and resize the image to YouTube thumbnail dimensions
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            
            # Resize to proper YouTube thumbnail dimensions
            image = image.resize((self.config.width, self.config.height), Image.Resampling.LANCZOS)
            
            # Create language-specific directory
            lang_dir = os.path.join(self.thumbnail_dir, language)
            os.makedirs(lang_dir, exist_ok=True)
            
            # Save thumbnail
            filename = f"{video_id}_optimized_thumbnail.png"
            filepath = os.path.join(lang_dir, filename)
            image.save(filepath)
            
            # Add text overlay if configured
            if self.config.include_text_overlay:
                filepath = self._add_text_overlay(filepath, story_data, language)
            
            return os.path.abspath(filepath)
            
        except Exception as e:
            print(f"❌ Error generating optimized thumbnail: {e}")
            return None

    def _add_text_overlay(self, image_path: str, story_data: Dict, language: str) -> str:
        """Add engaging text overlay to thumbnail"""
        try:
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            
            # Get engaging title
            title = self.get_correct_title(story_data, language)
            
            # Try to load a font, fallback to default if not available
            try:
                font = ImageFont.truetype("arial.ttf", 48)
                small_font = ImageFont.truetype("arial.ttf", 32)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Add main title at bottom
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position text at bottom with background
            x = (image.width - text_width) // 2
            y = image.height - text_height - 40
            
            # Add semi-transparent background for text
            draw.rectangle([x-20, y-10, x+text_width+20, y+text_height+10], 
                         fill=(255, 255, 255, 200))
            
            # Add text
            draw.text((x, y), title, fill=(0, 0, 0), font=font)
            
            # Save with text overlay
            overlay_path = image_path.replace('.png', '_with_text.png')
            image.save(overlay_path)
            
            return overlay_path
            
        except Exception as e:
            print(f"⚠️ Could not add text overlay: {e}")
            return image_path

def main():
    """Test the optimized thumbnail generator"""
    
    print("🎯 OPTIMIZED THUMBNAIL GENERATOR TEST")
    print("Addressing: Secular tone + Engaging text strategy")
    print("=" * 60)
    
    # Test data
    test_video = {
        "story_number": 1,
        "title": "Seeing Signs: A Journey to Inner Strength", 
        "youtube_title": "The Hidden Signs That Changed My Career Forever",
        "youtube_description": "How missing one interview led to discovering my true professional path",
        "language": "en",
        "video_filename": "optimized_test.mp4"
    }
    
    generator = OptimizedThumbnailGenerator()
    
    # Test prompt generation
    print("📝 Testing Optimized Prompt:")
    prompt = generator.generate_optimized_prompt(test_video, 'en')
    print("-" * 40)
    print(prompt[:500] + "...")
    print("-" * 40)
    
    print("\n✅ Key Improvements:")
    print("1. 🎯 Secular, professional tone (not religious/preachy)")
    print("2. 📝 Engaging text overlay for higher CTR")
    print("3. 💼 Modern workplace/life coaching aesthetic")
    print("4. 🚀 Clickable, benefit-focused titles")
    
    # Generate actual thumbnail
    print(f"\n🔄 Generating optimized thumbnail...")
    result = generator.generate_thumbnail(test_video, 'en', 'optimized_test')
    
    if result:
        print(f"✅ Success: {result}")
    else:
        print("❌ Generation failed")

if __name__ == "__main__":
    main()