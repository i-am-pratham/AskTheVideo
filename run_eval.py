"""
Runs an eval set automatically against a built index, printing
each question, the expected answer, and the actual answer side by
side. You still make the PASS/FAIL judgment call at the end — but
you no longer type each question in by hand.
"""
import sys
import indexing
import retrieval
import chain as chain_module
from eval_set import EVAL_SET
from eval_set_2 import EVAL_SET_2


def run_eval(video_id: str, eval_items):
    if not indexing.index_exists(video_id):
        raise RuntimeError(
            f"No index found for {video_id}. Run main.py first to build it."
        )

    vector_store = indexing.load_index(video_id)
    retriever = retrieval.get_retriever(vector_store)
    qa_chain = chain_module.build_chain(retriever)

    for i, item in enumerate(eval_items, start=1):
        question = item["question"]
        expected = item["expected_answer_summary"]
        q_type = item["type"]

        actual = qa_chain.invoke(question)

        print(f"\n{'=' * 70}")
        print(f"Q{i} [{q_type}]: {question}")
        print(f"\nExpected: {expected}")
        print(f"\nActual:   {actual}")

    print(f"\n{'=' * 70}")
    print(f"\nRan {len(eval_items)} questions. Review each Actual vs Expected above")
    print("and score PASS/FAIL yourself — this script doesn't auto-grade correctness.")


if __name__ == "__main__":
    video_id = input("Enter the video ID to evaluate: ").strip()
    which = input("Which eval set? (1 = Sinek, 2 = Musk): ").strip()

    eval_items = EVAL_SET_2 if which == "2" else EVAL_SET
    run_eval(video_id, eval_items)