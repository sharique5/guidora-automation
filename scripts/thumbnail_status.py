#!/usr/bin/env python3
"""
Simple Thumbnail Status Checker
Test thumbnail generation capabilities and provider availability.
"""

import sys
import os
from pathlib import Path

# Add the lib directory to the path
sys.path.append(str(Path(__file__).parent.parent / "lib"))

from video_tools.thumbnail_generator import ThumbnailGenerator

def main():
    """Check thumbnail generation status and capabilities."""
    print("🎨 THUMBNAIL GENERATION STATUS")
    print("=" * 60)
    
    # Initialize generator
    generator = ThumbnailGenerator()
    
    # Check provider status
    provider_status = generator.get_provider_status()
    
    print("📊 Provider Availability:")
    total_available = 0
    
    for provider, status in provider_status.items():
        if status['available']:
            icon = "✅"
            total_available += 1
        else:
            icon = "❌"
        
        recommended = "⭐" if status['recommended'] else "  "
        cost = f"${status['cost_per_image']:.3f}/image"
        
        print(f"{recommended} {icon} {provider.upper():>10}: {cost} - {status['best_for']}")
    
    print(f"\n📈 Summary:")
    print(f"   Available providers: {total_available}/3")
    print(f"   Recommended setup: OpenAI + Stability AI")
    print(f"   Estimated cost per batch (5 thumbnails): $0.20 - $0.30")
    
    # Check for missing API keys and provide setup guidance
    print(f"\n🔧 Setup Status:")
    
    if generator.openai_api_key:
        print("   ✅ OpenAI API key configured")
    else:
        print("   ❌ OpenAI API key missing")
        print("      Add OPENAI_API_KEY to your .env file")
    
    if generator.stability_api_key:
        print("   ✅ Stability AI API key configured") 
    else:
        print("   ⚠️  Stability AI API key missing (optional but recommended)")
        print("      Add STABILITY_API_KEY to your .env file")
    
    if generator.gemini_api_key:
        print("   ✅ Gemini API key configured")
    else:
        print("   ℹ️  Gemini API key missing (optional)")
        print("      Add GEMINI_API_KEY to your .env file for free tier")
    
    # Provide next steps
    print(f"\n💡 Next Steps:")
    
    if total_available == 0:
        print("   1. Add at least OPENAI_API_KEY to your .env file")
        print("   2. Optionally add STABILITY_API_KEY for backup/cost savings")
        print("   3. Test with: python scripts/thumbnail_test.py generate")
    elif total_available == 1:
        print("   1. Consider adding STABILITY_API_KEY for redundancy")
        print("   2. Test thumbnail generation for your current batch")
        print("   3. Ready for production thumbnail generation!")
    else:
        print("   ✅ You're ready for production thumbnail generation!")
        print("   1. Test with single video first")
        print("   2. Then generate batch thumbnails for all languages")
        print("   3. Integrate with your video production workflow")
    
    # Show example commands
    print(f"\n🚀 Example Commands:")
    print("   # Generate single thumbnail")
    print("   python scripts/thumbnail_test.py generate story_001_en")
    print("   ")
    print("   # Generate batch thumbnails")  
    print("   python scripts/thumbnail_test.py batch")

if __name__ == "__main__":
    main()