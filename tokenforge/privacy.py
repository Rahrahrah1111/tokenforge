import re
from dataclasses import dataclass
from typing import Tuple

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b")


@dataclass
class PrivacyResult:
    text: str
    redactions: int


def redact_pii(text: str) -> PrivacyResult:
    redactions = 0

    def _replace(pattern: re.Pattern, label: str, target: str) -> Tuple[str, int]:
        matches = list(pattern.finditer(target))
        if not matches:
            return target, 0
        return pattern.sub(label, target), len(matches)

    text, count = _replace(EMAIL_PATTERN, "[email redacted]", text)
    redactions += count
    text, count = _replace(PHONE_PATTERN, "[phone redacted]", text)
    redactions += count
    return PrivacyResult(text=text, redactions=redactions)
