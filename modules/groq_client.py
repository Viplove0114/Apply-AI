"""
groq_client.py — Wrapper around the Groq API for LLM completions.

Handles client initialization, request dispatch, and error handling.
"""

from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, MODEL_TEMPERATURE, MODEL_MAX_TOKENS


def _get_client() -> Groq:
    """
    Create and return a Groq client instance.
    Raises ValueError if the API key is missing.
    """
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not set. "
            "Please add it to your .env file (see .env.example)."
        )
    return Groq(api_key=GROQ_API_KEY)


def generate_response(prompt: str) -> str:
    """
    Send a prompt to the Groq LLM and return the generated text.

    Args:
        prompt: The fully assembled prompt string.

    Returns:
        The model's completion text.

    Raises:
        RuntimeError: If the API call fails for any reason.
    """
    try:
        client = _get_client()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert career coach and professional writer. "
                        "You craft compelling, human-sounding cover letters and cold emails "
                        "that feel genuine — never robotic or templated."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=MODEL_NAME,
            temperature=MODEL_TEMPERATURE,
            max_tokens=MODEL_MAX_TOKENS,
        )
        return chat_completion.choices[0].message.content

    except ValueError:
        # Re-raise missing key errors as-is
        raise
    except Exception as e:
        raise RuntimeError(
            f"Groq API request failed: {e}\n\n"
            "Please check your API key and internet connection."
        ) from e
