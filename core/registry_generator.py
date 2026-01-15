import yaml
from pathlib import Path

REGISTRY_PATH = Path("personas/registry.yaml")
AGENTS_DIR = Path("agents")


def clear_previous_session():
    """Clear registry and agents from previous session."""
    # Remove old registry
    if REGISTRY_PATH.exists():
        REGISTRY_PATH.unlink()

    # Clear old agent files
    if AGENTS_DIR.exists():
        for agent_file in AGENTS_DIR.glob("*.md"):
            agent_file.unlink()


def generate_registry(domain: str, problem: str, llm_client) -> dict:
    """
    LLM Call 1: Generate domain constraints and 5-7 personas.
    Saves to personas/registry.yaml and returns the full registry dict.
    """
    # Clear previous session data
    clear_previous_session()

    system_prompt = Path("prompts/registry_generator.system.txt").read_text()

    user_prompt = f"""Domain: {domain}
Problem: {problem}

Generate domain-specific constraints and 5-7 expert personas for the {domain} industry."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = llm_client(messages)

    if isinstance(response, dict):
        registry = response
    else:
        registry = yaml.safe_load(response)

    # Save to disk
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False)

    persona_count = len(registry.get("personas", {}))
    print(f"Generated registry with {persona_count} personas for '{domain}' domain")
    return registry


def load_registry() -> dict:
    """Load the current registry from disk."""
    with open(REGISTRY_PATH, "r") as f:
        return yaml.safe_load(f)
