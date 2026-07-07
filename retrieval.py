"""
Builds a retriever from a FAISS vector store.
Kept separate so retrieval strategy (k, search type, filters,
re-ranking, etc.) can evolve independently of how the index
was built or how the LLM chain is wired together.
"""
import config



def get_retriever(vector_store):
    """
    Returns a retriever configured to fetch the top-k most
    similar chunks for a given question.
    """
    retriever= vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": config.RETRIEVER_K},
    )
    return retriever

