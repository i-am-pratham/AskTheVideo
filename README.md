# AskTheVideo

A RAG-based chatbot that answers questions about a specific YouTube video's
content — e.g. "does this podcast cover LangChain?" — grounded strictly in
the video's actual transcript, not the model's general knowledge.

Built as a portfolio project to demonstrate real AI engineering practice
(architecture, evaluation, deployment) rather than just prompting.

**Live app:** https://askthevideo-frontend.vercel.app
**Live API docs:** https://askthevideo-api.onrender.com/docs

## Status: M3 complete — deployed and publicly accessible

- **M1** — core RAG pipeline restructured into a proper multi-file
  architecture, validated against two hand-built eval sets (30
  question/answer pairs total) — **30/30 correct**, including proper
  rejection of all out-of-scope/trick questions.
- **M2** — full-stack UI: FastAPI backend + React frontend, tested against
  both happy-path and failure-path scenarios.
- **M3** — deployed publicly: backend on Render, frontend on Vercel, CORS
  locked to the production frontend origin.

See [`REQUIREMENTS.md`](./REQUIREMENTS.md) for full scope, success
criteria, the milestone roadmap, and tracked open items (including a
naming-ambiguity edge case and a planned persistent-storage upgrade).

`AskTheVideo_v0_prototype.ipynb` is preserved as the original working
single-notebook prototype this project was refactored from.

## A real deployment lesson worth reading

The transcript-fetching approach that worked perfectly locally (scraping
YouTube directly via `youtube-transcript-api`) broke immediately once
deployed, because YouTube blocks requests from cloud/datacenter IP ranges
— a class of bug that only appears once you actually deploy, not during
local development. A free-tier proxy didn't fix it (still a datacenter
IP, just a different one). The real fix: switched to
[Supadata](https://supadata.ai), a hosted transcript API that fetches
transcripts on its own infrastructure — the backend now never talks to
YouTube directly at all. Simpler code, and no more IP-blocking to fight.

## Known limitations (by design, for now)

- **Ephemeral vector storage**: FAISS indexes live on local disk, which is
  wiped on every backend restart (free-tier hosting doesn't persist disk).
  Every video needs re-indexing after a backend restart. Tracked as an M4
  task — planned fix is migrating to a hosted vector store (Pinecone,
  Supabase+pgvector, or Qdrant Cloud, all with usable free tiers).
- Single video at a time, English captions only
- No multi-video search

## How it works

1. **Ingestion** (`ingestion.py`) — fetches a YouTube video's transcript
   via the Supadata API
2. **Indexing** (`indexing.py`) — splits the transcript into chunks, embeds
   them with Gemini, builds a FAISS vector store (rate-limit safe, with
   batching + retry for the free tier)
3. **Retrieval** (`retrieval.py`) — fetches the most relevant chunks for a
   given question
4. **Generation** (`chain.py`) — an LCEL chain combining retrieval, a
   grounding-focused prompt, and Gemini to produce an answer
5. **API** (`api.py`) — exposes the pipeline as `/index`, `/ask`, `/health`
6. **Frontend** (`frontend/`) — a React app for loading a video and asking
   questions through a browser

`main.py` also provides a CLI entry point for direct testing without the
frontend.

## Project structure

```
config.py          # centralized settings (models, chunk size, rate limits)
ingestion.py        # transcript fetching (via Supadata API)
indexing.py           # chunking, embedding, FAISS build/save/load
retrieval.py            # retriever configuration
chain.py                  # prompt + LLM + LCEL chain
main.py                     # CLI entry point
api.py                        # FastAPI backend
frontend/                       # React frontend (Vite), deployed on Vercel
eval_set.py                        # eval set #1 (Simon Sinek TED talk)
eval_set_2.py                         # eval set #2 (Elon Musk TED interview)
run_eval.py                              # runs an eval set automatically
requirements.txt                            # backend dependency versions
```

## Setup (local development)

**Backend:**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GOOGLE_API_KEY=your_gemini_key_here
SUPADATA_API_KEY=your_supadata_key_here
```
Free Gemini key: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
Free Supadata key (100 transcripts/month): [supadata.ai](https://supadata.ai)

**Frontend:**
```powershell
cd frontend
npm install
```
Create `frontend/.env`:
```
VITE_API_BASE=http://127.0.0.1:8000
```

## Usage

**Run the full stack locally (two terminals):**
```powershell
# Terminal 1 — backend
uvicorn api:app --reload

# Terminal 2 — frontend
cd frontend
npm run dev
```
Then open `http://localhost:5173`.

**CLI only:**
```powershell
python main.py
```

**Re-run the eval sets:**
```powershell
python run_eval.py
```

## Tech stack

- Supadata — hosted transcript extraction
- LangChain (LCEL) — orchestration
- Google Gemini: `gemini-2.5-flash` (chat) + `gemini-embedding-001` (embeddings)
- FAISS — vector store
- FastAPI — backend API, deployed on Render
- React (Vite) — frontend, deployed on Vercel

## Roadmap

- **M4** — persistent vector storage, error handling polish, edge cases,
  rate-limit UX