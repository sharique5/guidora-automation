# Guidora — Project Checklist & MVP Schedule

**Status**: 🚀 **Week 1 Complete** - Learning Extraction & Fingerprinting MVP ✅  
**Next**: Week 2 - LLM Story Generation MVP  
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

### **🔄 Week 2: LLM Story Generation MVP**
- [ ] **LLM Integration**: OpenAI/Gemini API wrapper with retry logic (`lib/llm_tools.py`)
- [ ] **Story Prompts**: Template system for universal, modern storytelling (`prompts/story_*.txt`)
- [ ] **Universalization**: Islamic→Universal term translation filter
- [ ] **Story Generator**: Convert learnings to engaging, relatable stories
- [ ] **Audience Targeting**: Custom prompts for different audience groups
- [ ] **Output**: Generated stories from extracted learnings with metadata

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
- [ ] **Story Generation**: LLM-powered modern storytelling with universal language
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
- 🔄 AI-powered story generation
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

### **Completed (Week 1)**
```
✅ Data: 6,236 verses processed, 0 duplicates
✅ Extraction: 2 learnings from 100 verses (2% success rate)
✅ Fingerprinting: Semantic content uniqueness detection
✅ Infrastructure: Weekly batch processing framework
```

### **Week 2 Priorities**
1. **LLM Integration Setup** - OpenAI/Gemini API configuration
2. **Story Generation Prompts** - Universal storytelling templates
3. **Learning→Story Pipeline** - Convert extracted wisdom to engaging content
4. **Quality Validation** - Ensure appropriate tone and universal language
5. **Batch Processing** - Generate stories for all extracted learnings

### **Critical Dependencies**
- [ ] **API Keys**: OpenAI/Gemini for story generation
- [ ] **Storage Setup**: Organized file structure for generated content
- [ ] **Prompt Engineering**: Templates for consistent, high-quality output
- [ ] **Error Handling**: Robust failure recovery and retry logic

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
│   ├── 🔄 llm_tools.py          # Week 2: LLM integration
│   ├── 📝 providers/
│   │   ├── 📝 tts_api.py        # Week 3: TTS providers
│   │   └── 📝 storage_client.py # Cloud storage
│   └── 📝 video_tools/
│       ├── 📝 video_assembler.py # Week 4: Video creation
│       └── 📝 youtube_uploader.py # Week 5: Publishing
├── 📁 data/
│   ├── ✅ tafsir/quran_filtered.jsonl # Source data
│   └── ✅ learnings/learnings.jsonl   # Extracted wisdom
├── 📁 prompts/
│   ├── 📝 story_en.txt          # Week 2: Story templates
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
