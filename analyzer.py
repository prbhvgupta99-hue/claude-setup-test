from pathlib import Path

def analyze_problem(problem_text, llm_client):
    # Load your system prompt
    system_prompt = Path("prompts/problem_analyzer.system.txt").read_text()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": problem_text}
    ]

    return llm_client(messages)
