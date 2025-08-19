# Guidora — Project Checklist

Use this as your single source of truth. Convert items to GitHub Issues and link PRs.

## A. Foundation
- [x] Create repo, branch protection, CI
- [ ] Secrets policy + `.env.example`
- [x] Pick YouTube handle **@YourGuidora**
- [x] Finalize brand (logo, colors, thumbnail style)

## B. Data & Grounding
- [ ] Implement `providers/quran_api.py` (ayah + translation + tafsir)
- [ ] Caching & retries; sample fixtures for tests
- [ ] Define grounding rules (no rulings, cite tafsir lines)

## C. LLM & Content
- [ ] `llm.py`: learning extraction (JSON) from provided context
- [ ] `llm.py`: story generation (tone/length guardrails)
- [ ] Universalization filter (Islamic → universal)
- [ ] Title/description prompts

## D. Assembly
- [ ] `i18n.py`: translate to EN/UR/HI (+AR later)
- [ ] SRT generator with basic timing
- [ ] `tts.py`: ElevenLabs + Google TTS (SSML)
- [ ] `video.py`: slideshow MP4 (ffmpeg/moviepy), 1080p
- [ ] Thumbnail template

## E. Publishing
- [ ] `uploader.py`: YouTube OAuth (device flow), upload, schedule
- [ ] Localized title/description per language
- [ ] Multi-playlist routing (EN/UR/HI)
- [ ] Idempotent publish logs

## F. Ops & Quality
- [ ] Observability: structured logs + error alerts
- [ ] Cost telemetry: tokens, TTS seconds, render time
- [ ] Golden tests for prompts (snapshot JSON)
- [ ] Reviewer UI (approve/edit → publish)
- [ ] Content policy checks (banned claims, tone)

## G. Growth
- [ ] Shorts auto-cuts (vertical)
- [ ] A/B titles & thumbnails
- [ ] Analytics export (sheets/DB)
- [ ] Roadmap: multi-audio tracks when GA

### Milestones
- **MVP (~2 weeks):** fetch → story → TTS → slideshow → unlisted upload
- **v1 (~1 month):** multilingual, reviewer gate, scheduler, telemetry
- **v1.1:** Shorts + A/B testing
