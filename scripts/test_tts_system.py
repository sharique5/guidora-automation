#!/usr/bin/env python3
"""
TTS System Test Script
Comprehensive testing of the TTS pipeline with sample data
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.tts_manager import create_default_tts_manager
from lib.jsonl_utils import load_jsonl

class TTSSystemTester:
    """Comprehensive testing for the TTS system."""
    
    def __init__(self):
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "errors": []
        }
        
        # Create test data directory
        self.test_dir = Path("test_audio_output")
        self.test_dir.mkdir(exist_ok=True)
        
        print("🧪 TTS System Testing Suite")
        print("=" * 50)
    
    def run_all_tests(self):
        """Run comprehensive test suite."""
        
        # Test 1: Manager initialization
        self.test_manager_initialization()
        
        # Test 2: Provider availability
        self.test_provider_availability()
        
        # Test 3: Voice selection system
        self.test_voice_selection()
        
        # Test 4: Cost estimation
        self.test_cost_estimation()
        
        # Test 5: Sample audio generation
        self.test_sample_audio_generation()
        
        # Test 6: Story processing from JSONL
        self.test_story_processing()
        
        # Test 7: Provider comparison
        self.test_provider_comparison()
        
        # Final results
        self.print_test_results()
    
    def test_manager_initialization(self):
        """Test TTS manager initialization."""
        print("\n🔧 Test 1: Manager Initialization")
        
        try:
            self.manager = create_default_tts_manager()
            available_providers = self.manager.get_available_providers()
            
            if len(available_providers) > 0:
                print(f"   ✅ Manager initialized with {len(available_providers)} providers")
                print(f"   📋 Available: {', '.join(available_providers)}")
                self.record_test_pass()
            else:
                print(f"   ❌ No providers available")
                self.record_test_fail("No TTS providers initialized")
                
        except Exception as e:
            print(f"   ❌ Manager initialization failed: {e}")
            self.record_test_fail(f"Manager init error: {e}")
    
    def test_provider_availability(self):
        """Test individual provider functionality."""
        print("\n🏭 Test 2: Provider Availability")
        
        if not hasattr(self, 'manager'):
            self.record_test_fail("Manager not available for provider testing")
            return
        
        for provider_name in self.manager.get_available_providers():
            try:
                info = self.manager.get_provider_info(provider_name)
                
                if info:
                    print(f"   ✅ {provider_name}: {info['available_voices']} voices")
                    if info['voice_samples']:
                        for voice in info['voice_samples']:
                            print(f"      - {voice['name']} ({voice['gender']})")
                    self.record_test_pass()
                else:
                    print(f"   ❌ {provider_name}: No info available")
                    self.record_test_fail(f"{provider_name} info unavailable")
                    
            except Exception as e:
                print(f"   ❌ {provider_name}: {e}")
                self.record_test_fail(f"{provider_name} error: {e}")
    
    def test_voice_selection(self):
        """Test voice selection for different audiences."""
        print("\n🎤 Test 3: Voice Selection System")
        
        if not hasattr(self, 'manager'):
            self.record_test_fail("Manager not available for voice testing")
            return
        
        audiences = ["universal", "muslim_community", "spiritual_seekers"]
        
        for audience in audiences:
            try:
                recommendations = self.manager.voice_selector.get_recommended_providers(audience)
                print(f"   ✅ {audience}: {', '.join(recommendations)}")
                self.record_test_pass()
                
            except Exception as e:
                print(f"   ❌ {audience}: {e}")
                self.record_test_fail(f"Voice selection for {audience}: {e}")
    
    def test_cost_estimation(self):
        """Test cost estimation across providers."""
        print("\n💰 Test 4: Cost Estimation")
        
        if not hasattr(self, 'manager'):
            self.record_test_fail("Manager not available for cost testing")
            return
        
        sample_text = "This is a test story about mindfulness and daily reflection. " * 10
        
        try:
            comparison = self.manager.compare_providers(sample_text)
            
            for provider, stats in comparison.items():
                if "error" not in stats:
                    cost = stats.get('estimated_cost', 0)
                    voices = stats.get('available_voices', 0)
                    print(f"   ✅ {provider}: ${cost:.4f} for sample, {voices} voices")
                    self.record_test_pass()
                else:
                    print(f"   ❌ {provider}: {stats['error']}")
                    self.record_test_fail(f"{provider} cost estimation failed")
                    
        except Exception as e:
            print(f"   ❌ Cost estimation failed: {e}")
            self.record_test_fail(f"Cost estimation error: {e}")
    
    def test_sample_audio_generation(self):
        """Test audio generation with sample story."""
        print("\n🎵 Test 5: Sample Audio Generation")
        
        if not hasattr(self, 'manager'):
            self.record_test_fail("Manager not available for audio testing")
            return
        
        sample_story = {
            "id": "test_sample_001",
            "title": "A Moment of Mindfulness",
            "content": """Maya paused at her kitchen window, watching the morning light filter through the leaves. 
            For just this moment, she let go of her endless to-do list. 
            She breathed deeply and felt grateful for this simple, peaceful start to her day."""
        }
        
        audiences = ["universal", "muslim_community"]
        
        for audience in audiences:
            try:
                print(f"   🎯 Testing {audience} audience...")
                
                # Generate audio (in demo mode this will simulate)
                audio_file = self.manager.generate_audio(sample_story, audience=audience)
                
                if audio_file:
                    print(f"      ✅ Generated: {audio_file.duration_seconds:.1f}s, ${audio_file.generation_cost:.4f}")
                    print(f"      📋 Provider: {audio_file.provider}, Voice: {audio_file.voice_used}")
                    self.record_test_pass()
                else:
                    print(f"      ❌ Audio generation failed")
                    self.record_test_fail(f"Audio generation failed for {audience}")
                    
            except Exception as e:
                print(f"      ❌ Error: {e}")
                self.record_test_fail(f"Audio generation error for {audience}: {e}")
    
    def test_story_processing(self):
        """Test processing existing stories from JSONL."""
        print("\n📚 Test 6: Story Processing from JSONL")
        
        stories_file = "data/videos/videos.jsonl"
        
        if not os.path.exists(stories_file):
            print(f"   ⏭️ Skipping: {stories_file} not found")
            return
        
        try:
            stories = load_jsonl(stories_file)
            
            if not stories:
                print(f"   ⏭️ No stories found in {stories_file}")
                return
            
            # Test with first story
            test_story = stories[0]
            story_id = test_story.get('id', 'unknown')
            
            print(f"   📖 Testing with story: {story_id}")
            
            if not hasattr(self, 'manager'):
                self.record_test_fail("Manager not available for story processing")
                return
            
            # Check story content
            content = test_story.get('content', '')
            if content:
                print(f"   ✅ Story has content: {len(content)} characters")
                
                # Test audio generation
                audio_file = self.manager.generate_audio(test_story, audience="universal")
                
                if audio_file:
                    print(f"   ✅ Audio generated: {audio_file.duration_seconds:.1f}s")
                    self.record_test_pass()
                else:
                    print(f"   ❌ Audio generation failed")
                    self.record_test_fail("Real story audio generation failed")
            else:
                print(f"   ❌ Story has no content")
                self.record_test_fail("Story missing content")
                
        except Exception as e:
            print(f"   ❌ Story processing failed: {e}")
            self.record_test_fail(f"Story processing error: {e}")
    
    def test_provider_comparison(self):
        """Test provider comparison functionality."""
        print("\n📊 Test 7: Provider Comparison")
        
        if not hasattr(self, 'manager'):
            self.record_test_fail("Manager not available for comparison testing")
            return
        
        sample_text = "A short story for comparison testing. " * 5
        
        try:
            comparison = self.manager.compare_providers(sample_text)
            
            print(f"   📋 Comparing {len(comparison)} providers:")
            
            for provider, stats in comparison.items():
                if "error" not in stats:
                    cost_per_min = stats.get('cost_per_minute', 0)
                    premium_voices = stats.get('premium_voices', 0)
                    print(f"      {provider}: ${cost_per_min:.4f}/min, {premium_voices} premium voices")
                else:
                    print(f"      {provider}: {stats['error']}")
            
            self.record_test_pass()
            
        except Exception as e:
            print(f"   ❌ Provider comparison failed: {e}")
            self.record_test_fail(f"Provider comparison error: {e}")
    
    def record_test_pass(self):
        """Record a passing test."""
        self.test_results["tests_run"] += 1
        self.test_results["tests_passed"] += 1
    
    def record_test_fail(self, error_msg: str):
        """Record a failing test."""
        self.test_results["tests_run"] += 1
        self.test_results["tests_failed"] += 1
        self.test_results["errors"].append(error_msg)
    
    def print_test_results(self):
        """Print comprehensive test results."""
        print("\n" + "=" * 50)
        print("🧪 TTS System Test Results")
        print("=" * 50)
        
        results = self.test_results
        
        print(f"📊 Tests Run: {results['tests_run']}")
        print(f"✅ Passed: {results['tests_passed']}")
        print(f"❌ Failed: {results['tests_failed']}")
        
        if results['tests_run'] > 0:
            success_rate = (results['tests_passed'] / results['tests_run']) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if results['errors']:
            print(f"\n⚠️ Errors Encountered:")
            for i, error in enumerate(results['errors'], 1):
                print(f"   {i}. {error}")
        
        # System recommendations
        print(f"\n💡 System Status:")
        if results['tests_failed'] == 0:
            print("   🟢 TTS system is fully operational!")
            print("   ✨ Ready for production audio generation")
        elif results['tests_failed'] < results['tests_passed']:
            print("   🟡 TTS system is partially operational")
            print("   🔧 Some features may need configuration")
        else:
            print("   🔴 TTS system needs attention")
            print("   🛠️ Check API keys and provider configurations")
        
        # Save results to file
        results_file = self.test_dir / f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n💾 Test results saved to: {results_file}")

def main():
    """Run the TTS system test suite."""
    
    tester = TTSSystemTester()
    tester.run_all_tests()
    
    print(f"\n🏁 Testing complete!")

if __name__ == "__main__":
    main()