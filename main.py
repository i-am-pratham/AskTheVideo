"""
AskTheVideo — entry point.
Given a YouTube video ID, indexes it (or loads an existing index),
then lets you ask questions about its content in a loop.
"""
import ingestion
import indexing
import retrieval
import chain as chain_module  # avoid shadowing the local variable name "chain"


def get_or_build_index(video_id: str):
    """
    Loads a saved index if one exists for this video, otherwise
    builds a new one from scratch (fetch transcript -> chunk ->
    embed -> save).
    """
    if indexing.index_exists(video_id):
        print(f"Found existing index for {video_id}, loading from disk...")
        vector_store = indexing.load_index(video_id)
    else:
        print(f"No existing index for {video_id}. Building one now...")
        transcript = ingestion.get_transcript(video_id)
        print(f"Transcript fetched ({len(transcript)} characters)")

        vector_store = indexing.build_index(video_id, transcript)
        saved_path = indexing.save_index(vector_store, video_id)
        print(f"Index saved to {saved_path}")

    return vector_store


def main():
    video_id = input("Enter a YouTube video ID: ").strip()

    vector_store = get_or_build_index(video_id)
    retriever = retrieval.get_retriever(vector_store)
    qa_chain = chain_module.build_chain(retriever)

    print("\nReady! Ask questions about the video (type 'exit' to quit).\n")

    while True:
        question = input("Your question: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue

        answer = qa_chain.invoke(question)
        print(f"\nAnswer: {answer}\n")


if __name__ == "__main__":
    main()