import json

from typing import List, Dict

def load_jsonl(file_path: str) -> List[Dict]:
    """Load all records from a JSONL file into a list."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        return []

def save_jsonl(data: List[Dict], file_path: str):
    """Save data to a JSONL file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')