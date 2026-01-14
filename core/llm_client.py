import anthropic
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Pick a model that exists on your account
MODEL_ID = "claude-haiku-4-5-20251001"  # Replace with one you got from list_models.py

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")  # Make sure env variable is set
)

def claude_call(messages):
    """
    messages: [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."}
    ]
    """

    system_prompt = messages[0]["content"]
    user_prompt = messages[1]["content"]

    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=4000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    text = response.content[0].text

    # Clean up possible Markdown / code fences
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"Claude returned invalid JSON:\n{text}")
