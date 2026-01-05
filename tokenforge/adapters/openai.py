from typing import List

from .base import BaseAdapter, Message, AdapterError
import requests


class OpenAIAdapter(BaseAdapter):
    def __init__(self, api_key: str, model: str, base_url: str = "https://api.openai.com/v1") -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")

    def send(self, messages: List[Message]) -> str:
        if not self.api_key:
            raise AdapterError("OpenAI API key is required.")
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code >= 400:
            raise AdapterError(f"Request failed ({response.status_code}): {response.text}")
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise AdapterError(f"Unexpected response: {data}") from exc
