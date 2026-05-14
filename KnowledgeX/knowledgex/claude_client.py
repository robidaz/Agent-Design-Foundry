"""Anthropic SDK wrapper with prompt caching on the stable system prefix.

The Anthropic SDK supports prompt caching via `system` blocks marked with
`cache_control={"type": "ephemeral"}`. The cached prefix must be ≥1024 tokens
for Sonnet to qualify; prompts in knowledgex.prompts are sized accordingly.

Structured output is enforced via tool-use: the caller passes a tool schema
and we force `tool_choice` to that tool.
"""

from __future__ import annotations

import json
import time
from typing import Any

import anthropic

from knowledgex.config import load_config, load_env

_MAX_TOKENS = 1024
_MAX_RETRIES = 2


def _client() -> anthropic.Anthropic:
    env = load_env()
    if not env.anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set; check .env")
    return anthropic.Anthropic(api_key=env.anthropic_api_key)


def call(
    *,
    system_prefix: str,
    user_text: str,
    tool: dict[str, Any],
    max_tokens: int = _MAX_TOKENS,
) -> dict[str, Any]:
    """Single Claude call with cached system prefix and forced tool use.

    Returns the parsed tool-input dict.
    """
    cfg = load_config()
    client = _client()

    system_blocks = [
        {
            "type": "text",
            "text": system_prefix,
            "cache_control": {"type": "ephemeral"},
        }
    ]
    messages = [{"role": "user", "content": user_text}]

    for attempt in range(_MAX_RETRIES + 1):
        try:
            resp = client.messages.create(
                model=cfg.models.claude_model,
                max_tokens=max_tokens,
                system=system_blocks,
                messages=messages,
                tools=[tool],
                tool_choice={"type": "tool", "name": tool["name"]},
            )
            for block in resp.content:
                if block.type == "tool_use" and block.name == tool["name"]:
                    return dict(block.input)
            raise RuntimeError(
                f"Claude did not invoke tool {tool['name']}; raw response: {resp.content!r}"
            )
        except (anthropic.APIError, anthropic.APIStatusError) as exc:
            if attempt == _MAX_RETRIES:
                raise
            time.sleep(1.5 * (attempt + 1))
            _ = exc  # silence unused
    raise RuntimeError("unreachable")


def call_json(*, system_prefix: str, user_text: str, schema_name: str, schema: dict[str, Any]) -> dict[str, Any]:
    """Convenience wrapper that builds the tool spec from a JSON schema."""
    tool = {
        "name": schema_name,
        "description": f"Return the structured {schema_name} output.",
        "input_schema": schema,
    }
    raw = call(system_prefix=system_prefix, user_text=user_text, tool=tool)
    # Validate that the SDK gave us a dict (not a string); the tool framework
    # normally does this, but guard anyway.
    if isinstance(raw, str):
        return json.loads(raw)
    return raw
