# YouTube Shorts Generation - Complete Guide

## ✅ Setup Complete

### Files Created:
1. **`prompts/short_script_youtube.txt`** - Shorts generation prompt
   - 30-60 second optimization
   - Vertical format (9:16) 
   - Text overlay friendly
   - Hook/Wisdom/Crisis variants

2. **`generate_shorts.py`** - Shorts generator script
   - Generates 2 shorts per story by default (Hook + Wisdom)
   - Optional Crisis short
   - Saved to `data/stories/shorts/`

3. **`track_shorts_simple.py`** - Add shorts to video tracker
   - Interactive tracking
   - Links shorts to parent videos

---

## 📝 Usage Workflow

### 1. Generate Shorts from a Story

```powershell
# Generate both Hook and Wisdom shorts (default)
python generate_shorts.py youtube_optimized_learning_4_1_91b588ac_7ac9e43b

# Generate specific type only
python generate_shorts.py <story_id> --type hook
python generate_shorts.py <story_id> --type wisdom
python generate_shorts.py <story_id> --type crisis
```

**Output**: Saves to `data/stories/shorts/`
- `*_short_hook_*.json` - Teaser that drives to full video
- `*_short_wisdom_*.json` - Standalone value/lesson

**Cost**: ~$0.07-0.08 per short (~$0.15 for both)

### 2. Track Shorts in Video Tracker

```powershell
python track_shorts_simple.py
# Then: type "all" → Enter story number (e.g., "006")
```

Adds shorts to `data/video_tracker.json`:
- `006_short_hook` 
- `006_short_wisdom`

Status: `script_ready` → ready for video creation

---

## 🎬 Short Types Explained

### 1. **Hook/Teaser Short** 
**Purpose**: Drive traffic to long-form video

**Structure**:
- 0-3s: Shocking moment/question
- 3-20s: Build crisis (don't resolve!)
- 20-25s: Hint at what's coming
- 25-30s: CLIFFHANGER + "Watch full video"

**Example**: 
- "She almost killed her patient..."
- "3 AM. Alone. Crying..."
- Ends: "You won't believe what happened next"

### 2. **Wisdom/Insight Short**
**Purpose**: Standalone value → build followers

**Structure**:
- 0-3s: Bold statement of insight
- 3-15s: Quick story context
- 15-40s: Transformation/application  
- 40-45s: Powerful close + "More in my videos"

**Example**:
- "This ONE phrase changed everything..."
- Delivers actual lesson
- Makes viewers want to save/share

### 3. **Crisis/Dramatic Short** (Optional)
**Purpose**: Viral potential through emotion

**Structure**:
- 0-3s: Drop into crisis
- 3-25s: Build emotional intensity
- 25-40s: Turning point
- 40-45s: Resolution + CTA

**Example**:
- Pure emotion, not explanation
- Music is key
- "Full story will make you cry"

---

## 📊 Current Status

### Emma's Story (006):
✅ **Hook Short**: "On the Brink: A Teacher's Crisis"
- Teases Emma's near-quit moment
- Ends with cliffhanger
- Drives to full video

✅ **Wisdom Short**: "Close to Quitting: A Teacher's Revelation"  
- Delivers the taqwa/consciousness insight
- Standalone value
- Builds authority

**Cost**: $0.15 total
**Status**: Tracked in video_tracker.json as `script_ready`

---

## 🎥 Next Steps for Production

### For Each Short:

1. **Create Vertical Video (9:16)**
   - Use whiteboard animation or stock footage
   - 30-60 seconds duration
   - Fast-paced cuts

2. **Add Text Overlays**
   - Short punchy sentences (under 10 words)
   - High contrast (white text on dark background)
   - Sync to script timestamps
   - Large readable font

3. **Add Music**
   - Hook short: Tense → Curious
   - Wisdom short: Uplifting → Motivational
   - 30-60s loop

4. **Upload as YouTube Short**
   - Vertical format required
   - Title from short script
   - Description: Hook + link to full video
   - Add #Shorts tag

5. **Link to Full Video**
   - In description: "Full story: [link to 006_en]"
   - Pin comment with link
   - End screen (if possible in Shorts)

---

## 💡 Best Practices

### Text Overlays (CRITICAL):
- Most viewers watch MUTED
- Each sentence = one text card (3-5 seconds)
- Place text in TOP 2/3 of screen (YouTube UI at bottom)
- Use emojis sparingly
- Emphasize key words in CAPS

### Hooks (First 3 Seconds):
❌ "This is Emma, a teacher who..."
✅ "Ever feel like giving EVERYTHING up?"

❌ "Let me tell you about..."
✅ "She was about to quit FOREVER."

### Retention:
- Plant "wait for it" moments early
- Use phrases: "But then...", "Here's what happened..."
- Question → Answer → Payoff structure

### CTA (Last 5 Seconds):
- "Watch full story in my videos"
- "Part 2 in bio"  
- "Link to full video below"
- Clear next action

---

## 🔄 Workflow for New Stories

For each new story:

```powershell
# 1. Generate story
python generate_youtube_optimized_story.py

# 2. Translate
python translate_story.py <story_id>

# 3. Track main video
python add_to_tracker.py <number>

# 4. Generate shorts
python generate_shorts.py <story_id>

# 5. Track shorts
python track_shorts_simple.py
```

---

## 📈 Expected Results

**Shorts Strategy**:
- 2 shorts per story = 6 shorts from 3 stories (Sarah/Tom/Emma)
- Hook shorts → drive views to long-form
- Wisdom shorts → build followers
- Cross-promotion between formats

**Algorithm Benefits**:
- Shorts get separate discovery feed
- Higher reach than long-form alone
- Can go viral independently
- Drive subscribers to channel

**Metrics to Track**:
- Short views vs long-form views
- Click-through rate from short to full video
- New subscribers from shorts
- Which short type performs better (Hook vs Wisdom)

---

## 🎯 Summary

✅ **Shorts generation setup complete**
✅ **2 shorts generated for Emma's story**  
✅ **Tracked in video tracker**
⏳ **Ready for video production**

Next: Create vertical videos with text overlays → Upload → Monitor performance
