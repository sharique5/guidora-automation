import json
from typing import List, Dict, Generator, Optional

def load_all_jsonl(file_path: str) -> List[Dict]:
    """
    Load all records from a JSONL file into a list.
    ⚠️ Use only if file size is reasonable (fits in memory).
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_chapter_jsonl(file_path: str, chapter_id: int) -> List[Dict]:
    """
    Load all verses from a specific chapter (surah).
    Returns a list of dicts for that chapter.
    """
    verses = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("chapter_id") == chapter_id:
                verses.append(record)
    return verses


def load_chapter_verse_jsonl(file_path: str, chapter_id: int, verse_number: int) -> Optional[Dict]:
    """
    Load a single verse record from a chapter.
    Returns the dict if found, else None.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("chapter_id") == chapter_id and record.get("verse_number") == verse_number:
                return record
    return None
