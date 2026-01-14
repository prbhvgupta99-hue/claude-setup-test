from analyzer import analyze_problem
from generator import generate_agents
from llm_clients.claude import claude_call
import os
import json

# #region agent log
log_path = "/Users/prabhavgupta/Desktop/claude_setup/.cursor/debug.log"
with open(log_path, "a") as log_file:
    log_file.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"main.py:6","message":"Main entry point","data":{"env_keys":list(os.environ.keys()) if "ANTHROPIC_API_KEY" in os.environ else []},"timestamp":int(__import__("time").time()*1000)})+"\n")
# #endregion agent log

if __name__ == "__main__":
    # #region agent log
    with open(log_path, "a") as log_file:
        log_file.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"main.py:11","message":"Before input prompt","data":{"api_key_in_env":"ANTHROPIC_API_KEY" in os.environ},"timestamp":int(__import__("time").time()*1000)})+"\n")
    # #endregion agent log
    problem = input("Describe your problem:\n> ")

    # #region agent log
    with open(log_path, "a") as log_file:
        log_file.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"main.py:16","message":"Before analyze_problem call","data":{},"timestamp":int(__import__("time").time()*1000)})+"\n")
    # #endregion agent log
    analysis = analyze_problem(problem, llm_client=claude_call)

    # Pass both the original problem and analysis
    generate_agents(problem, analysis, output_dir="agents/")

    print("\n✅ Agents generated successfully!")
