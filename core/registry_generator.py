import yaml
from pathlib import Path

REGISTRY_PATH = Path("personas/registry.yaml")

def generate_registry(domain: str, problem: str, llm_client) -> dict:
    """
    LLM Call 1: Generate 5-7 personas relevant to domain + problem.
    Saves to personas/registry.yaml and returns the registry dict.
    """
    system_prompt = Path("prompts/registry_generator.system.txt").read_text()

    user_prompt = f"""Domain: {domain}
Problem: {problem}

Generate 5-7 expert personas that would be needed to solve this problem in the {domain} industry."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # LLM returns YAML string
    response = llm_client(messages)

    # Response is already parsed as dict from claude_call
    # But we need raw YAML, so we'll modify claude.py or handle it here
    if isinstance(response, dict):
        registry = response
    else:
        registry = yaml.safe_load(response)

    # Save to disk
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False)

    print(f"Generated registry with {len(registry)} personas for '{domain}' domain")
    return registry


def load_registry() -> dict:
    """Load the current registry from disk."""
    with open(REGISTRY_PATH, "r") as f:
        return yaml.safe_load(f)
