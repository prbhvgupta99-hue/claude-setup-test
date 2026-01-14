from core.registry_generator import generate_registry
from core.analyzer import analyze_problem
from core.generator import generate_agents
from core.llm_client import claude_call
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate agents for a problem")
    parser.add_argument("--domain", "-d", required=True, help="Industry domain (e.g., gaming, healthcare, fintech)")
    parser.add_argument("problem", nargs="?", help="Problem description")
    args = parser.parse_args()

    domain = args.domain
    problem = args.problem if args.problem else input("Describe your problem:\n> ")

    print(f"\n🏭 Agent Factory - {domain.title()} Domain")
    print("=" * 50)

    # Step 1: Generate registry based on domain + problem
    print(f"\n📋 Step 1: Generating personas for '{domain}' domain...")
    registry = generate_registry(domain, problem, llm_client=claude_call)

    # Step 2: Analyze problem and select relevant personas
    print(f"\n🔍 Step 2: Analyzing problem and selecting personas...")
    analysis = analyze_problem(problem, registry, llm_client=claude_call)

    # Step 3: Generate agent files
    print(f"\n📝 Step 3: Generating agent files...")
    generate_agents(problem, analysis, output_dir="agents/")

    print("\n✅ Agents generated successfully!")
