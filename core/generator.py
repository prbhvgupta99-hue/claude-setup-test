# generator.py
import os
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

# Jinja2 setup
TEMPLATE_DIR = Path("templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("agent.md.j2")

REGISTRY_PATH = Path("personas/registry.yaml")


def load_registry() -> dict:
    """Load the current registry from disk at runtime."""
    with open(REGISTRY_PATH, "r") as f:
        return yaml.safe_load(f)


def generate_agents(problem_text, analysis, output_dir="agents/"):
    """
    Generate markdown files for each persona based on analysis.

    All files go directly into `agents/` folder. No subfolders.
    """
    # Load registry at runtime (after it's been generated)
    personas_registry = load_registry()

    personas = analysis.get("required_personas", [])

    # Create base output folder
    problem_folder = Path(output_dir)
    problem_folder.mkdir(parents=True, exist_ok=True)

    for p in personas:
        persona_name = p.get("persona")
        reason = p.get("reason", "")

        # Look up persona metadata from registry
        persona_info = personas_registry.get(persona_name)
        if not persona_info:
            print(f"⚠️ Warning: persona '{persona_name}' not found in registry. Skipping...")
            continue

        role = persona_info.get("role_description", "")
        expertise = persona_info.get("expertise_list", [])
        goals = persona_info.get("goals", [])
        questions = persona_info.get("typical_questions", [])

        # Render markdown from template
        rendered = template.render(
            persona_name=persona_name,
            role_description=role,
            expertise_list=expertise,
            goals=goals,
            problem_specific_reason=reason,
            typical_questions=questions
        )

        # Save file (remove spaces for filenames)
        output_path = problem_folder / f"{persona_name.replace(' ', '')}.md"
        with open(output_path, "w") as f:
            f.write(rendered)

    print(f"\n✅ Finished generating agents in '{problem_folder}'")
