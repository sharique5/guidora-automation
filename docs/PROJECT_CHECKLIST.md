# Guidora — Project Checklist & MVP Schedule

**Status**: 🚀 **Week 2 Complete** - Story Generation MVP with OpenAI Integration ✅  
**Next**: Week 3 - Text-to-Speech Pipeline MVP  
**Approach**: Weekly MVP iterations with production automation  

---

## 📅 **6-Week MVP Schedule**

### **✅ Week 1: Learning Extraction & Fingerprinting** (COMPLETED)
- [x] **Data Processing**: Clean CSV→JSONL with audience group merging (`scripts/csv2json.py`)
- [x] **Verse Readers**: Efficient chapter/verse lookup functions (`scripts/read_surahs.py`) 
- [x] **Learning Extractor**: Core system to extract practical applications (`lib/learning_extractor.py`)
- [x] **Fingerprinting**: Content uniqueness detection with semantic hashing (`lib/fingerprints.py`)
- [x] **Weekly Cadence**: Batch processing manager for sustainable automation (`lib/weekly_cadence.py`)
- [x] **Output**: 2 unique learnings extracted from first 100 verses (`data/learnings/learnings.jsonl`)

### **✅ Week 2: LLM Story Generation MVP** (COMPLETED)
- [x] **LLM Integration**: OpenAI API wrapper with retry logic and cost controls (`lib/llm_tools.py`)
- [x] **Story Prompts**: Template system for universal, Muslim community, and spiritual seekers (`prompts/story_*.txt`)
- [x] **Story Generator**: Convert learnings to engaging, relatable modern stories (`scripts/story_generator.py`)
- [x] **Audience Targeting**: Custom prompts for different audience groups with cultural adaptation
- [x] **YouTube Optimization**: Auto-generated titles, descriptions, tags, and thumbnail concepts
- [x] **Weekly Integration**: Updated cadence system for automated story generation pipeline
- [x] **Output**: 4 professional stories (12.5 min content) with YouTube metadata ($0.29 cost)

### **📝 Week 3: Text-to-Speech Pipeline MVP**
- [ ] **TTS Providers**: Multi-provider support (ElevenLabs, Google, Azure) (`lib/providers/tts_api.py`)
- [ ] **Voice Selection**: Natural, engaging voice profiles per audience
- [ ] **SSML Processing**: Pause, emphasis, and pacing optimization
- [ ] **Audio Pipeline**: Story→Speech with quality validation
- [ ] **Audio Storage**: Organized file management with metadata
- [ ] **Output**: High-quality audio files from generated stories

### **🎬 Week 4: Video Assembly MVP**
- [ ] **Video Engine**: FFmpeg/MoviePy integration (`lib/video_tools/video_assembler.py`)
- [ ] **Visual Assets**: Background images, text overlays, transitions
- [ ] **Slideshow Builder**: Auto-sync visuals with audio timing
- [ ] **Template System**: Consistent branding and layout
- [ ] **Quality Control**: 1080p output with optimized encoding
- [ ] **Output**: Complete video files ready for upload

### **📺 Week 5: YouTube Publisher MVP**
- [ ] **YouTube API**: OAuth device flow integration (`lib/video_tools/youtube_uploader.py`)
- [ ] **Metadata Generation**: Auto-generated titles, descriptions, tags
- [ ] **Upload Pipeline**: Automated video publishing with retry logic
- [ ] **Playlist Management**: Auto-categorization by audience/theme
- [ ] **Publishing Logs**: Idempotent tracking and error handling
- [ ] **Output**: Automated YouTube uploads with proper metadata

### **⚙️ Week 6: Full Automation & GitHub Actions**
- [ ] **GitHub Workflows**: Weekly processing automation (`.github/workflows/`)
- [ ] **State Management**: Progress tracking across automation runs
- [ ] **Error Handling**: Comprehensive failure recovery and notifications
- [ ] **Monitoring**: Structured logging and performance metrics
- [ ] **Cost Tracking**: API usage and budget monitoring
- [ ] **Output**: Fully automated weekly content generation

---

## 🏗️ **Technical Foundation**

### **A. Data Infrastructure** ✅
- [x] **Quranic Dataset**: 6,236 verses with tafsir, themes, audience groups
- [x] **Data Processing**: Deduplicated JSONL with merged audience targeting
- [x] **Verse Access**: Efficient lookup by chapter/verse with caching
- [x] **Learning Storage**: Structured storage for extracted wisdom

### **B. Content Processing Pipeline**
- [x] **Learning Extraction**: Practical applications with uniqueness fingerprinting
- [x] **Story Generation**: LLM-powered modern storytelling with universal language
- [ ] **Multi-Language**: Support for EN/UR/HI with localized prompts
- [ ] **Quality Control**: Content validation and tone consistency

### **C. Media Production**
- [ ] **Text-to-Speech**: Natural voice synthesis with emotional inflection
- [ ] **Video Assembly**: Automated slideshow creation with visual assets
- [ ] **Audio Processing**: Background music, normalization, quality optimization
- [ ] **Visual Design**: Consistent branding, thumbnails, and overlays

### **D. Publishing & Distribution**
- [ ] **YouTube Integration**: Automated uploads with metadata optimization
- [ ] **Content Scheduling**: Strategic timing for maximum engagement
- [ ] **Analytics Tracking**: Performance monitoring and optimization
- [ ] **Multi-Platform**: Expandable to other platforms (Instagram, TikTok)

---

## 🎯 **Production Milestones**

### **MVP Completion (Week 6)**
**Goal**: End-to-end automation generating weekly content
- ✅ Learning extraction from Quranic wisdom
- ✅ AI-powered story generation
- 📝 High-quality TTS audio production
- 🎬 Automated video assembly
- 📺 YouTube publishing pipeline
- ⚙️ GitHub Actions automation

### **V1.0 (Week 8-10)**
**Goal**: Production-ready with quality controls
- [ ] **Reviewer Interface**: Human oversight for content approval
- [ ] **Content Policy**: Automated checks for appropriateness
- [ ] **Multi-Language**: Full EN/UR/HI support with cultural adaptation
- [ ] **Advanced Analytics**: Detailed performance tracking and optimization
- [ ] **Cost Optimization**: Efficient API usage and budget controls

### **V1.1 (Week 12-16)**
**Goal**: Growth and optimization features
- [ ] **YouTube Shorts**: Vertical format auto-generation
- [ ] **A/B Testing**: Title, thumbnail, and content optimization
- [ ] **Advanced Targeting**: Personalized content for audience segments
- [ ] **Performance Analytics**: Data-driven content improvement
- [ ] **Multi-Platform**: Expansion to Instagram, TikTok, Facebook

---

## 📊 **Current Status & Next Actions**

### **Completed (Week 1-2)**
```
✅ Data: 6,236 verses processed, 0 duplicates
✅ Extraction: 4 unique learnings extracted with fingerprinting
✅ Story Generation: 4 professional stories (12.5 min content)
✅ LLM Integration: OpenAI API with cost controls ($0.29 total)
✅ YouTube Optimization: Auto-generated metadata for all stories
✅ Infrastructure: Weekly batch processing with story generation
```

### **Week 3 Priorities**
1. **TTS Provider Setup** - ElevenLabs/Azure Speech Services configuration
2. **Voice Selection** - Natural, engaging voices for different audiences
3. **Audio Pipeline** - Convert stories to high-quality audio files
4. **SSML Processing** - Optimize pacing, emphasis, and naturalness
5. **Audio Storage** - Organized file management with metadata

### **Critical Dependencies**
- [x] **API Keys**: OpenAI for story generation (configured and tested)
- [x] **Storage Setup**: Organized file structure for generated content
- [x] **Prompt Engineering**: Templates for consistent, high-quality output
- [x] **Error Handling**: Robust failure recovery and retry logic
- [ ] **TTS API Keys**: ElevenLabs/Azure for voice synthesis
- [ ] **Audio Processing**: FFmpeg for audio manipulation and optimization

---

## 🔧 **File Structure**

```
📁 guidora-automation/
├── 📁 scripts/
│   ├── ✅ csv2json.py           # Data preprocessing
│   └── ✅ read_surahs.py        # Verse lookup utilities
├── 📁 lib/
│   ├── ✅ learning_extractor.py # Core extraction logic
│   ├── ✅ fingerprints.py       # Uniqueness detection
│   ├── ✅ weekly_cadence.py     # Batch processing
│   ├── ✅ llm_tools.py          # Week 2: LLM integration
│   ├── 📝 providers/
│   │   ├── 📝 tts_api.py        # Week 3: TTS providers
│   │   └── 📝 storage_client.py # Cloud storage
│   └── 📝 video_tools/
│       ├── 📝 video_assembler.py # Week 4: Video creation
│       └── 📝 youtube_uploader.py # Week 5: Publishing
├── 📁 data/
│   ├── ✅ tafsir/quran_filtered.jsonl # Source data
│   ├── ✅ learnings/learnings.jsonl   # Extracted wisdom
│   └── ✅ stories/stories.jsonl       # Generated stories
├── 📁 prompts/
│   ├── ✅ story_universal.txt    # Week 2: Universal audience
│   ├── ✅ story_muslim.txt       # Week 2: Muslim community
│   ├── ✅ story_spiritual.txt    # Week 2: Spiritual seekers
│   ├── ✅ youtube_metadata.txt   # YouTube optimization
│   ├── 📝 description_en.txt    # YouTube descriptions
│   └── 📝 title_en.txt          # Title generation
└── 📁 .github/workflows/
    └── 📝 weekly_generation.yml  # Week 6: Automation
```

**Legend**: ✅ Complete | 🔄 In Progress | 📝 Planned

---

## 📈 **Success Metrics**

### **Quality Metrics**
- **Uniqueness Rate**: >95% unique content (fingerprint-verified)
- **Engagement**: Universal, relatable storytelling for all audiences
- **Authenticity**: Faithful to original Quranic wisdom and scholarship

### **Production Metrics**
- **Processing Speed**: 200 verses/week sustainable rate
- **Automation Reliability**: >99% successful weekly runs
- **Cost Efficiency**: <$50/week for full pipeline operation

### **Growth Metrics**
- **Content Volume**: 52 videos/year fully automated
- **Multi-Language**: EN/UR/HI localization by V1.0
- **Platform Expansion**: YouTube + Shorts by V1.1
