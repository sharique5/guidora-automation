# Guidora — Project Checklist & MVP Schedule

**Status**: 🚀 **Week 3 Complete** - Text-to-Speech Pipeline MVP with OpenAI TTS ✅  
**Next**: Week 4 - Video Assembly MVP  
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

### **✅ Week 3: Text-to-Speech Pipeline MVP** (COMPLETED)
- [x] **TTS Providers**: Platform-agnostic multi-provider support (OpenAI, Google, ElevenLabs) (`lib/providers/tts_api.py`)
- [x] **Voice Selection**: Intelligent voice selection system for different audiences (`lib/tts_manager.py`)
- [x] **Audio Generation**: Real MP3 audio file generation from story content
- [x] **Audio Pipeline**: Complete story→speech conversion with cost tracking
- [x] **Audio Storage**: Organized file management with metadata in `data/audio/files/`
- [x] **Batch Processing**: CLI tool for processing multiple stories (`scripts/audio_generator.py`)
- [x] **Output**: High-quality audio files (367.7s content) from generated stories ($0.0142 cost)

## Week 4: Multi-Language Video Assembly (Instadoodle Strategy) 🎬

### A) Enhanced Natural Language Translator ✅ COMPLETED
- [x] **Whiteboard-Optimized Script Generation** - Enhanced translator for clean, narration-ready scripts
- [x] **Short Sentence Structure** - 10-15 words maximum for visual pacing
- [x] **Cultural Adaptation** - Native expressions and slang per language
- [x] **Clean JSON Output** - No nested formatting, direct script field
- [x] **Quality Validation** - Script readability scoring and whiteboard readiness check
- [x] **Multi-Language Support** - Spanish, French, Urdu with regional authenticity

**Results:**
- ✅ Spanish translations with "carro", "coche" and natural expressions
- ✅ French translations with "bagnole", "voiture" and cultural nuances  
- ✅ Urdu translations with "mashallah", "subhanallah", "yaar" integration
- ✅ Average cost: ~$0.03 per story translation across all languages
- ✅ Quality scores: 8-10/10 readability, all languages whiteboard-ready
- ✅ Duration estimation: 76-285 seconds depending on language density

### B) Video Storage Organization ✅ COMPLETED
- [x] **Multi-Language Directory Structure** - Organized videos by production stage and language
- [x] **Video Tracking System** - Comprehensive metadata tracking for all production stages
- [x] **Batch Management** - Smart batching system for efficient production workflow
- [x] **Publishing Scheduler** - Automated scheduling system with optimal distribution
- [x] **Production CLI** - Command-line interface for video management operations
- [x] **GitIgnore Configuration** - Protected large media files while preserving story content

**Results:**
- ✅ Directory structure: data/videos/{production,drafts,published}/{en,es,fr,ur}
- ✅ Video tracker with 8 production status stages (script_ready → published)
- ✅ Batch manager with intelligent language prioritization and scheduling
- ✅ CLI tool for registering scripts, managing batches, and scheduling uploads
- ✅ Production config with quality thresholds and upload scheduling
- ✅ 3 translated stories registered and ready for Instadoodle video creation

**Production Workflow:**
1. **Script Registration**: Translated stories automatically tracked
2. **Batch Planning**: Intelligent batching across languages (5 videos/batch)
3. **Instadoodle Creation**: Manual video creation with tracked progress
4. **Asset Management**: Video, thumbnail, and metadata tracking
5. **Publishing Schedule**: Automated multi-channel scheduling (2 videos/day)

### C) YouTube Multi-Channel Strategy � PLANNED
- [ ] **Language-Specific Channels** - Dedicated channels per language  
- [ ] **Automated Upload Scheduling** - Coordinated releases across languages
- [ ] **Cross-Language Linking** - Connect related videos across channels
- [ ] **Analytics Integration** - Track performance per language market

### **🎬 Week 5: Video Production & Multi-Channel Publishing MVP**
- [ ] **Video Organization System**: File management for videos by language and channel (`lib/video_tools/video_organizer.py`)
- [ ] **Multi-Language Thumbnails**: AI-generated thumbnails with language-specific text and cultural elements
- [ ] **Multi-Channel YouTube Setup**: Separate channels for different languages with proper branding
- [ ] **Batch Upload Pipeline**: Automated publishing across multiple language channels
- [ ] **Cross-Language SEO**: Optimized metadata for different regional markets
- [ ] **Output**: Organized multi-language video library with automated publishing

### **⚙️ Week 6: Global Automation & Analytics**
- [ ] **Multi-Language Workflows**: GitHub Actions for automated translation and formatting
- [ ] **Global Content Strategy**: Regional optimization and cultural sensitivity checks
- [ ] **Cross-Platform Analytics**: Performance tracking across language channels
- [ ] **Scalability Testing**: Load testing for multiple language processing
- [ ] **Cost Optimization**: Budget management for global content production
- [ ] **Output**: Fully automated global content generation system

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
- [x] **Text-to-Speech**: Natural voice synthesis (OpenAI TTS) - *Paused for Instadoodle integration*
- [ ] **Multi-Language Translation**: Conversational translations with cultural adaptation
- [ ] **Whiteboard Animation**: Instadoodle-based explainer video creation (manual process)
- [ ] **Visual Consistency**: Standardized branding across language versions
- [ ] **Video Organization**: Systematic storage and management by language

### **D. Publishing & Distribution**
- [ ] **Multi-Channel YouTube**: Automated uploads across language-specific channels
- [ ] **Global SEO Optimization**: Region-specific metadata and cultural adaptation
- [ ] **Cross-Language Analytics**: Performance tracking across different markets
- [ ] **Content Localization**: Strategic timing and cultural considerations per region

---

## 🎯 **Production Milestones**

### **MVP Completion (Week 6)**
**Goal**: End-to-end global automation generating weekly multi-language content
- ✅ Learning extraction from Quranic wisdom
- ✅ AI-powered story generation (English)
- 🌍 Natural language translation (Spanish, French, Hindi, Arabic)
- 🎬 Instadoodle whiteboard explainer creation (manual)
- 📺 Multi-channel YouTube publishing pipeline
- ⚙️ Global automation with cultural adaptation

### **V1.0 (Week 8-10)**
**Goal**: Production-ready global content system with quality controls
- [ ] **Content Review Interface**: Human oversight for multi-language content approval
- [ ] **Cultural Sensitivity**: Automated checks for regional appropriateness
- [ ] **Advanced Translation**: Context-aware localization with cultural nuance
- [ ] **Global Analytics**: Detailed performance tracking across markets
- [ ] **Cost Optimization**: Efficient translation and storage management

### **V1.1 (Week 12-16)**
**Goal**: Global growth and advanced localization features
- [ ] **Regional YouTube Shorts**: Vertical format with language-specific optimization
- [ ] **Cultural A/B Testing**: Region-specific content optimization
- [ ] **Advanced Localization**: AI-powered cultural adaptation and regional preferences
- [ ] **Global Performance Analytics**: Cross-market data analysis and insights
- [ ] **Multi-Platform Expansion**: Instagram, TikTok, Facebook with regional focus

---

## 📊 **Current Status & Next Actions**

### **Completed (Week 1-3)**
```
✅ Data: 6,236 verses processed, 0 duplicates
✅ Extraction: 4 unique learnings extracted with fingerprinting
✅ Story Generation: 4 professional stories (12.5 min content)
✅ LLM Integration: OpenAI API with cost controls ($0.29 total)
✅ YouTube Optimization: Auto-generated metadata for all stories
✅ Infrastructure: Weekly batch processing with story generation
✅ TTS Pipeline: Platform-agnostic audio generation with OpenAI TTS
✅ Audio Production: 367.7s high-quality MP3 content generated ($0.0142)
✅ Voice Selection: Intelligent audience-based voice mapping system
```

### **Week 4 Priorities**
1. **Natural Language Translator** - Build conversational translation system for Spanish, French, Hindi, Arabic
2. **Instadoodle Script Formatting** - Create whiteboard explainer format from story content
3. **Multi-Language Storage** - Organize translated stories by language for easy management
4. **Cultural Adaptation** - Ensure translations use natural slang and regional context
5. **Manual Video Workflow** - Document step-by-step Instadoodle creation process

### **Critical Dependencies**
- [x] **API Keys**: OpenAI for story generation and translation (configured and tested)
- [x] **Storage Setup**: Organized file structure for generated content
- [x] **Prompt Engineering**: Templates for consistent, high-quality output
- [x] **Error Handling**: Robust failure recovery and retry logic
- [x] **TTS Integration**: OpenAI TTS (paused for Instadoodle integration)
- [ ] **Translation API**: Multi-language support with cultural adaptation
- [ ] **Instadoodle Account**: Premium subscription for whiteboard video creation
- [ ] **Multi-Channel Setup**: YouTube channels for different languages

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
│   ├── ✅ tts_manager.py        # Week 3: TTS orchestration (paused)
│   ├── 📝 translators/
│   │   └── 📝 natural_translator.py # Week 4: Multi-language translation
│   ├── ✅ providers/
│   │   ├── ✅ tts_api.py        # Week 3: TTS providers (paused)
│   │   └── 📝 storage_client.py # Cloud storage
│   └── 📝 video_tools/
│       ├── 📝 instadoodle_formatter.py # Week 4: Whiteboard script format
│       ├── 📝 video_organizer.py # Week 5: Multi-language video management
│       └── 📝 youtube_uploader.py # Week 5: Multi-channel publishing
├── 📁 data/
│   ├── ✅ tafsir/quran_filtered.jsonl # Source data
│   ├── ✅ learnings/learnings.jsonl   # Extracted wisdom
│   ├── ✅ videos/videos.jsonl         # Generated stories with metadata
│   ├── ✅ audio/files/                # Week 3: Generated audio files (paused)
│   └── 📝 stories/                    # Week 4: Multi-language stories
│       ├── 📝 en/                     # English stories
│       ├── 📝 es/                     # Spanish stories
│       ├── 📝 fr/                     # French stories
│       ├── 📝 ur/                     # Urdu stories
│       └── 📝 ar/                     # Arabic stories
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
