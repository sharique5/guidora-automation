#!/usr/bin/env python3
"""
Centralized utilities for story management.
Handles file operations, character tracking, and common patterns.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

# Import centralized config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.paths import STORIES_DIR, STORY_DIRS, LANGUAGES, ACTIVE_LANGUAGES


def find_story(story_id: str) -> Tuple[Optional[Path], Optional[Dict]]:
    """
    Find a story file by ID across all language directories.
    
    Args:
        story_id: Story identifier (can be hash, number, or filename)
    
    Returns:
        Tuple of (file_path, story_data) or (None, None) if not found
    """
    # Search in all story directories
    for json_file in STORIES_DIR.rglob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Check various ID fields
                if (data.get('id') == story_id or 
                    story_id in str(json_file.name) or
                    data.get('video_id', '').startswith(story_id)):
                    return json_file, data
        except (json.JSONDecodeError, IOError):
            continue
    
    return None, None


def find_story_files(story_number: str) -> Dict[str, Path]:
    """
    Find all language versions of a story by number.
    
    Args:
        story_number: Story number (e.g., "004", "005")
    
    Returns:
        Dictionary mapping language codes to file paths
    """
    files = {}
    
    # Search in each language directory
    for lang_key, lang_dir in STORY_DIRS.items():
        if not lang_dir.exists():
            continue
        
        # Get most recent JSON files
        json_files = sorted(
            lang_dir.glob("*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if json_files:
            files[lang_key] = json_files[0]
    
    return files


def load_story(file_path: Path) -> Optional[Dict]:
    """
    Load a story from a JSON file with error handling.
    
    Args:
        file_path: Path to the JSON file
    
    Returns:
        Story data dictionary or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None


def save_story(file_path: Path, story_data: Dict) -> bool:
    """
    Save a story to a JSON file with error handling.
    
    Args:
        file_path: Path to save the JSON file
        story_data: Story data dictionary
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"❌ Error saving {file_path}: {e}")
        return False


def extract_title(file_path: Path) -> str:
    """
    Extract title from a story file.
    
    Args:
        file_path: Path to the story JSON file
    
    Returns:
        Extracted title or "Untitled"
    """
    story_data = load_story(file_path)
    if not story_data:
        return "Untitled"
    
    # Try multiple title fields
    title = story_data.get('title')
    if title:
        return title
    
    # Try extracting from content
    content = story_data.get('story_content') or story_data.get('content', '')
    
    # Look for markdown title
    title_match = re.search(r'\*\*Title\*\*:\s*["\']?([^"\'\n]+)["\']?', content)
    if title_match:
        return title_match.group(1).strip()
    
    # Look for first heading
    heading_match = re.search(r'^#+ (.+)$', content, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()
    
    return "Untitled"


def extract_character_info(content: str) -> Optional[Dict[str, str]]:
    """
    Extract character name and occupation from story content.
    
    Args:
        content: Story content text
    
    Returns:
        Dictionary with 'name' and 'occupation' or None
    """
    # Common patterns for character introductions
    patterns = [
        r"(?:Meet |This is )?([A-Z][a-z]+)[,\s]+(?:a|an)\s+([^.,\n]+?)(?:\.|,|\s+who)",
        r"([A-Z][a-z]+)\s+(?:was|is)\s+(?:a|an)\s+([^.,\n]+?)(?:\.|,)",
        r"([A-Z][a-z]+)\s*\(([^)]+)\)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return {
                'name': match.group(1).strip(),
                'occupation': match.group(2).strip()
            }
    
    return None


def extract_used_characters() -> List[str]:
    """
    Extract all characters used in recent stories.
    Smart detection that works for any character.
    
    Returns:
        List of character descriptions (e.g., "Sarah (night-shift nurse)")
    """
    used_chars = []
    youtube_dir = STORY_DIRS.get('youtube_optimized')
    
    if not youtube_dir or not youtube_dir.exists():
        return []
    
    # Get all story files
    for file in sorted(youtube_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        story_data = load_story(file)
        if not story_data:
            continue
        
        content = story_data.get('story_content', '')
        char_info = extract_character_info(content)
        
        if char_info:
            char_desc = f"{char_info['name']} ({char_info['occupation']})"
            if char_desc not in used_chars:
                used_chars.append(char_desc)
    
    return used_chars


def get_character_exclusion_text(used_chars: List[str]) -> str:
    """
    Generate exclusion text for prompt to avoid character repetition.
    
    Args:
        used_chars: List of used character descriptions
    
    Returns:
        Formatted exclusion text for prompt
    """
    if not used_chars:
        return ""
    
    exclusion = "\n\nCRITICAL: DO NOT use these characters (already used in recent videos):\n"
    exclusion += "\n".join([f"- {char}" for char in used_chars])
    exclusion += "\n\nYou MUST choose a completely different character type from the diverse options list."
    
    return exclusion


def get_story_count(directory: Optional[Path] = None) -> int:
    """
    Count number of story files in a directory.
    
    Args:
        directory: Directory to count stories in (default: youtube_optimized)
    
    Returns:
        Number of JSON files found
    """
    if directory is None:
        directory = STORY_DIRS.get('youtube_optimized')
    
    if not directory or not directory.exists():
        return 0
    
    return len(list(directory.glob("*.json")))


def generate_story_filename(title: str, lang_code: str, max_length: int = 60) -> str:
    """
    Generate a safe filename from a story title.
    
    Args:
        title: Story title
        lang_code: Language code
        max_length: Maximum filename length
    
    Returns:
        Safe filename with extension
    """
    # Remove quotes and special characters
    safe_title = re.sub(r'["\':?!]', '', title)
    safe_title = re.sub(r'[^\w\s-]', '_', safe_title)
    safe_title = re.sub(r'\s+', '_', safe_title).lower()
    
    # Truncate if too long
    if len(safe_title) > max_length:
        safe_title = safe_title[:max_length]
    
    return f"{safe_title}_{lang_code}.json"


def validate_story_data(story_data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate story data structure.
    
    Args:
        story_data: Story data dictionary
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required fields
    required_fields = ['id', 'story_content']
    for field in required_fields:
        if field not in story_data:
            errors.append(f"Missing required field: {field}")
    
    # Check content not empty
    content = story_data.get('story_content', '')
    if not content or len(content.strip()) < 100:
        errors.append("Story content is empty or too short")
    
    return len(errors) == 0, errors


def format_story_preview(story_data: Dict, max_length: int = 500) -> str:
    """
    Format a story preview for display.
    
    Args:
        story_data: Story data dictionary
        max_length: Maximum preview length
    
    Returns:
        Formatted preview string
    """
    content = story_data.get('story_content', 'No content')
    preview = content[:max_length]
    
    if len(content) > max_length:
        preview += "..."
    
    return preview


# Export commonly used functions
__all__ = [
    'find_story',
    'find_story_files',
    'load_story',
    'save_story',
    'extract_title',
    'extract_character_info',
    'extract_used_characters',
    'get_character_exclusion_text',
    'get_story_count',
    'generate_story_filename',
    'validate_story_data',
    'format_story_preview'
]


if __name__ == "__main__":
    # Test utilities
    print("🧪 Testing Story Utilities\n")
    
    print("📚 Used Characters:")
    chars = extract_used_characters()
    for char in chars:
        print(f"  - {char}")
    
    print(f"\n📊 Story Count: {get_story_count()}")
    
    print(f"\n✅ Utilities loaded successfully")
