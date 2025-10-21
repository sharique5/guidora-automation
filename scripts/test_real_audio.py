#!/usr/bin/env python3
"""
Test script to generate a real audio file using OpenAI TTS
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.tts_manager import create_default_tts_manager

def test_real_audio_generation():
    """Test generating a real audio file that can be played."""
    
    print("🎵 Testing Real Audio Generation")
    print("=" * 40)
    
    # Create TTS manager
    manager = create_default_tts_manager()
    
    # Sample story for testing
    test_story = {
        "id": "real_audio_test",
        "title": "Mindfulness Test",
        "content": """Good morning. Take a deep breath and let yourself be present in this moment. 
        Notice how your body feels as you sit or stand. 
        Feel the air entering and leaving your lungs. 
        This simple practice of awareness can transform your day."""
    }
    
    print(f"📝 Story: {test_story['title']}")
    print(f"📊 Content length: {len(test_story['content'])} characters")
    
    try:
        # Generate audio with OpenAI
        print(f"\n🎤 Generating audio with OpenAI TTS...")
        audio_file = manager.generate_audio(
            story=test_story, 
            audience="universal",
            preferred_provider="openai"
        )
        
        if audio_file and audio_file.file_path:
            print(f"✅ Audio generated successfully!")
            print(f"📁 File: {audio_file.file_path}")
            print(f"⏱️ Duration: {audio_file.duration_seconds:.1f} seconds")
            print(f"💰 Cost: ${audio_file.generation_cost:.4f}")
            print(f"🔊 Provider: {audio_file.provider}")
            print(f"🎭 Voice: {audio_file.voice_used}")
            print(f"📏 File size: {audio_file.file_size_bytes:,} bytes")
            
            # Check if file exists and has content
            if os.path.exists(audio_file.file_path):
                file_size = os.path.getsize(audio_file.file_path)
                print(f"✅ File exists on disk: {file_size:,} bytes")
                
                # Try to identify file type
                with open(audio_file.file_path, 'rb') as f:
                    header = f.read(10)
                    if header.startswith(b'ID3') or b'MP3' in header:
                        print("🎵 File format: MP3")
                    elif header.startswith(b'RIFF'):
                        print("🎵 File format: WAV")
                    else:
                        print(f"🎵 File header: {header}")
                
                return audio_file.file_path
            else:
                print(f"❌ File not found on disk: {audio_file.file_path}")
                return None
        else:
            print(f"❌ Audio generation failed")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    audio_path = test_real_audio_generation()
    
    if audio_path:
        print(f"\n🎉 Success! Audio file generated: {audio_path}")
        print(f"💡 You can now play this file with any audio player")
    else:
        print(f"\n❌ Audio generation failed")
        print(f"🔧 Check your OpenAI API key and internet connection")