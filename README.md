# AskTheVideo

RAG-based chatbot for querying long YouTube videos (podcasts, lectures) — 
ask whether a topic is covered and get an answer grounded in the transcript.

## Status
v0 — working prototype in a single Colab notebook. Refactoring into a 
proper multi-file project in progress.

## Stack
- youtube-transcript-api — transcript extraction
- LangChain (LCEL) — orchestration
- Google Gemini (gemini-2.5-flash + gemini-embedding-001) — LLM + embeddings
- FAISS — vector store
