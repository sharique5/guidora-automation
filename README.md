# guidora-automation

# Guidora

**Tagline:** *Your journey, guided.*

Guidora is an automation‑first pipeline that turns timeless insights into short, universal stories and publishes them to YouTube with multilingual subtitles and (optionally) native voiceovers.

> Source of truth is grounded in vetted texts and commentaries; LLMs are used for summarization & storytelling, not rulings.

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Dry run (stub providers):
python -m src.guidora.pipeline --surah 1 --ayah 1 --lang en --dry-run
```
