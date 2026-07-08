"""
FastAPI backend for AskTheVideo.
Exposes the existing RAG pipeline (ingestion, indexing, retrieval,
chain) as HTTP endpoints a frontend can call.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import ingestion
import indexing
import retrieval
import chain as chain_module

app = FastAPI(title="AskTheVideo API")

# Allows a React app running on a different port (localhost:3000)
# to call this API (running on localhost:8000). Without this,
# browsers block the request by default for security reasons.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for local development; tighten before deploying publicly
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keeps built chains in memory per video_id, so we don't rebuild
# the retriever/chain on every single question.
_chain_cache = {}


class IndexRequest(BaseModel):
    video_id: str


class QuestionRequest(BaseModel):
    video_id: str
    question: str


def _get_chain(video_id: str):
    if video_id not in _chain_cache:
        if not indexing.index_exists(video_id):
            raise HTTPException(
                status_code=404,
                detail=f"No index found for {video_id}. Call /index first.",
            )
        vector_store = indexing.load_index(video_id)
        retriever = retrieval.get_retriever(vector_store)
        _chain_cache[video_id] = chain_module.build_chain(retriever)
    return _chain_cache[video_id]


@app.post("/index")
def index_video(req: IndexRequest):
    """
    Indexes a video if not already indexed. Returns quickly if an
    index already exists on disk.
    """
    video_id = req.video_id

    if indexing.index_exists(video_id):
        return {"status": "already_indexed", "video_id": video_id}

    try:
        transcript = ingestion.get_transcript(video_id)
        vector_store = indexing.build_index(video_id, transcript)
        indexing.save_index(vector_store, video_id)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "indexed", "video_id": video_id}


@app.post("/ask")
def ask_question(req: QuestionRequest):
    """Answers a question about a previously indexed video."""
    qa_chain = _get_chain(req.video_id)
    answer = qa_chain.invoke(req.question)
    return {"video_id": req.video_id, "question": req.question, "answer": answer}


@app.get("/health")
def health():
    """Simple check that the API is running."""
    return {"status": "ok"}