"""
Handles splitting transcripts into chunks, embedding them, and
building/saving/loading the FAISS vector store.
"""
import os
import time

from google.genai.errors import ClientError
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

import config


def split_transcript(transcript: str):
    """Splits raw transcript text into overlapping chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.create_documents([transcript])
    return chunks


def get_embeddings_model():
    """Returns a configured Gemini embeddings model instance."""
    return GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)


def embed_in_batches(docs, embeddings_model):
    """
    Embeds documents in small batches with pauses, to stay under
    Gemini's free-tier rate limit (100 requests/minute), retrying
    with backoff if we still get rate-limited.
    """
    vector_store = None
    batch_size = config.EMBED_BATCH_SIZE
    pause = config.EMBED_PAUSE_SECONDS
    max_retries = config.EMBED_MAX_RETRIES

    total_batches = (len(docs) - 1) // batch_size + 1

    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        attempt = 0
        while True:
            try:
                if vector_store is None:
                    vector_store = FAISS.from_documents(batch, embeddings_model)
                else:
                    vector_store.add_documents(batch)
                break
            except ClientError as e:
                attempt += 1
                if attempt > max_retries or "RESOURCE_EXHAUSTED" not in str(e):
                    raise
                wait = pause * attempt
                print( 
                    f"Rate limited on batch {i // batch_size + 1}, "
                    f"retrying in {wait}s (attempt {attempt}/{max_retries})..."
                )
                time.sleep(wait)

        print(
            f"Embedded batch {i // batch_size + 1}/{total_batches} "
            f"({len(batch)} chunks)"
        )
        time.sleep(pause)

    return vector_store


def build_index(video_id: str, transcript: str):
    """
    Full pipeline: split transcript -> embed -> build FAISS index.
    Returns the vector store (does not save it — see save_index).
    """
    chunks = split_transcript(transcript)
    print(f"Split into {len(chunks)} chunks")

    embeddings_model = get_embeddings_model()
    vector_store = embed_in_batches(chunks, embeddings_model)
    return vector_store


def save_index(vector_store, video_id: str):
    """Saves a FAISS index to disk, in a per-video folder."""
    path = os.path.join(config.INDEX_STORAGE_DIR, video_id)
    vector_store.save_local(path)
    return path


def load_index(video_id: str):
    """Loads a previously saved FAISS index for a given video."""
    path = os.path.join(config.INDEX_STORAGE_DIR, video_id)
    embeddings_model = get_embeddings_model()
    vector_store = FAISS.load_local(
        path, embeddings_model, allow_dangerous_deserialization=True
    )
    return vector_store


def index_exists(video_id: str) -> bool:
    """Checks whether a saved index already exists for this video."""
    path = os.path.join(config.INDEX_STORAGE_DIR, video_id)
    return os.path.isdir(path)