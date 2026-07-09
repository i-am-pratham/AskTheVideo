"""
Central configuration for AskTheVideo.
All other modules import settings from here instead of hardcoding values or reading environment variables directly. Its just need to import to other files
"""

import os
from dotenv import load_dotenv

load_dotenv()


GOOGLE_API_KEY= os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Make sure it's set in your .env file."
    )

# Model settings — change these in one place, affects the whole project
CHAT_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "models/gemini-embedding-001"
TEMPERATURE = 0.2


# Chunking settings
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300

# Embedding rate-limit handling (free tier: 100 requests/minute)
EMBED_BATCH_SIZE = 20
EMBED_PAUSE_SECONDS = 15
EMBED_MAX_RETRIES = 5


# Retrieval settings
RETRIEVER_K = 4

# Where FAISS indexes get saved locally (per-video subfolder created at runtime)
INDEX_STORAGE_DIR = "faiss_indexes"

#Used for getting the transcript of youtube in ingestion.py
SUPADATA_API_KEY = os.environ.get("SUPADATA_API_KEY")