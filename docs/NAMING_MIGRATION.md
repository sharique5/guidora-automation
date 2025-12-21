# ✅ File Naming Migration Complete

## What Changed

Migrated from **hash-based naming** to **structured naming convention** for all stories, translations, and shorts.

### Before:
```
youtube_optimized_learning_1_1_b9b9bc1f_2d15ef3d.json
the_mistake_that_destroys_your_peace_sarah_es.json
youtube_optimized_learning_1_1_b9b9bc1f_2d15ef3d_short_hook_d6040470.json
```

### After:
```
004_sarah_nurse_story_en.json
004_sarah_nurse_story_es.json
004_sarah_short_hook.json
```

---

## New Naming Convention

### Format:
```
{number}_{character}_{occupation}_{type}_{lang}.json
```

### Components:
- **number**: 004, 005, 006 (3-digit story number)
- **character**: sarah, tom, emma (lowercase)
- **occupation**: nurse, father, teacher (lowercase)
- **type**: story (for main content)
- **lang**: en, es, fr, hi (2-letter code)

### Shorts Format:
```
{number}_{character}_short_{type}.json
```
- **type**: hook, wisdom, crisis

---

## Migration Results

### Files Renamed: 15 total

**Main Stories (3)**:
- ✅ 004_sarah_nurse_story_en.json
- ✅ 005_tom_father_story_en.json
- ✅ 006_emma_teacher_story_en.json

**Translations (6)**:
- ✅ 005_tom_father_story_es.json
- ✅ 005_tom_father_story_fr.json
- ✅ 005_tom_father_story_hi.json
- ✅ 006_emma_teacher_story_es.json
- ✅ 006_emma_teacher_story_fr.json
- ✅ 006_emma_teacher_story_hi.json

**Shorts (6)**:
- ✅ 004_sarah_short_hook.json
- ✅ 004_sarah_short_wisdom.json
- ✅ 005_tom_short_hook.json
- ✅ 005_tom_short_wisdom.json
- ✅ 006_emma_short_hook.json
- ✅ 006_emma_short_wisdom.json

### Video Tracker Updated:
- ✅ 11 entries updated with new file paths
- ✅ All story_file and short_file references corrected

### Internal IDs Updated:
- ✅ All JSON files now have consistent internal IDs matching filenames
- ✅ parent_story_id references updated in shorts

---

## Benefits

✅ **Instant Recognition**: `004_sarah_nurse_story_en.json` tells you everything
✅ **Easy Sorting**: Files naturally sort by story number
✅ **No Hash Lookups**: Don't need tracker to find related files
✅ **Clear Relationships**: All files for story 004 start with `004_sarah_`
✅ **Future-Proof**: Easy to add new stories with next number

---

## Future File Naming

### New Stories:
```
007_{character}_{occupation}_story_en.json
007_{character}_{occupation}_story_es.json
007_{character}_{occupation}_story_fr.json
007_{character}_{occupation}_story_hi.json
```

### Videos (when created):
```
004_sarah_main_en.mp4
004_sarah_main_es.mp4
004_sarah_short_hook.mp4
```

### Thumbnails:
```
assets/thumbnails/main/004_sarah_en.png
assets/thumbnails/shorts/004_sarah_hook.png
```

---

## Scripts Updated

### Generators:
- ✅ `lib/story_utils.py` - Added `generate_story_id()` and `generate_story_filename()` helpers
- ✅ `translate_story.py` - Uses new naming for translations
- ⚠️ `generate_youtube_optimized_story.py` - **Needs manual update** (requires character/occupation input)
- ⚠️ `generate_shorts.py` - **Needs manual update** (requires story metadata)

### Utilities:
- ✅ `migrate_file_names.py` - Migration script (can be deleted after confirmation)
- ✅ `update_tracker_migration.py` - Tracker update script (can be deleted)
- ✅ `track_shorts.py` - Consolidated (removed duplicate)

---

## Backup Location

All original files backed up to:
```
data/stories_backup_20251221_125317/
```

Keep this backup for at least 1 week, then delete if everything works correctly.

---

## Next Steps

1. **Test translation**: Generate new story → translate → verify new naming
2. **Test shorts**: Generate shorts for new story → verify naming
3. **Update generators**: Add character/occupation prompts to story generator
4. **Clean up**: Delete migration scripts + backup after 1 week
5. **Documentation**: Update README with new naming convention

---

## Quick Reference

### Find all files for a story:
```powershell
Get-ChildItem -Path "data\stories" -Recurse -Filter "004_sarah*"
```

### Find all shorts:
```powershell
Get-ChildItem -Path "data\stories\shorts" -Filter "*_short_*"
```

### Find specific language:
```powershell
Get-ChildItem -Path "data\stories" -Recurse -Filter "*_story_es.json"
```
