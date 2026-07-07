# AskTheVideo — Requirements & Specification

## Purpose
A RAG-based chatbot that answers questions about a specific YouTube video's
content — e.g. "does this podcast cover LangChain?" — grounded in the
video's actual transcript, not the model's general knowledge.

## Primary audience
Portfolio/resume piece first — built to demonstrate real AI engineering
practice (not just prompting) for AI Backend Engineer / GenAI Developer
roles. Secondary goal: a working public demo others can actually try.

## Scope (v1)

### In scope
- Single YouTube video at a time, with existing English captions
  (manual or auto-generated)
- User submits a video URL/ID once; system ingests and indexes it
- User asks free-text questions about that video's content
- Answers are grounded strictly in the transcript (no hallucinated claims)
- System says "I don't know" when the transcript doesn't cover the question
- Deployed and reachable via a public URL, not just local/Colab execution

### Out of scope (explicitly, for now)
- Non-English videos / auto-translation
- Videos without any captions available (no audio transcription fallback yet)
- Multi-video search/collections
- User accounts, auth, or saved history
- Real-time/streaming video support

## Success criteria (how we know v1 is "done")
1. **Accuracy**: on a fixed eval set of 15 known Q&A pairs (from one test
   video), the system answers correctly on at least 80%
2. **Reliability**: ingesting a new video (up to ~4 hours) completes
   without manual intervention, including handling rate limits gracefully
3. **Deployment**: a person with no code access can open a URL, paste a
   video link, and ask questions — no Colab, no local setup required
4. **Honesty**: for out-of-scope questions (topic not in video), the system
   declines rather than fabricating an answer, verified against a small
   set of "trick" questions in the eval set

## Milestones toward v1
- **M1 — Core pipeline correctness**: restructured multi-file code,
  working reliably for one video, with the eval set passing threshold
  (this is what we're about to build)
- **M2 — Simple UI**: a minimal interface (Streamlit or similar) replacing
  notebook cells — usable by someone who isn't you
- **M3 — Deployment**: hosted somewhere with a public URL (e.g. Streamlit
  Community Cloud, Render, HuggingFace Spaces — free tiers)
- **M4 — Polish**: error handling for bad URLs, no-captions videos,
  loading states, basic rate-limit messaging in the UI itself

## Tech stack (locked in from prototype, carried forward)
- `youtube-transcript-api` — transcript extraction
- LangChain (LCEL) — orchestration
- Google Gemini: `gemini-2.5-flash` (chat) + `gemini-embedding-001` (embeddings)
- FAISS — vector store
- Chunking: `chunk_size=1000-1500`, `chunk_overlap=200-300` (tune during eval)

## Open questions (revisit later, not blocking M1)
- Does storing timestamps per chunk improve answer usefulness enough to
  prioritize before M2?
- What happens on Gemini free-tier rate limits during a live demo — need a
  UX-level answer, not just backend retry logic