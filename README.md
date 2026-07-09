# AskTheVideo

A RAG-based chatbot that answers questions about a specific YouTube video's
content — e.g. "does this podcast cover LangChain?" — grounded strictly in
the video's actual transcript, not the model's general knowledge.

Built as a portfolio project to demonstrate real AI engineering practice
(architecture, evaluation, verification) rather than just prompting.

## Status: M2 complete

The core RAG pipeline (M1) is restructured into a proper multi-file
architecture and validated against two hand-built eval sets (30
question/answer pairs total) — **30/30 correct**, including proper
rejection of all out-of-scope/trick questions.

A full-stack UI (M2) now wraps the pipeline: a FastAPI backend (`api.py`)
exposes it as a REST API, and a React frontend (`frontend/`) consumes it —
tested against both happy-path and failure-path scenarios (empty input,
server down, uncaptioned videos, asking before loading a video).

See [`REQUIREMENTS.md`](./REQUIREMENTS.md) for full scope, success
criteria, the milestone roadmap (M1 → M4), and tracked open questions
(including one observed edge case in name-attribution grounding).

`AskTheVideo_v0_prototype.ipynb` is preserved as the original working
single-notebook prototype this project was refactored from.

## How it works

1. **Ingestion** (`ingestion.py`) — fetches a YouTube video's transcript
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
ingestion.py        # transcript fetching
indexing.py           # chunking, embedding, FAISS build/save/load
retrieval.py            # retriever configuration
chain.py                  # prompt + LLM + LCEL chain
main.py                     # CLI entry point
api.py                        # FastAPI backend
frontend/                       # React frontend (Vite)
eval_set.py                        # eval set #1 (Simon Sinek TED talk)
eval_set_2.py                         # eval set #2 (Elon Musk TED interview)
run_eval.py                              # runs an eval set automatically
requirements.txt                            # backend dependency versions
```

## Setup

**Backend:**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with a free Gemini API key
([aistudio.google.com/apikey](https://aistudio.google.com/apikey)):
```
GOOGLE_API_KEY=your_key_here
```

**Frontend:**
```powershell
cd frontend
npm install
```

## Usage

**Run the full stack (two terminals):**
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

**API only** (interactive docs at `http://127.0.0.1:8000/docs`):
```powershell
uvicorn api:app --reload
```

**Re-run the eval sets:**
```powershell
python run_eval.py
```

## Tech stack

- `youtube-transcript-api` — transcript extraction
- LangChain (LCEL) — orchestration
- Google Gemini: `gemini-2.5-flash` (chat) + `gemini-embedding-001` (embeddings)
- FAISS — vector store
- FastAPI — backend API
- React (Vite) — frontend

## Roadmap

- **M3** — public deployment (backend + frontend hosted separately)
- **M4** — error handling, edge cases, rate-limit UX polish

## Known limitations (by design, for now)

- Single video at a time, English captions only
- No audio-transcription fallback for videos without captions
- No multi-video search