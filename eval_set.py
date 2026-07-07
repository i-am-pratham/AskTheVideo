"""
Eval set for AskTheVideo — Simon Sinek, "How Great Leaders Inspire Action"
(TEDxPugetSound, 2009). Video ID: u4ZoJKF_VuA

Each entry has a question, the expected type of answer, and notes on
what to check for when grading manually. "in_scope" questions should
be answered correctly from the transcript. "out_of_scope" (trick)
questions should be met with an honest "I don't know" — NOT a
hallucinated or unrelated answer.

Run main.py with video_id = "u4ZoJKF_VuA" first to build its index,
then manually ask each question below and score PASS/FAIL against
the expected_answer_summary.
"""

EVAL_SET = [
    # ---- In-scope: should be answered correctly ----
    {
        "question": "What is the Golden Circle?",
        "type": "in_scope",
        "expected_answer_summary": (
            "A model with three concentric parts — Why (core belief/purpose), "
            "How (the process), and What (the product/service) — describing "
            "how inspiring leaders and organizations communicate, starting "
            "from Why rather than What."
        ),
    },
    {
        "question": "What company does Sinek use as his main example?",
        "type": "in_scope",
        "expected_answer_summary": "Apple.",
    },
    {
        "question": "According to the talk, what makes Apple different from its competitors?",
        "type": "in_scope",
        "expected_answer_summary": (
            "Apple communicates starting with WHY (their belief in challenging "
            "the status quo and thinking differently) before WHAT they make, "
            "unlike typical companies that lead with What."
        ),
    },
    {
        "question": "Who does Sinek compare to Samuel Pierpont Langley?",
        "type": "in_scope",
        "expected_answer_summary": "The Wright Brothers.",
    },
    {
        "question": "Why did the Wright Brothers succeed where Langley failed, according to the talk?",
        "type": "in_scope",
        "expected_answer_summary": (
            "The Wright Brothers were driven by a cause/belief (to change the "
            "course of the world), had a dedicated team, and did it with "
            "meager resources, whereas Langley pursued it mainly for fame and "
            "fortune, and had more funding but no real team buy-in."
        ),
    },
    {
        "question": "What historical speech does Sinek reference?",
        "type": "in_scope",
        "expected_answer_summary": "Martin Luther King Jr.'s 'I Have a Dream' speech.",
    },
    {
        "question": "How many people showed up to hear MLK speak, and why does that matter to Sinek's argument?",
        "type": "in_scope",
        "expected_answer_summary": (
            "About 250,000 people showed up, not because of an invitation, "
            "but because they believed what MLK believed — used to argue "
            "people follow leaders/causes they believe in, not just being told to."
        ),
    },
    {
        "question": "What is the law of diffusion of innovation?",
        "type": "in_scope",
        "expected_answer_summary": (
            "A concept describing how new ideas spread through a population "
            "in categories: innovators, early adopters, early majority, late "
            "majority, and laggards — with roughly 15-18% adoption (innovators "
            "+ early adopters) as the tipping point to mass-market success."
        ),
    },
    {
        "question": "What example does Sinek give of a product that failed despite being good?",
        "type": "in_scope",
        "expected_answer_summary": (
            "TiVo — described as a great, well-funded product that failed "
            "commercially because it was marketed with What/How instead of Why."
        ),
    },
    {
        "question": "Does Sinek say people buy products for rational reasons?",
        "type": "in_scope",
        "expected_answer_summary": (
            "No — he argues people don't buy WHAT you do, they buy WHY you do "
            "it, tying this to the limbic brain governing decision-making and "
            "behavior rather than purely rational, language-based reasoning."
        ),
    },

    # ---- Out-of-scope: should trigger an honest "I don't know" ----
    {
        "question": "Does this talk mention LangChain or RAG systems?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not mentioned.",
    },
    {
        "question": "Does the speaker discuss climate change policy?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not mentioned.",
    },
    {
        "question": "What programming languages does Sinek recommend learning?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not applicable — not a coding talk.",
    },
    {
        "question": "Does this video give a recipe for chocolate cake?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not mentioned.",
    },
    {
        "question": "What is Sinek's opinion on cryptocurrency?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not mentioned.",
    },
]


if __name__ == "__main__":
    for i, item in enumerate(EVAL_SET, start=1):
        print(f"{i}. [{item['type']}] {item['question']}")