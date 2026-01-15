# Development Session - 2025-01-15 - agent-factory-refactor

## Goals
- [x] Push initial repo to GitHub
- [x] Fix authentication error with Anthropic API
- [x] Debug agent generation (persona mismatch bug)
- [x] Add CLI argument support for problem input
- [x] Implement dynamic registry generation (industry-agnostic)
- [x] Reorganize repository structure
- [x] Add retry logic and better error handling for LLM client
- [x] Make constraints dynamic based on domain
- [ ] Test dynamic constraints across all domains

## Progress

### Session Start - Git Setup
- Initialized git repo and pushed to GitHub
- Fixed `.env` file exposure by adding to `.gitignore`
- Removed `export` prefix from `.env` for python-dotenv compatibility

### API Authentication Fix
- Added `python-dotenv` import to `llm_clients/claude.py`
- Fixed `load_dotenv()` call to properly load API key

### Agent Generation Bug Fix
- Identified persona mismatch: LLM returned "Data Engineer" but registry had "DataEngineer"
- Root cause: System prompt didn't list available personas
- Solution: Updated `prompts/problem_analyzer.system.txt` to include available persona list

### CLI Argument Support
- Added `argparse` to `main.py`
- Supports: `python main.py "problem description"`
- Falls back to interactive input if no argument provided

### Dynamic Registry Generation (Major Feature)
- Created `registry_generator.py` - generates personas based on domain + problem
- Created `prompts/registry_generator.system.txt` - system prompt for persona generation
- Modified `analyzer.py` - dynamically builds prompt from generated registry
- Modified `main.py` - added `--domain` CLI argument
- Usage: `python main.py --domain "gaming" "Build matchmaking system"`

### Repository Reorganization
- Created `core/` directory for Python modules
- Moved: `analyzer.py`, `generator.py`, `registry_generator.py`, `llm_client.py`
- Created `docs/` for documentation
- Moved `architecture.excalidraw` to `docs/`
- Deleted obsolete files: `command.txt`, `llm_clients/`
- Updated all imports to use `core.` prefix

### LLM Client Improvements
- Added `clean_json_response()` for robust JSON extraction
- Implemented retry logic (3 attempts) with delays
- Better error messages showing response preview on failure
- Increased `max_tokens` from 800 to 4000

### Dynamic Constraints
- Updated registry structure to include `domain_constraints`
- Modified `generator.py` to pass constraints to template
- Updated `templates/agent.md.j2` to render dynamic constraints
- Updated `prompts/registry_generator.system.txt` for new JSON structure

## Git Changes Summary
- Modified: `main.py`, `core/analyzer.py`, `core/generator.py`, `core/llm_client.py`
- Added: `core/__init__.py`, `core/registry_generator.py`, `prompts/registry_generator.system.txt`
- Added: `docs/architecture.excalidraw`
- Deleted: `analyzer.py`, `generator.py`, `llm_clients/`, `command.txt`
- Commits: 3 (Initial commit, Reorganize repo, Add retry logic)

## Issues Encountered & Solutions
1. **Issue**: GitHub rejected push due to secret scanning (API key in `.env`)
   **Solution**: Added `.env` to `.gitignore`, removed from git tracking with `git rm --cached`

2. **Issue**: `os.getenv()` not loading `.env` file
   **Solution**: Added `python-dotenv` and `load_dotenv()` call

3. **Issue**: LLM returned personas not in registry (name mismatch)
   **Solution**: Updated system prompt to explicitly list available personas

4. **Issue**: JSON response truncated (max_tokens too low)
   **Solution**: Increased `max_tokens` from 800 to 4000

5. **Issue**: Registry loaded at import time, not runtime
   **Solution**: Moved registry loading inside `generate_agents()` function

6. **Issue**: JSON parsing failures from LLM responses
   **Solution**: Added retry logic and better JSON cleanup regex

## Architecture Overview
```
agent_factory/
├── main.py                 # Entry point with --domain arg
├── core/                   # Core Python modules
│   ├── analyzer.py         # LLM Call 2: Select personas
│   ├── generator.py        # Generate agent .md files
│   ├── registry_generator.py # LLM Call 1: Generate personas
│   └── llm_client.py       # Anthropic API wrapper
├── prompts/                # System prompts
├── templates/              # Jinja2 templates
├── personas/               # Generated registry.yaml
├── agents/                 # Generated agent files
└── docs/                   # Documentation
```

## Session Summary
Transformed a static HFT-specific agent factory into a dynamic, industry-agnostic system. Key achievements:
- Dynamic persona generation based on domain + problem
- Clean repository structure with `core/` module
- Robust LLM client with retry logic
- Domain-specific constraints in generated agents

## Tips for Future Sessions
- Run `python main.py --domain "X" "problem"` to test different industries
- Registry is regenerated fresh each run (clears previous session)
- If JSON parsing fails, check LLM response in error message
- Constraints are now dynamic - defined per domain in registry generation
