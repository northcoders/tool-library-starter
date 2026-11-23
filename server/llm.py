"""A small, provider-agnostic wrapper around an LLM API.

Every task this week talks to the model through this module rather than a
specific vendor SDK, so the mechanics (streaming, system prompts,
structured output, embeddings) are the same regardless of which provider
is behind it. Swap providers by changing the LLM_* environment variables:
nothing in this module, or in any code that calls it, needs to change.

Written against a generic OpenAI-compatible chat completions and
embeddings REST shape, which a wide range of providers and gateways
support.
"""

import json
import os
import threading
from collections.abc import AsyncIterator
from pathlib import Path

import httpx


class LLMAPIError(Exception):
    """The provider answered, but with an error status (or an error inside a stream).

    The message always starts "LLM API error <status>: " followed by the
    provider's own response body.
    """


# Read the LLM_* settings when a call is made, not when this module is
# first imported, so it doesn't matter whether load_dotenv() ran before or
# after the import.
def _config() -> dict[str, str | None]:
    return {
        "base_url": os.getenv("LLM_API_BASE"),
        "api_key": os.getenv("LLM_API_KEY"),
        "model": os.getenv("LLM_MODEL"),
        "embed_model": os.getenv("LLM_EMBED_MODEL"),
    }


def _headers(api_key: str | None) -> dict[str, str]:
    return {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}


# An empty system prompt is left out entirely: some providers reject an
# empty system message.
def _with_system(system: str, messages: list[dict]) -> list[dict]:
    return [{"role": "system", "content": system}, *messages] if system else messages


async def send_message(
    *,
    system: str = "",
    messages: list[dict],
    temperature: float = 0.7,
    top_p: float = 1,
    max_tokens: int = 500,
    tools: list[dict] | None = None,
) -> dict:
    """Returns the model's reply message: {"role", "content", "tool_calls"?}."""
    config = _config()
    body = {
        "model": config["model"],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "messages": _with_system(system, messages),
    }
    if tools is not None:
        body["tools"] = tools

    try:
        # timeout=None: this module sets no time limit of its own.
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                f"{config['base_url']}/chat/completions",
                headers=_headers(config["api_key"]),
                json=body,
            )
    except httpx.TransportError as err:
        raise ConnectionError(f"Could not reach the LLM provider: {err}") from err

    if response.is_error:
        raise LLMAPIError(f"LLM API error {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]


_DONE = object()


# Turns one line of the provider's stream into text (or None). Returns
# _DONE at the end-of-stream marker.
def _parse_line(line: str):
    trimmed = line.strip()
    if not trimmed.startswith("data:"):
        return None
    payload = trimmed[5:].strip()
    if payload == "[DONE]":
        return _DONE

    try:
        chunk = json.loads(payload)
    except json.JSONDecodeError:
        return None  # skip a line we can't read rather than crash mid-answer
    if chunk.get("error"):
        # Some providers report a failure inside the stream instead of with a status code.
        raise LLMAPIError(f"LLM API error (in stream): {json.dumps(chunk['error'])}")
    choices = chunk.get("choices") or [{}]
    return (choices[0].get("delta") or {}).get("content") or None


async def stream_message(
    *,
    system: str = "",
    messages: list[dict],
    temperature: float = 0.7,
    top_p: float = 1,
    max_tokens: int = 500,
) -> AsyncIterator[str]:
    """Yields the reply a piece at a time.

    Stopping early (breaking out of the loop, the generator being closed, or
    the task being cancelled because the client went away) closes the
    connection, so the provider stops generating too.
    """
    config = _config()
    body = {
        "model": config["model"],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "stream": True,
        "messages": _with_system(system, messages),
    }

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{config['base_url']}/chat/completions",
                headers=_headers(config["api_key"]),
                json=body,
            ) as response:
                if response.is_error:
                    error_body = (await response.aread()).decode(errors="replace")
                    raise LLMAPIError(f"LLM API error {response.status_code}: {error_body}")

                async for line in response.aiter_lines():
                    token = _parse_line(line)
                    if token is _DONE:
                        return
                    if token:
                        yield token
    except httpx.TransportError as err:
        raise ConnectionError(f"Could not reach the LLM provider: {err}") from err


# Embeddings: by default these run locally, on your own machine, using a
# small open model (all-MiniLM-L6-v2, 384 dimensions) via fastembed. That
# means no API key and no cost for Day 3, and it works the same no matter
# which chat provider you use (not every chat provider offers an embeddings
# endpoint). The model is downloaded once (~90MB) the first time embed()
# runs, then cached in ~/.cache/fastembed.
#
# Set EMBED_PROVIDER=api to call an OpenAI-compatible /embeddings endpoint
# instead (uses LLM_API_BASE, LLM_API_KEY and LLM_EMBED_MODEL).
LOCAL_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LOCAL_EMBED_CACHE = Path.home() / ".cache" / "fastembed"

# Loaded once, on first use. The lock means two requests arriving at the
# same moment share one load rather than loading the model twice.
_local_model = None
_local_model_lock = threading.Lock()


def _embed_locally(text: str) -> list[float]:
    global _local_model
    with _local_model_lock:
        if _local_model is None:
            from fastembed import TextEmbedding

            _local_model = TextEmbedding(LOCAL_EMBED_MODEL, cache_dir=str(LOCAL_EMBED_CACHE))
    vector = next(iter(_local_model.embed([text])))
    # A plain list of Python floats, not a numpy array.
    return vector.tolist()


def _embed_via_api(text: str) -> list[float]:
    config = _config()
    try:
        response = httpx.post(
            f"{config['base_url']}/embeddings",
            headers=_headers(config["api_key"]),
            json={"model": config["embed_model"], "input": text},
            timeout=None,
        )
    except httpx.TransportError as err:
        raise ConnectionError(f"Could not reach the LLM provider: {err}") from err

    if response.is_error:
        raise LLMAPIError(f"LLM API error {response.status_code}: {response.text}")

    return response.json()["data"][0]["embedding"]


def embed(text: str) -> list[float]:
    """Returns a list of numbers (a vector) representing the meaning of `text`."""
    provider = os.getenv("EMBED_PROVIDER") or "local"
    return _embed_via_api(text) if provider == "api" else _embed_locally(text)
