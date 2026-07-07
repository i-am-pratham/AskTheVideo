"""
Builds the RAG chain: retrieval + prompt + LLM + output parsing,
wired together with LangChain's LCEL (the `|` pipe syntax).
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

import config


PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions about a YouTube
video's transcript.
Answer ONLY from the provided transcript context.
If the context is insufficient to answer, say you don't know — do
not make anything up.

Transcript context:
{context}

Question: {question}
"""


def format_docs(retrieved_docs) -> str:
    """Joins retrieved chunk texts into one context string for the prompt."""
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


def get_llm():
    """Returns a configured Gemini chat model instance."""
    return ChatGoogleGenerativeAI(
        model=config.CHAT_MODEL,
        temperature=config.TEMPERATURE,
    )


def build_chain(retriever):
    """
    Wires retriever + prompt + LLM + parser into one runnable chain.
    Call chain.invoke("some question") to get a plain-text answer.
    """
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    llm = get_llm()
    parser = StrOutputParser()

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough(),
    })

    chain = parallel_chain | prompt | llm | parser
    return chain