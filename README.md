# AskTheVideo

A RAG-based chatbot that answers questions about a specific YouTube video's
content — e.g. "does this podcast cover LangChain?" — grounded strictly in
the video's actual transcript, not the model's general knowledge.

Built as a portfolio project to demonstrate real AI engineering practice
(architecture, evaluation, verification) rather than just prompting.

## Status: M1 complete

The core RAG pipeline is restructured into a proper multi-file architecture
and validated against two hand-built eval sets (30 question/answer pairs
total, across a scripted TED talk and a messy conversational interview) —
**30/30 correct**, including proper rejection of all out-of-scope/trick
questions.

See [`REQUIREMENTS.md`](./REQUIREMENTS.md) for full scope, success
criteria, and the milestone roadmap (M1 → M4).

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

`main.py` ties these together into a runnable CLI: give it a video ID, ask
questions, get transcript-grounded answers.

## Project structure

```
config.py         # centralized settings (models, chunk size, rate limits)
ingestion.py      # transcript fetching
indexing.py       # chunking, embedding, FAISS build/save/load
retrieval.py      # retriever configuration
chain.py          # prompt + LLM + LCEL chain
main.py           # entry point — run this
eval_set.py       # eval set #1 (Simon Sinek TED talk)
eval_set_2.py     # eval set #2 (Elon Musk TED interview)
run_eval.py       # runs an eval set automatically against a built index
requirements.txt  # exact dependency versions
```

## Setup

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

## Usage

```powershell
python main.py
```
Enter a YouTube video ID (not the full URL) when prompted, then ask
questions about it. Type `exit` to quit.

To re-run the eval sets against a video you've already indexed:
```powershell
python run_eval.py
```

## Tech stack

- `youtube-transcript-api` — transcript extraction
- LangChain (LCEL) — orchestration
- Google Gemini: `gemini-2.5-flash` (chat) + `gemini-embedding-001` (embeddings)
- FAISS — vector store

## Roadmap

- **M2** — simple UI (Streamlit), replacing the CLI loop
- **M3** — public deployment
- **M4** — error handling, edge cases, rate-limit UX polish

## Known limitations (by design, for now)

- Single video at a time, English captions only
- No audio-transcription fallback for videos without captions
- No multi-video search