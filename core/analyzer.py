from pathlib import Path


def build_persona_list(registry: dict) -> str:
    """Build a formatted list of personas from the registry for the prompt."""
    lines = []
    for name, details in registry.items():
        role = details.get("role_description", "")
        expertise = ", ".join(details.get("expertise_list", [])[:3])
        lines.append(f"- {name}: {role} (Expertise: {expertise})")
    return "\n".join(lines)


def analyze_problem(problem_text: str, registry: dict, llm_client):
    """
    LLM Call 2: Analyze the problem and select relevant personas from the registry.
    Dynamically builds the prompt with available personas.
    """
    # Load base system prompt
    base_prompt = Path("prompts/problem_analyzer.system.txt").read_text()

    # Build persona list from registry
    persona_list = build_persona_list(registry)
    persona_names = list(registry.keys())

    # Inject personas into prompt
    system_prompt = base_prompt.replace("{personas_from_registry}", persona_list)
    system_prompt = system_prompt.replace("{persona_names}", ", ".join(persona_names))

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": problem_text}
    ]

    return llm_client(messages)
