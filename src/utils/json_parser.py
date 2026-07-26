import json

def extract_json(text: str) -> dict:
    if text is None:
        raise ValueError("LLM response is empty.")
    
    text = text.strip()

    # removing markdown code fences if present
    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        return json.loads(text)
    
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by LLM:\n{text}"
        ) from e
    