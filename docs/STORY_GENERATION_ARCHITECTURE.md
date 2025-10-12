# Story Generation Architecture - Week 2 MVP

## Overview
Transform practical Islamic wisdom into modern, universal stories that resonate across cultures and demographics. Create engaging 2-3 minute video content that delivers timeless wisdom through relatable scenarios.

## Story Structure Framework

### 1. **Core Story Components**
```
- **Hook** (15-20 words): Attention-grabbing opening
- **Scenario** (100-150 words): Modern, relatable situation
- **Conflict/Challenge** (50-75 words): Realistic problem/dilemma
- **Wisdom Application** (75-100 words): How the learning resolves the situation
- **Universal Takeaway** (25-50 words): Actionable insight for all audiences
```

### 2. **Story Categories**
Based on our current learnings, we'll generate stories in these categories:

#### **A. Spiritual Practice Stories** (Learning 1 & 2)
- **Modern Scenarios**: Busy professional, student stress, family chaos
- **Wisdom Focus**: Mindfulness, daily reflection, inner peace practices
- **Universal Appeal**: Meditation, gratitude, mindful moments

#### **B. Faith & Recognition Stories** (Learning 3)
- **Modern Scenarios**: Career setbacks, life transitions, nature appreciation
- **Wisdom Focus**: Finding meaning, recognizing patterns, building resilience
- **Universal Appeal**: Purpose, wonder, perspective

#### **C. Ethical Relationships Stories** (Learning 4)
- **Modern Scenarios**: Workplace conflicts, family dynamics, community issues
- **Wisdom Focus**: Conscious decision-making, empathy, integrity
- **Universal Appeal**: Respect, fairness, compassion

### 3. **Audience Adaptation Strategy**

#### **Universal/All Humanity** (Primary Target)
- Secular language, universal values
- Focus on human psychology and relationships
- Remove religious terminology, keep wisdom essence

#### **General Muslim Community** (Secondary)
- Balance Islamic terms with universal concepts
- Include spiritual context while remaining accessible
- Reference Islamic concepts naturally

#### **Spiritual Seekers** (Tertiary)
- Include spiritual/metaphysical language
- Focus on inner growth and consciousness
- Bridge religious and secular spirituality

### 4. **Story Generation Pipeline**

```
Learning Input → Audience Selection → Template Selection → LLM Generation → Quality Check → Storage
```

#### **Input Processing**
1. Extract practical_application from learning
2. Identify primary theme and audience
3. Select appropriate story template
4. Generate modern scenario context

#### **LLM Integration Points**
1. **Scenario Generation**: Create relatable modern situations
2. **Character Development**: Build authentic, diverse characters
3. **Dialogue Writing**: Natural conversations that reveal wisdom
4. **Narrative Flow**: Engaging story progression
5. **Universal Translation**: Adapt religious concepts for broad appeal

### 5. **Quality Criteria**

#### **Engagement Metrics**
- Clear story arc with resolution
- Relatable characters and situations
- Emotional connection points
- Practical, actionable takeaways

#### **Accessibility Standards**
- 6th-8th grade reading level
- Cultural sensitivity across backgrounds
- Inclusive character representation
- Clear cause-and-effect relationships

#### **Content Guidelines**
- No preaching or religious conversion intent
- Focus on human values and wisdom
- Respect for diverse beliefs and practices
- Practical applicability in modern life

### 6. **Technical Implementation**

#### **Data Structure**
```python
@dataclass
class Story:
    id: str
    source_learning_id: str
    title: str
    description: str
    content: str
    category: str  # spiritual_practice, faith_recognition, ethical_relationships
    target_audience: str
    estimated_duration: int  # seconds
    themes: List[str]
    characters: List[str]
    setting: str
    generated_at: str
    quality_score: float
```

#### **File Organization**
```
data/stories/
├── stories.jsonl           # All generated stories
├── by_category/
│   ├── spiritual_practice.jsonl
│   ├── faith_recognition.jsonl
│   └── ethical_relationships.jsonl
└── by_audience/
    ├── universal.jsonl
    ├── muslim_community.jsonl
    └── spiritual_seekers.jsonl
```

### 7. **MVP Success Metrics**

#### **Week 2 Goals**
- ✅ Generate 4 stories (1 per existing learning)
- ✅ Test 2 audience adaptations per story (8 total variations)
- ✅ Validate story quality and engagement potential
- ✅ Establish reliable LLM integration

#### **Quality Benchmarks**
- Story coherence: Manual review (pass/fail)
- Reading level: Automated analysis (6th-8th grade)
- Cultural sensitivity: Manual review checklist
- Practical applicability: Test audience feedback

### 8. **Next Phase Integration**

#### **Week 3: TTS Pipeline**
- Stories → Audio files
- Voice selection for different audiences
- Pacing and emphasis optimization

#### **Week 4: Video Assembly**
- Audio + visuals + background music
- Scene timing based on story structure
- Cultural/audience-appropriate imagery

## Implementation Plan

### Phase 1: Foundation (This Week)
1. Build LLM integration module
2. Create story prompt templates
3. Develop story generator class
4. Implement storage system

### Phase 2: Testing & Validation
1. Generate test stories from 4 learnings
2. Manual quality review
3. Audience adaptation testing
4. Refine prompts and templates

### Phase 3: Pipeline Integration
1. Update weekly cadence system
2. Automated story generation workflow
3. Quality assurance automation
4. Prepare for Week 3 TTS integration

---

**Key Insight**: Stories should feel like modern parables - timeless wisdom delivered through contemporary scenarios that anyone can relate to, regardless of their religious or cultural background.