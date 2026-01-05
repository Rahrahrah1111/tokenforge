from typing import List, Optional

from .adapters.base import BaseAdapter, Message
from .compression import compress_text, build_decoder_prompt
from .config import ForgeConfig
from .encryption import MessageEncryptor
from .privacy import redact_pii
from .stats import ForgeStats


class TokenForge:
    def __init__(self, adapter: BaseAdapter, config: Optional[ForgeConfig] = None) -> None:
        self.adapter = adapter
        self.config = config or ForgeConfig()
        self.stats = ForgeStats()
        self._encryptor = MessageEncryptor(self.config.encryption_key)
        self.stats.encryption_method = self._encryptor.method
        self._decoder_prompt_sent = False

    def new_session(self) -> None:
        self._decoder_prompt_sent = False

    def chat(self, message: str) -> str:
        processed = message
        redactions = 0
        if self.config.enable_privacy:
            privacy_result = redact_pii(processed)
            processed = privacy_result.text
            redactions = privacy_result.redactions

        if self.config.auto_compress:
            compression = compress_text(processed, self.config.compression_level.value)
            compressed_message = compression.compressed_text
            mapping = compression.mapping
        else:
            compression = None
            compressed_message = processed
            mapping = {}

        messages: List[Message] = []
        if self.config.include_decoder_prompt and (not self._decoder_prompt_sent):
            decoder_prompt = build_decoder_prompt(mapping)
            messages.append(Message(role="system", content=decoder_prompt))
            self._decoder_prompt_sent = True

        messages.append(Message(role="user", content=compressed_message))
        response = self.adapter.send(messages)

        self._update_stats(message, compressed_message, response, redactions)
        if self.config.enable_encryption:
            self._encryptor.encrypt(compressed_message)

        return response

    def _update_stats(self, original: str, compressed: str, response: str, redactions: int) -> None:
        self.stats.total_requests += 1
        self.stats.total_input_chars += len(original)
        self.stats.total_compressed_chars += len(compressed)
        self.stats.total_tokens_sent += _estimate_tokens(compressed)
        self.stats.total_tokens_received += _estimate_tokens(response)
        saved = _estimate_tokens(original) - _estimate_tokens(compressed)
        self.stats.total_tokens_saved += max(saved, 0)
        self.stats.total_pii_redacted += redactions


def _estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)
