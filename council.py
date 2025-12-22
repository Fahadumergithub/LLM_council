import asyncio
import random
from openrouter import query_model
from config import COUNCIL_MODELS, CHAIRMAN_MODEL, MODEL_NAMES, CHAIRMAN_NAME


async def get_council_responses(question: str):
    messages = [{"role": "user", "content": question}]
    tasks = [query_model(model, messages) for model in COUNCIL_MODELS]
    responses = await asyncio.gather(*tasks)
    council_responses = []
    for i, response in enumerate(responses):
        if response and "content" in response:
            council_responses.append({
                "model": COUNCIL_MODELS[i],
                "name": MODEL_NAMES[COUNCIL_MODELS[i]],
                "response": response["content"]
            })
    return council_responses


async def chairman_rank_responses(question: str, responses: list):
    anonymous_responses = responses.copy()
    random.shuffle(anonymous_responses)
    ranking_prompt = f"""You are the Supreme Judge evaluating responses to this question:

QUESTION: {question}

Below are {len(anonymous_responses)} responses from different AI models (labeled A, B, C, D). Your task is to:
1. Analyze each response carefully
2. Rank them from BEST to WORST
3. Explain your reasoning

RESPONSES:
"""
    for i, resp in enumerate(anonymous_responses):
        label = chr(65 + i)
        ranking_prompt += f"\n--- RESPONSE {label} ---\n{resp['response']}\n"
    
    ranking_prompt += """

Provide your ranking in this EXACT format:
RANKING: [Letter of best], [Letter of 2nd best], [Letter of 3rd best], [Letter of worst]
REASONING: [Your detailed explanation]

Example format:
RANKING: C, A, D, B
REASONING: Response C provided the most comprehensive answer because..."""

    messages = [{"role": "user", "content": ranking_prompt}]
    chairman_response = await query_model(CHAIRMAN_MODEL, messages, timeout=90.0)
    if not chairman_response or "content" not in chairman_response or not chairman_response["content"]:
        return None, anonymous_responses
    return chairman_response["content"], anonymous_responses


def parse_ranking(chairman_output: str, anonymous_responses: list):
    lines = chairman_output.split("\n")
    ranking_line = ""
    reasoning = ""
    for i, line in enumerate(lines):
        if line.startswith("RANKING:"):
            ranking_line = line.replace("RANKING:", "").strip()
        elif line.startswith("REASONING:"):
            reasoning = "\n".join(lines[i:]).replace("REASONING:", "").strip()
            break
    if not ranking_line:
        return None, reasoning
    ranked_letters = [letter.strip() for letter in ranking_line.split(",")]
    ranked_responses = []
    for letter in ranked_letters:
        idx = ord(letter.upper()) - 65
        if 0 <= idx < len(anonymous_responses):
            ranked_responses.append(anonymous_responses[idx])
    return ranked_responses, reasoning
