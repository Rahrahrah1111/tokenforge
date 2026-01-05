from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    role: str
    content: str


class AdapterError(RuntimeError):
    pass


class BaseAdapter:
    def send(self, messages: List[Message]) -> str:
        raise NotImplementedError
