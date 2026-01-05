from dataclasses import dataclass
from typing import Dict


@dataclass
class ForgeStats:
    total_requests: int = 0
    total_input_chars: int = 0
    total_compressed_chars: int = 0
    total_tokens_sent: int = 0
    total_tokens_received: int = 0
    total_tokens_saved: int = 0
    total_pii_redacted: int = 0
    encryption_method: str = "xor"

    def to_dict(self) -> Dict[str, object]:
        compression_ratio = "0%"
        if self.total_input_chars:
            ratio = 1 - (self.total_compressed_chars / self.total_input_chars)
            compression_ratio = f"{ratio:.1%}"
        return {
            "total_requests": self.total_requests,
            "total_input_chars": self.total_input_chars,
            "total_compressed_chars": self.total_compressed_chars,
            "compression_ratio": compression_ratio,
            "total_tokens_sent": self.total_tokens_sent,
            "total_tokens_received": self.total_tokens_received,
            "total_tokens_saved": self.total_tokens_saved,
            "estimated_cost_savings": f"${self.total_tokens_saved * 0.000002:.4f}",
            "total_pii_redacted": self.total_pii_redacted,
            "encryption_method": self.encryption_method,
        }
