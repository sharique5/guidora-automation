#!/usr/bin/env python3
"""
Video Branding Outro System
Creates consistent 5-7 second call-to-action outros with channel logo and subscribe messages
for all language channels to improve brand recognition and engagement.
"""

import json
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class OutroConfig:
    """Configuration for video outro branding."""
    duration_seconds: int = 6
    logo_path: str = "assets/branding/channel_logo.png"
    background_color: str = "#1a1a1a"  # Dark background
    text_color: str = "#ffffff"       # White text
    accent_color: str = "#ff4444"     # YouTube red for subscribe button
    font_family: str = "Arial Bold"
    font_size: int = 24
    logo_size_percent: int = 25       # Logo takes 25% of screen width
    animation_style: str = "fade_in"  # fade_in, slide_up, zoom_in

class BrandingOutro:
    """Manages video outro branding across all languages."""
    
    def __init__(self, base_path: str = None):
        """Initialize branding outro system."""
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent.parent
        self.config_path = self.base_path / "config" / "branding_outro.json"
        self.assets_path = self.base_path / "assets" / "branding"
        
        # Ensure directories exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.assets_path.mkdir(parents=True, exist_ok=True)
        
        # Load or create configuration
        self.config = self._load_or_create_config()
        
        # Multi-language outro messages
        self.outro_messages = {
            "en": {
                "main_text": "Thank you for watching!",
                "subscribe_text": "Like, Share & Subscribe for more inspirational content",
                "channel_name": "Guidora Mindfulness"
            },
            "es": {
                "main_text": "¡Gracias por ver!",
                "subscribe_text": "Dale like, comparte y suscríbete para más contenido inspirador",
                "channel_name": "Guidora Mindfulness"
            },
            "fr": {
                "main_text": "Merci d'avoir regardé !",
                "subscribe_text": "Aimez, partagez et abonnez-vous pour plus de contenu inspirant",
                "channel_name": "Guidora Mindfulness"
            },
            "ur": {
                "main_text": "دیکھنے کا شکریہ!",
                "subscribe_text": "مزید متاثرکن مواد کے لیے لائک، شیئر اور سبسکرائب کریں",
                "channel_name": "Guidora Mindfulness"
            },
            "ar": {
                "main_text": "شكراً لك على المشاهدة!",
                "subscribe_text": "اضغط إعجاب، شارك واشترك للمزيد من المحتوى الملهم",
                "channel_name": "Guidora Mindfulness"
            }
        }
    
    def _load_or_create_config(self) -> OutroConfig:
        """Load existing config or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                return OutroConfig(**config_data)
            except Exception as e:
                logger.warning(f"Failed to load outro config: {e}. Using defaults.")
        
        # Create default config
        config = OutroConfig()
        self._save_config(config)
        return config
    
    def _save_config(self, config: OutroConfig):
        """Save outro configuration."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save outro config: {e}")
    
    def generate_outro_script(self, language: str) -> str:
        """Generate outro script text for specific language."""
        if language not in self.outro_messages:
            logger.warning(f"Language {language} not supported. Using English.")
            language = "en"
        
        messages = self.outro_messages[language]
        
        outro_script = f"""
[OUTRO SEGMENT - {self.config.duration_seconds} seconds]

VISUAL: 
- Channel logo appears center-screen ({self.config.logo_size_percent}% width)
- Dark background ({self.config.background_color})
- Smooth {self.config.animation_style} animation

AUDIO & TEXT:
"{messages['main_text']}"

[PAUSE 1 second]

"{messages['subscribe_text']}"

VISUAL ELEMENTS:
- Subscribe button animation (YouTube red)
- Like and Share icons with gentle pulse effect
- Channel name: "{messages['channel_name']}"

[END OUTRO]
"""
        return outro_script
    
    def generate_instadoodle_outro_instructions(self, language: str) -> Dict[str, str]:
        """Generate specific instructions for Instadoodle outro creation."""
        if language not in self.outro_messages:
            language = "en"
        
        messages = self.outro_messages[language]
        
        return {
            "duration": f"{self.config.duration_seconds} seconds",
            "scene_description": f"""
Create a professional outro scene with:

BACKGROUND:
- Solid dark background ({self.config.background_color})
- Clean, minimalist design

MAIN ELEMENTS:
1. Channel logo (centered, prominent)
2. Text: "{messages['main_text']}" (appears first)
3. Text: "{messages['subscribe_text']}" (appears after 1 second)
4. Subscribe button visual (YouTube red color)
5. Like and Share icons

ANIMATION:
- Logo fades in smoothly
- Text appears with gentle slide-up effect
- Subscribe button has subtle pulse animation
- Professional, clean transitions

BRANDING:
- Channel name: "{messages['channel_name']}"
- Consistent with YouTube branding standards
- Encourages engagement without being pushy
""",
            "voice_script": f'"{messages["main_text"]}" [pause] "{messages["subscribe_text"]}"',
            "visual_elements": [
                "Channel logo (center)",
                "Thank you message",
                "Subscribe call-to-action",
                "Like and Share icons",
                "Channel name"
            ]
        }
    
    def update_outro_messages(self, language: str, messages: Dict[str, str]):
        """Update outro messages for specific language."""
        if language in self.outro_messages:
            self.outro_messages[language].update(messages)
            # Save updated messages to config file
            self._save_outro_messages()
            logger.info(f"Updated outro messages for {language}")
        else:
            logger.error(f"Language {language} not supported")
    
    def _save_outro_messages(self):
        """Save outro messages to separate file."""
        messages_file = self.config_path.parent / "outro_messages.json"
        try:
            with open(messages_file, 'w', encoding='utf-8') as f:
                json.dump(self.outro_messages, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save outro messages: {e}")
    
    def get_outro_for_video(self, video_id: str, language: str) -> Dict[str, str]:
        """Get complete outro package for specific video."""
        return {
            "video_id": video_id,
            "language": language,
            "script": self.generate_outro_script(language),
            "instadoodle_instructions": self.generate_instadoodle_outro_instructions(language),
            "duration_seconds": self.config.duration_seconds,
            "assets_needed": [
                "Channel logo PNG (transparent background)",
                "Subscribe button icon",
                "Like icon", 
                "Share icon"
            ]
        }
    
    def export_all_outros(self) -> Dict[str, Dict]:
        """Export outro configurations for all languages."""
        all_outros = {}
        
        for language in self.outro_messages.keys():
            all_outros[language] = self.get_outro_for_video(
                video_id=f"generic_outro_{language}",
                language=language
            )
        
        # Save to file
        export_file = self.base_path / "data" / "outro_exports.json"
        export_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(all_outros, f, indent=2, ensure_ascii=False)
            logger.info(f"Exported all outros to {export_file}")
        except Exception as e:
            logger.error(f"Failed to export outros: {e}")
        
        return all_outros
    
    def create_assets_checklist(self) -> str:
        """Create checklist for required branding assets."""
        return f"""
# Branding Assets Checklist

## Required Files:
- [ ] Channel logo (PNG, transparent background, 1080x1080px minimum)
  - Save as: `assets/branding/channel_logo.png`

- [ ] Subscribe button icon (PNG, 200x60px)
  - Save as: `assets/branding/subscribe_button.png`

- [ ] Like icon (PNG, 64x64px)
  - Save as: `assets/branding/like_icon.png`

- [ ] Share icon (PNG, 64x64px)
  - Save as: `assets/branding/share_icon.png`

## Design Guidelines:
- Use your brand colors consistently
- Ensure logo is clear at small sizes
- Icons should be simple and recognizable
- All PNGs should have transparent backgrounds

## Instadoodle Setup:
1. Upload all assets to your Instadoodle media library
2. Create a template outro scene
3. Use the generated instructions for each language
4. Test outro timing ({self.config.duration_seconds} seconds total)

## File Structure:
```
assets/
  branding/
    channel_logo.png
    subscribe_button.png
    like_icon.png
    share_icon.png
```
"""

def main():
    """Demo the branding outro system."""
    outro_system = BrandingOutro()
    
    print("🎨 Branding Outro System")
    print("=" * 50)
    
    # Export all outros
    all_outros = outro_system.export_all_outros()
    
    print(f"✅ Generated outros for {len(all_outros)} languages")
    
    # Show example for English
    english_outro = outro_system.get_outro_for_video("demo_video", "en")
    print("\n📝 Example English Outro:")
    print(english_outro["script"])
    
    # Create assets checklist
    checklist = outro_system.create_assets_checklist()
    checklist_file = outro_system.base_path / "docs" / "BRANDING_ASSETS_CHECKLIST.md"
    checklist_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(checklist_file, 'w', encoding='utf-8') as f:
        f.write(checklist)
    
    print(f"\n📋 Assets checklist created: {checklist_file}")
    print("\n🎬 Ready to add professional outros to your videos!")

if __name__ == "__main__":
    main()