# Story Storage System Documentation

## Directory Structure

```
data/stories/
├── stories.jsonl                    # Main file with all generated stories
├── by_category/                     # Stories organized by content category
│   ├── spiritual_practice.jsonl
│   ├── faith_recognition.jsonl
│   ├── ethical_relationships.jsonl
│   └── general_wisdom.jsonl
└── by_audience/                     # Stories organized by target audience
    ├── universal.jsonl
    ├── muslim_community.jsonl
    └── spiritual_seekers.jsonl
```

## Story Data Schema

Each story is stored as a JSON object with the following structure:

```json
{
  "id": "story_3_1_universal_4d16a857",
  "source_learning_id": "learning_3_1_4d16a857",
  "title": "The Power of Mindful Moments",
  "description": "A busy professional discovers how small moments of awareness transform their day",
  "content": "Sarah stared at her computer screen...",
  "category": "spiritual_practice",
  "target_audience": "universal",
  "estimated_duration": 180,
  "themes": ["Faith", "Guidance", "Psychology"],
  "characters": ["Sarah", "professional", "colleague"],
  "setting": "office",
  "youtube_title": "How 3 Minutes Changed My Entire Workday",
  "youtube_description": "Discover the simple practice that transformed stress into peace...",
  "youtube_tags": ["mindfulness", "workplace", "stress relief", "productivity"],
  "thumbnail_concept": "Professional at desk with peaceful expression, warm lighting",
  "target_keywords": ["mindfulness at work", "stress relief", "daily practice"],
  "generation_metadata": {
    "story_tokens": 456,
    "metadata_tokens": 123,
    "total_cost": 0.0234,
    "model_used": "gpt-4-turbo",
    "prompt_type": "universal"
  },
  "generated_at": "2025-10-12T20:45:00.123456",
  "quality_score": 0.0
}
```

## Field Descriptions

### Core Story Fields
- `id`: Unique identifier combining source learning and audience
- `source_learning_id`: References the original learning that inspired this story
- `title`: Story title for internal use
- `description`: Brief description of the story content
- `content`: Full story text (300-500 words)

### Categorization
- `category`: Content theme (spiritual_practice, faith_recognition, ethical_relationships, general_wisdom)
- `target_audience`: Primary audience (universal, muslim_community, spiritual_seekers)
- `themes`: Array of main themes from source learning

### Story Elements
- `characters`: Main characters or character types in the story
- `setting`: Primary location/environment
- `estimated_duration`: Video length in seconds

### YouTube Optimization
- `youtube_title`: Optimized title for YouTube (60 chars max)
- `youtube_description`: Video description for YouTube
- `youtube_tags`: Array of relevant tags for discovery
- `thumbnail_concept`: Description for thumbnail design
- `target_keywords`: SEO keywords for ranking

### Metadata
- `generation_metadata`: LLM usage stats and generation details
- `generated_at`: ISO timestamp of story creation
- `quality_score`: Future quality assessment (0.0-1.0)

## Storage Operations

### Writing Stories
Stories are automatically saved to multiple files:
1. **Main file**: `stories.jsonl` - All stories for global access
2. **Category file**: `by_category/{category}.jsonl` - Filtered by content type
3. **Audience file**: `by_audience/{audience}.jsonl` - Filtered by target audience

### Reading Stories
Use standard JSONL reading patterns:

```python
# Read all stories
with open('data/stories/stories.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            story = json.loads(line)
            # Process story

# Read by category
with open('data/stories/by_category/spiritual_practice.jsonl', 'r', encoding='utf-8') as f:
    spiritual_stories = [json.loads(line) for line in f if line.strip()]

# Read by audience
with open('data/stories/by_audience/universal.jsonl', 'r', encoding='utf-8') as f:
    universal_stories = [json.loads(line) for line in f if line.strip()]
```

## Performance Considerations

- **Append-only**: Stories are appended to files for efficiency
- **No deduplication**: Each generation creates a new story (use unique IDs)
- **Parallel reading**: Category and audience files allow filtered access
- **Size management**: Monitor file sizes; implement rotation if needed

## Quality Management

The `quality_score` field is reserved for future quality assessment:
- Manual review scores
- Engagement metrics
- A/B testing results
- Automated quality checks

## Integration Points

### With Learning Extraction
- `source_learning_id` links stories to their source wisdom
- Stories inherit themes and audience data from learnings

### With TTS Pipeline (Week 3)
- `content` field provides text for speech synthesis
- `estimated_duration` helps with audio planning

### With Video Assembly (Week 4)
- `thumbnail_concept` guides visual design
- `setting` and `characters` inform scene selection

### With YouTube Publisher (Week 5)
- `youtube_*` fields provide optimized metadata
- `target_keywords` support SEO strategy