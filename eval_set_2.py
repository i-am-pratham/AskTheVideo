"""
Eval set #2 for AskTheVideo — Elon Musk, "The future we're building
-- and boring" (TED2017, interview format with Chris Anderson).
Video ID: zIwLWfaAg-8

Chosen deliberately to be more conversational/messier than the
Sinek talk (eval_set.py) — real interview back-and-forth, tangents,
interruptions — to test whether the pipeline holds up on less
structured transcripts.
"""

EVAL_SET_2 = [
    # ---- In-scope: should be answered correctly ----
    {
        "question": "What is the Boring Company project about?",
        "type": "in_scope",
        "expected_answer_summary": (
            "Digging tunnels under LA to create a 3D network of tunnels "
            "to alleviate traffic congestion, using car-carrying 'skates' "
            "lowered by elevator into the tunnels."
        ),
    },
    {
        "question": "How fast are the tunnel car-skates designed to go?",
        "type": "in_scope",
        "expected_answer_summary": (
            "About 200 km/h (roughly 130 mph), with no speed limit inside "
            "the tunnel."
        ),
    },
    {
        "question": "What example trip time does Musk give for the tunnels?",
        "type": "in_scope",
        "expected_answer_summary": "Getting from Westwood to LAX in about 5-6 minutes.",
    },
    {
        "question": "What did Musk say about a fully self-driving cross-country trip?",
        "type": "in_scope",
        "expected_answer_summary": (
            "He said Tesla should be able to go from a parking lot in "
            "California to a parking lot in New York with no controls "
            "touched, targeting around November or December of that year."
        ),
    },
    {
        "question": "What new Tesla vehicle does Musk reveal or mention?",
        "type": "in_scope",
        "expected_answer_summary": (
            "The Model 3 (coming soon at the time) and the Tesla Semi — "
            "an electric heavy-duty truck claimed to out-torque any diesel semi."
        ),
    },
    {
        "question": "Why does Tesla need Gigafactories, according to the talk?",
        "type": "in_scope",
        "expected_answer_summary": (
            "To own the core competency of lithium-ion battery production "
            "(key to the economics of Tesla's cars, Semi, and houses) by "
            "building the world's largest manufacturing plant, aiming to "
            "double the world's supply of lithium-ion batteries."
        ),
    },
    {
        "question": "What does Musk say about SpaceX and reusable rockets?",
        "type": "in_scope",
        "expected_answer_summary": (
            "References the Falcon 9's successful reflights, saying "
            "reusability only matters if it's rapid and complete, "
            "comparing it to how aircraft aren't rebuilt between flights."
        ),
    },
    {
        "question": "How does Musk describe the scale of the Mars rocket?",
        "type": "in_scope",
        "expected_answer_summary": (
            "About the size of a 40-story building, with roughly 4 times "
            "the thrust of a Saturn V, or the equivalent of about 120 "
            "747s with all engines blazing."
        ),
    },
    {
        "question": "What is Musk's opinion on flying cars as a solution to traffic?",
        "type": "in_scope",
        "expected_answer_summary": (
            "He's not opposed to flying vehicles in general (he builds "
            "rockets), but is concerned flying cars would be noisy, "
            "unsettling, and risky if something overhead malfunctions."
        ),
    },
    {
        "question": "What does Musk say motivates him about the future, near the end of the talk?",
        "type": "in_scope",
        "expected_answer_summary": (
            "That he values beauty and inspiration, isn't trying to be "
            "anyone's savior, and wants a future that's inspiring enough "
            "to give people a reason to want to live — tied to his "
            "multi-planetary species goal."
        ),
    },

    # ---- Out-of-scope: should trigger an honest "I don't know" ----
    {
        "question": "Does this interview mention LangChain or vector databases?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not mentioned.",
    },
    {
        "question": "Does Musk discuss his childhood in South Africa in this talk?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not mentioned.",
    },
    {
        "question": "What does Musk say about cryptocurrency in this interview?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not mentioned.",
    },
    {
        "question": "Does this video cover Twitter or X ownership?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not mentioned (this predates that entirely).",
    },
    {
        "question": "What diet or exercise routine does Musk recommend?",
        "type": "out_of_scope",
        "expected_answer_summary": "Should say it doesn't know / not mentioned.",
    },
]


if __name__ == "__main__":
    for i, item in enumerate(EVAL_SET_2, start=1):
        print(f"{i}. [{item['type']}] {item['question']}")