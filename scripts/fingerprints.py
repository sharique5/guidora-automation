#!/usr/bin/env python3
"""
Fingerprinting utilities for content uniqueness detection.
Part of Guidora Learning Extraction System.
"""

import hashlib
import re
from typing import List, Set
from difflib import SequenceMatcher

class ContentFingerprinter:
    """Handles content fingerprinting for uniqueness detection."""
    
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are', 
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must'
        }
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for fingerprinting."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove punctuation but keep word boundaries
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove stop words
        words = text.split()
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        return ' '.join(words)
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract key concepts from text."""
        normalized = self.normalize_text(text)
        words = normalized.split()
        
        # Simple keyword extraction (can be enhanced with TF-IDF later)
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and length (prefer longer, more frequent words)
        keywords = sorted(word_freq.keys(), 
                         key=lambda w: (word_freq[w], len(w)), 
                         reverse=True)
        
        return keywords[:max_keywords]
    
    def generate_content_fingerprint(self, text: str, themes: List[str] = None) -> str:
        """Generate a content-based fingerprint."""
        # Normalize main text
        normalized_text = self.normalize_text(text)
        
        # Extract key concepts
        keywords = self.extract_keywords(text, max_keywords=8)
        keywords_text = ' '.join(sorted(keywords))
        
        # Include themes if provided
        themes_text = ''
        if themes:
            themes_normalized = [self.normalize_text(theme) for theme in themes]
            themes_text = ' '.join(sorted(themes_normalized))
        
        # Combine for fingerprint
        combined_content = f"{keywords_text}|{themes_text}"
        
        # Generate hash
        return hashlib.sha256(combined_content.encode('utf-8')).hexdigest()[:16]
    
    def generate_semantic_fingerprint(self, text: str) -> str:
        """Generate a semantic-based fingerprint (simplified version)."""
        # Extract action words and concepts
        action_words = self.extract_action_concepts(text)
        concept_words = self.extract_core_concepts(text)
        
        # Combine semantic elements
        semantic_content = ' '.join(sorted(action_words + concept_words))
        
        return hashlib.sha256(semantic_content.encode('utf-8')).hexdigest()[:16]
    
    def extract_action_concepts(self, text: str) -> List[str]:
        """Extract action-related concepts."""
        action_patterns = [
            r'\b(practice|remember|focus|prioritize|maintain|develop|cultivate|embrace|avoid)\b',
            r'\b(prayer|gratitude|patience|kindness|charity|forgiveness|humility|compassion)\b',
            r'\b(daily|regularly|consistently|throughout|during|before|after)\b'
        ]
        
        actions = []
        text_lower = text.lower()
        
        for pattern in action_patterns:
            matches = re.findall(pattern, text_lower)
            actions.extend(matches)
        
        return list(set(actions))
    
    def extract_core_concepts(self, text: str) -> List[str]:
        """Extract core conceptual themes."""
        concept_patterns = [
            r'\b(spiritual|physical|mental|emotional|social|community)\b',
            r'\b(guidance|wisdom|knowledge|understanding|awareness|mindfulness)\b',
            r'\b(balance|harmony|peace|strength|resilience|growth)\b'
        ]
        
        concepts = []
        text_lower = text.lower()
        
        for pattern in concept_patterns:
            matches = re.findall(pattern, text_lower)
            concepts.extend(matches)
        
        return list(set(concepts))
    
    def similarity_score(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        norm1 = self.normalize_text(text1)
        norm2 = self.normalize_text(text2)
        
        return SequenceMatcher(None, norm1, norm2).ratio()
    
    def is_similar_content(self, text1: str, text2: str, threshold: float = 0.7) -> bool:
        """Check if two texts are semantically similar."""
        return self.similarity_score(text1, text2) >= threshold


# Convenience functions for easy usage
def generate_fingerprint(text: str, themes: List[str] = None) -> str:
    """Generate a fingerprint for given text and themes."""
    fingerprinter = ContentFingerprinter()
    return fingerprinter.generate_content_fingerprint(text, themes)

def check_uniqueness(text: str, existing_fingerprints: Set[str], themes: List[str] = None) -> bool:
    """Check if content is unique against existing fingerprints."""
    fingerprint = generate_fingerprint(text, themes)
    return fingerprint not in existing_fingerprints
