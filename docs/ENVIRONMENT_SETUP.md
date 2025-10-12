# Environment Setup Guide

## Quick Start

1. **Copy the template**:
   ```bash
   copy .env.example .env
   ```

2. **For immediate story generation testing**, you only need ONE of these:
   ```
   # Option A: OpenAI (recommended for MVP)
   OPENAI_API_KEY=sk-your-actual-key-here
   
   # Option B: Anthropic Claude (alternative)
   ANTHROPIC_API_KEY=your-actual-key-here
   ```

3. **Test the system**:
   ```bash
   python scripts/story_generator.py
   ```

## API Key Setup Instructions

### 🤖 OpenAI (Recommended for MVP)
1. Go to https://platform.openai.com/api-keys
2. Sign up/login to your account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add to `.env`: `OPENAI_API_KEY=sk-your-key-here`

**Cost**: ~$0.25 for generating stories from all 4 learnings

### 🧠 Anthropic Claude (Alternative)
1. Go to https://console.anthropic.com/
2. Sign up/login to your account  
3. Go to API Keys section
4. Create a new key
5. Add to `.env`: `ANTHROPIC_API_KEY=your-key-here`

**Cost**: Similar to OpenAI, ~$0.25 for 4 stories

## Immediate Next Steps

### Week 2: Story Generation (Current)
- ✅ Set up either OpenAI or Anthropic API key
- ✅ Run `python scripts/story_generator.py`
- ✅ Review generated stories in `data/stories/`

### Week 3: Text-to-Speech
- Set up ElevenLabs or Azure Speech Services
- Convert stories to audio files

### Week 5: YouTube Publishing  
- Set up YouTube Data API v3
- Enable automated video uploads

## Cost Management

The system includes built-in cost controls:
- Maximum $0.10 per LLM request
- Daily/monthly limits configurable
- Real-time cost tracking
- Automatic failover between providers

## Security Notes

⚠️ **Important**: 
- Never commit your actual `.env` file to git
- The `.env` file is already in `.gitignore`
- Only edit `.env.example` for adding new template variables
- Keep your API keys secure and rotate them regularly

## Testing Without API Keys

You can test the complete system architecture without API keys using:
```bash
python scripts/story_generator_demo.py
```

This generates sample stories showing exactly what the system produces.