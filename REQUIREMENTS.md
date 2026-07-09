# AskTheVideo — Requirements & Specification

## Purpose
A RAG-based chatbot that answers questions about a specific YouTube video's
content — e.g. "does this podcast cover LangChain?" — grounded in the
video's actual transcript, not the model's general knowledge.

## Primary audience
Portfolio/resume piece first — built to demonstrate real AI engineering
practice (not just prompting) for AI Backend Engineer / GenAI Developer
roles. Secondary goal: a working public demo others can actually try.

**Live app:** https://askthevideo-frontend.vercel.app
**Live API docs:** https://askthevideo-api.onrender.com/docs

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

## Success criteria — status: MET

1. **Accuracy**: ✅ validated against two 15-question eval sets (30 pairs
   total, across a scripted TED talk and a messy conversational
   interview) — **30/30 correct**, well above the 80% target
2. **Reliability**: ✅ ingestion completes without manual intervention,
   including rate-limit batching/retry for the embedding step
3. **Deployment**: ✅ live public URL, no code/Colab/local setup required
   for a user to try it
4. **Honesty**: ✅ all out-of-scope/trick questions across both eval sets
   correctly declined rather than fabricated

## Milestones — status

- **M1 — Core pipeline correctness**: ✅ done. Restructured into a
  multi-file architecture (`ingestion.py`, `indexing.py`, `retrieval.py`,
  `chain.py`, `config.py`), validated with the eval sets above.
- **M2 — Full-stack UI**: ✅ done. Built a FastAPI backend (`api.py`)
  exposing the pipeline as a REST API, and a React (Vite) frontend
  consuming it — a deliberate choice over the original "Streamlit or
  similar" plan, made to build genuine full-stack experience. Tested against happy-path and
  failure-path scenarios (empty input, server down, uncaptioned videos,
  asking before loading a video).
- **M3 — Deployment**: ✅ done. Backend deployed on Render (free tier),
  frontend deployed on Vercel (free tier), CORS locked to the production
  frontend origin. Required a mid-deployment architecture change — see
  "Deployment lessons" below.
- **M4 — Polish**: in progress, see tracked items below.

## M4 — tracked items

- **Persistent vector storage**: FAISS indexes currently live on local
  disk, which is wiped on every backend restart on Render's free tier.
  Migrate to a hosted vector store with a free tier (candidates:
  Pinecone, Supabase + pgvector, Qdrant Cloud) so indexed videos survive
  backend restarts. Requires updating `indexing.py` and `retrieval.py`,
  and re-running both eval sets to confirm no regression after migration.
- Error handling polish for bad URLs, no-captions videos, loading states
- Rate-limit UX messaging in the frontend itself (not just backend retry
  logic)

## Deployment lessons (real, encountered during M3)

The original transcript-fetching approach (`youtube-transcript-api`,
scraping YouTube directly) worked perfectly locally but failed
immediately once deployed to Render — YouTube blocks requests from
cloud/datacenter IP ranges, a class of bug that only surfaces once code
actually runs on real infrastructure, not during local development. A
free-tier Webshare proxy didn't fix it (still a datacenter IP, just a
different one — triggered Google's CAPTCHA challenge instead of a clean
block). The actual fix: switched to
[Supadata](https://supadata.ai), a hosted transcript API — the backend
no longer talks to YouTube directly at all, sidestepping the IP-blocking
problem entirely. Also simplified the code (no proxy config, no
library-specific exception juggling).

## Tech stack (current, as deployed)

- Supadata — hosted transcript extraction (replaced `youtube-transcript-api`
  after the deployment issue above)
- LangChain (LCEL) — orchestration
- Google Gemini: `gemini-2.5-flash` (chat) + `gemini-embedding-001` (embeddings)
- FAISS — vector store
- Chunking: `chunk_size=1500`, `chunk_overlap=300`
- FastAPI — backend API, deployed on Render
- React (Vite) — frontend, deployed on Vercel

## Open questions (revisit later)

- Does storing timestamps per chunk improve answer usefulness enough to
  prioritize before further polish?
- Observed edge case (M2 testing, video iG9CE55wbtY): when a video never
  states the speaker's name AND contains an unrelated same-named entity
  in an anecdote (e.g. "James Robinson" as a character, distinct from
  the actual speaker Ken Robinson), the bot correctly refuses to assume
  identity — but produces a confusing hedge instead of a clean answer.
  The underlying content stays correct/grounded, so this isn't a
  correctness bug — but worth revisiting for answer clarity, possibly by
  improving the prompt to better distinguish "named entities mentioned
  in the transcript" from "the speaker."