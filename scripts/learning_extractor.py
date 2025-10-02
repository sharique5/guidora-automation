#!/usr/bin/env python3
"""
MVP Learning Extraction & Fingerprinting System
Week 1: Extract lessons from verses and create uniqueness fingerprints
"""

import json
import hashlib
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import os

@dataclass
class Learning:
    """Represents an extracted learning from a Quranic verse."""
    id: str
    chapter_id: int
    verse_number: int
    chapter_name: str
    source_verse: str
    practical_application: str
    main_themes: List[str]
    audience_groups: List[str]
    fingerprint: str
    extracted_at: str
    lesson_type: str = "practical_wisdom"

class LearningExtractor:
    """Extracts and processes learnings from Quranic verses."""
    
    def __init__(self, data_file: str, output_file: str = "data/learnings/learnings.jsonl"):
        self.data_file = data_file
        self.output_file = output_file
        self.processed_fingerprints: Set[str] = set()
        self._load_existing_learnings()
    
    def _load_existing_learnings(self):
        """Load existing learnings to avoid duplicates."""
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        learning = json.loads(line)
                        self.processed_fingerprints.add(learning['fingerprint'])
            print(f"📚 Loaded {len(self.processed_fingerprints)} existing learnings")
    
    def generate_fingerprint(self, practical_application: str, themes: List[str]) -> str:
        """Generate a unique fingerprint for a learning."""
        # Normalize text for fingerprinting
        normalized_text = practical_application.lower().strip()
        themes_text = " ".join(sorted([theme.lower().strip() for theme in themes]))
        
        # Combine for uniqueness
        content = f"{normalized_text}|{themes_text}"
        
        # Create hash
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    
    def extract_learning(self, verse: Dict) -> Optional[Learning]:
        """Extract a learning from a verse if it's unique."""
        practical_app = verse.get('practical_application', '').strip()
        
        # Skip if no practical application
        if not practical_app or len(practical_app) < 20:
            return None
        
        # Generate fingerprint
        themes = verse.get('main_themes', [])
        fingerprint = self.generate_fingerprint(practical_app, themes)
        
        # Check uniqueness
        if fingerprint in self.processed_fingerprints:
            return None
        
        # Create learning
        learning_id = f"learning_{verse['chapter_id']}_{verse['verse_number']}_{fingerprint[:8]}"
        
        learning = Learning(
            id=learning_id,
            chapter_id=verse['chapter_id'],
            verse_number=verse['verse_number'],
            chapter_name=verse['chapter_name'],
            source_verse=verse['english_translation'][:100] + "...",
            practical_application=practical_app,
            main_themes=themes,
            audience_groups=verse.get('audience_groups', []),
            fingerprint=fingerprint,
            extracted_at=datetime.now().isoformat()
        )
        
        # Mark as processed
        self.processed_fingerprints.add(fingerprint)
        
        return learning
    
    def process_verses(self, limit: Optional[int] = None) -> List[Learning]:
        """Process verses and extract unique learnings."""
        learnings = []
        processed_count = 0
        
        print(f"🔄 Processing verses from {self.data_file}")
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                
                try:
                    verse = json.loads(line)
                    learning = self.extract_learning(verse)
                    
                    if learning:
                        learnings.append(learning)
                        print(f"✅ Extracted: {learning.id}")
                    
                    processed_count += 1
                    
                    # Progress indicator
                    if processed_count % 100 == 0:
                        print(f"📊 Processed {processed_count} verses, extracted {len(learnings)} learnings")
                    
                    # Respect limit for MVP testing
                    if limit and processed_count >= limit:
                        break
                        
                except json.JSONDecodeError:
                    print(f"⚠️ Skipping invalid JSON at line {line_num}")
                    continue
        
        print(f"🎉 Final: Processed {processed_count} verses, extracted {len(learnings)} unique learnings")
        return learnings
    
    def save_learnings(self, learnings: List[Learning]):
        """Save learnings to JSONL file."""
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        with open(self.output_file, 'a', encoding='utf-8') as f:
            for learning in learnings:
                f.write(json.dumps(asdict(learning), ensure_ascii=False) + '\n')
        
        print(f"💾 Saved {len(learnings)} learnings to {self.output_file}")
    
    def get_stats(self) -> Dict:
        """Get statistics about processed learnings."""
        theme_counts = {}
        audience_counts = {}
        total_learnings = len(self.processed_fingerprints)
        
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        learning = json.loads(line)
                        
                        # Count themes
                        for theme in learning.get('main_themes', []):
                            theme_counts[theme] = theme_counts.get(theme, 0) + 1
                        
                        # Count audiences
                        for audience in learning.get('audience_groups', []):
                            audience_counts[audience] = audience_counts.get(audience, 0) + 1
        
        return {
            'total_learnings': total_learnings,
            'top_themes': sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            'audience_distribution': sorted(audience_counts.items(), key=lambda x: x[1], reverse=True)
        }


def main():
    """Main function for MVP testing."""
    print("🚀 Guidora Learning Extraction MVP - Week 1")
    print("=" * 50)
    
    # Initialize extractor
    extractor = LearningExtractor(
        data_file="data/tafsir/quran_filtered.jsonl",
        output_file="data/learnings/learnings.jsonl"
    )
    
    # Process first 100 verses for MVP testing
    learnings = extractor.process_verses(limit=100)
    
    # Save results
    if learnings:
        extractor.save_learnings(learnings)
    
    # Show statistics
    stats = extractor.get_stats()
    print(f"\n📊 Statistics:")
    print(f"   Total unique learnings: {stats['total_learnings']}")
    print(f"   Top themes: {[f'{theme}({count})' for theme, count in stats['top_themes'][:5]]}")
    print(f"   Audience groups: {len(stats['audience_distribution'])}")
    
    print(f"\n🎯 Next Steps:")
    print(f"   - Review extracted learnings in data/learnings/learnings.jsonl")
    print(f"   - Adjust fingerprinting logic if needed")
    print(f"   - Ready for Week 2: LLM Story Generation!")


if __name__ == "__main__":
    main()