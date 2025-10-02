import csv
import json

INPUT_FILE = "../data/tafsir/quran_dataset.csv"
OUTPUT_FILE = "../data/tafsir/quran_filtered.jsonl"

FIELDS = [
    "chapter_id",
    "chapter_name",
    "verse_number",
    "english_translation",
    "tafsir",
    "main_themes",
    "practical_application",
    "audience_group"
]

def csv_to_jsonl(input_file, output_file, fields):
    """Convert CSV to JSONL merging duplicate verses and combining their audience groups."""
    from collections import defaultdict
    
    # First pass: group all rows by verse
    verse_groups = defaultdict(list)
    
    with open(input_file, "r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            verse_key = (int(row["chapter_id"]), int(row["verse_number"]))
            verse_groups[verse_key].append(row)
    
    # Second pass: merge and write
    written_count = 0
    merged_count = 0
    
    with open(output_file, "w", encoding="utf-8") as f_out:
        for verse_key, rows in verse_groups.items():
            if len(rows) > 1:
                merged_count += 1
            
            # Use first row as base
            base_row = rows[0]
            
            # Collect all unique audience groups
            audience_groups = []
            for row in rows:
                if row["audience_group"] and row["audience_group"] not in audience_groups:
                    audience_groups.append(row["audience_group"])
            
            # Create merged record
            record = {
                "chapter_id": int(base_row["chapter_id"]),
                "chapter_name": base_row["chapter_name"],
                "verse_number": int(base_row["verse_number"]),
                "english_translation": base_row["english_translation"],
                "tafsir": base_row["tafsir"],
                "main_themes": [t.strip() for t in base_row["main_themes"].split(",")] if base_row["main_themes"] else [],
                "practical_application": base_row["practical_application"],
                "audience_groups": audience_groups
            }
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
            written_count += 1

    print(f"✅ Written {written_count} unique verses to {output_file}")
    print(f"🔀 Merged {merged_count} verses that had multiple audience groups")
    print(f"ℹ️ Audience groups are now stored as 'audience_groups' (plural) array")

if __name__ == "__main__":
    csv_to_jsonl(INPUT_FILE, OUTPUT_FILE, FIELDS)