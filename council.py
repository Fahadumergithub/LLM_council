import asyncio
import random
from openrouter import query_model
from config import COUNCIL_MODELS, CHAIRMAN_MODEL, MODEL_NAMES, CHAIRMAN_NAME


async def get_council_responses(question: str):
    """
    Step 1: Get responses from all council members in parallel
    """
    messages = [{"role": "user", "content": question}]
    
    tasks = [
        query_model(model, messages) 
        for model in COUNCIL_MODELS
    ]
    
    responses = await asyncio.gather(*tasks)
    
    # Pair responses with model info
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
    """
    Step 2: Chairman ranks all responses anonymously
    """
    
    # Shuffle responses to make them anonymous
    anonymous_responses = responses.copy()
    random.shuffle(anonymous_responses)
    
    # Create ranking prompt for chairman
    ranking_prompt = f"""You are the Supreme Judge evaluating responses to this question:

QUESTION: {question}

Below are {len(anonymous_responses)} responses from different AI models (labeled A, B, C, D). Your task is to:
1. Analyze each response carefully
2. Rank them from BEST to WORST
3. Explain your reasoning

RESPONSES:
"""
    
    for i, resp in enumerate(anonymous_responses):
        label = chr(65 + i)  # A, B, C, D
        ranking_prompt += f"\n--- RESPONSE {label} ---\n{resp['response']}\n"
    
    ranking_prompt += f"""

Provide your ranking in this EXACT format:
RANKING: [Letter of best], [Letter of 2nd best], [Letter of 3rd best], [Letter of worst]
REASONING: [Your detailed explanation]

Example format:
RANKING: C, A, D, B
REASONING: Response C provided the most comprehensive answer because..."""

    messages = [{"role": "user", "content": ranking_prompt}]
    chairman_response = await query_model(CHAIRMAN_MODEL, messages, timeout=90.0)
    
    if not chairman_response or "content" in chairman_response and not chairman_response["content"]:
        return None, anonymous_responses
    
    return chairman_response["content"], anonymous_responses


def parse_ranking(chairman_output: str, anonymous_responses: list):
    """
    Step 3: Parse chairman's ranking and map back to original models
    """
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
    
    # Extract letters (A, B, C, D)
    ranked_letters = [letter.strip() for letter in ranking_line.split(",")]
    
    # Map letters back to models
    ranked_responses = []
    for letter in ranked_letters:
        idx = ord(letter.upper()) - 65  # A=0, B=1, C=2, D=3
        if 0 <= idx < len(anonymous_responses):
            ranked_responses.append(anonymous_responses[idx])
    
    return ranked_responses, reasoning
