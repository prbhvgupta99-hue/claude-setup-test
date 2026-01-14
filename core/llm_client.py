import anthropic
import os
import json
import re
import time
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "claude-haiku-4-5-20251001"

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def clean_json_response(text: str) -> str:
    """Clean up LLM response to extract valid JSON."""
    text = text.strip()

    # Remove markdown code fences (various formats)
    text = re.sub(r"^```(?:json|JSON)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)

    # Remove any leading/trailing whitespace again
    text = text.strip()

    # Try to extract JSON if there's extra text around it
    # Look for JSON object or array
    json_match = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', text)
    if json_match:
        text = json_match.group(1)

    return text


def claude_call(messages, max_retries=3):
    """
    Call Claude API with retry logic and robust JSON parsing.

    messages: [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."}
    ]
    """
    system_prompt = messages[0]["content"]
    user_prompt = messages[1]["content"]

    last_error = None
    last_response = None

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=MODEL_ID,
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            text = response.content[0].text
            last_response = text

            # Clean and parse JSON
            cleaned = clean_json_response(text)
            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"⚠️ JSON parse failed (attempt {attempt + 1}/{max_retries}), retrying...")
                time.sleep(1)
            continue

        except anthropic.APIError as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"⚠️ API error (attempt {attempt + 1}/{max_retries}), retrying...")
                time.sleep(2)
            continue

    # All retries failed
    error_msg = f"Failed after {max_retries} attempts.\n"
    error_msg += f"Last error: {last_error}\n"
    if last_response:
        # Show first 500 chars to help debug
        preview = last_response[:500] + "..." if len(last_response) > 500 else last_response
        error_msg += f"Last response preview:\n{preview}"

    raise ValueError(error_msg)
