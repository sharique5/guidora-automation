# Video File Naming Solution

## 🎯 **Your Questions Answered:**

### **Q: There isn't any story_id in generated scripts JSON file?**
**A: ✅ SOLVED** - Created automatic story ID generation system:
- Scans existing files and assigns sequential IDs: `story_001`, `story_002`, etc.
- Maps long filenames like `seeing_signs_a_journey_to_inner_strength` → `story_001`
- Consistent across all languages

### **Q: Is timestamp mandatory?**
**A: ❌ NO** - Timestamp is optional and not recommended for primary workflow:
- **Default**: `story_001_en.mp4` (clean, simple)
- **With timestamp**: `story_001_en_20251103.mp4` (only if needed for versioning)

## 🎬 **New Recommended Naming Convention:**

```
story_XXX_<lang>.mp4
```

### **Examples:**
- `story_001_en.mp4` - English version
- `story_001_es.mp4` - Spanish version  
- `story_001_fr.mp4` - French version
- `story_001_ur.mp4` - Urdu version
- `story_001_ar.mp4` - Arabic version

## 📂 **File Placement:**
Save videos to: `data/videos/production/{language}/{filename}`

### **Complete Paths:**
```
data/videos/production/en/story_001_en.mp4
data/videos/production/es/story_001_es.mp4
data/videos/production/fr/story_001_fr.mp4
data/videos/production/ur/story_001_ur.mp4
data/videos/production/ar/story_001_ar.mp4
```

## 🔧 **How to Use:**

### **1. Check Current Naming:**
```bash
python scripts/final_video_manager.py naming reference
```

### **2. Get All Video Filenames for Current Batch:**
```bash
python scripts/final_video_manager.py naming batch
```

### **3. Generate Specific Filename:**
```bash
python scripts/final_video_manager.py naming filename data/stories/en/seeing_signs_a_journey_to_inner_strength_en.json --language en
```

### **4. Enhanced Production Batch (with naming):**
```bash
python scripts/final_video_manager.py batch
```

## 🎯 **Benefits of This System:**

✅ **Simple & Clean**: No complex timestamps cluttering filenames  
✅ **Predictable**: Sequential numbering is easy to follow  
✅ **Scalable**: Works for 10 videos or 1000 videos  
✅ **Language Clear**: Instantly see which language each video is  
✅ **Sortable**: Files naturally sort in correct order  
✅ **Professional**: Clean naming for YouTube and storage  

## 💡 **Complete Workflow:**

1. **Get your batch with clean filenames:**
   ```bash
   python scripts/final_video_manager.py batch
   ```

2. **Create videos in Instadoodle using provided scripts**

3. **Generate outro for each video:**
   ```bash
   python scripts/final_video_manager.py outro generate story_001_en --language en
   ```

4. **Export from Instadoodle with exact filename shown:**
   - Save as: `story_001_en.mp4`
   - Location: `data/videos/production/en/`

5. **Update tracking:**
   ```bash
   python scripts/final_video_manager.py update-status story_001_en video_ready --video-path "data/videos/production/en/story_001_en.mp4"
   ```

## 🌟 **Key Insight:**
The system automatically handles the complexity behind the scenes while giving you super simple, clean filenames that are perfect for production workflow!

**No more confusion about story IDs or timestamps - everything is automated! 🚀**