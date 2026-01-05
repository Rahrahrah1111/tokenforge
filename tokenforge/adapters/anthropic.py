from typing import List, Optional
import requests

from .base import BaseAdapter, Message, AdapterError


class AnthropicAdapter(BaseAdapter):
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def send(self, messages: List[Message]) -> str:
        if not self.api_key:
            raise AdapterError("Anthropic API key is required.")
        system_prompt = None
        user_messages = []
        for msg in messages:
            if msg.role == "system" and system_prompt is None:
                system_prompt = msg.content
            else:
                user_messages.append({"role": msg.role, "content": msg.content})
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": user_messages,
        }
        if system_prompt:
            payload["system"] = system_prompt
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            json=payload,
            headers=headers,
            timeout=60,
        )
        if response.status_code >= 400:
            raise AdapterError(f"Request failed ({response.status_code}): {response.text}")
        data = response.json()
        try:
            return data["content"][0]["text"]
        except (KeyError, IndexError) as exc:
            raise AdapterError(f"Unexpected response: {data}") from exc
