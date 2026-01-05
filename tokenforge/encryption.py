import base64
import os
from dataclasses import dataclass
from typing import Optional

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    Fernet = None


@dataclass
class EncryptionResult:
    encrypted_text: str
    method: str


class MessageEncryptor:
    def __init__(self, key: Optional[str] = None) -> None:
        self._key = key or os.environ.get("TOKENFORGE_ENCRYPTION_KEY")
        self._method = "xor"
        self._fernet = None
        if CRYPTO_AVAILABLE:
            self._method = "fernet"
            if self._key is None:
                self._key = Fernet.generate_key().decode("utf-8")
            self._fernet = Fernet(self._key.encode("utf-8"))

    @property
    def method(self) -> str:
        return self._method

    @property
    def key(self) -> Optional[str]:
        return self._key

    def encrypt(self, plaintext: str) -> EncryptionResult:
        if self._fernet:
            encrypted = self._fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")
            return EncryptionResult(encrypted_text=encrypted, method=self._method)
        return EncryptionResult(encrypted_text=_xor_encrypt(plaintext, self._key), method=self._method)


def _xor_encrypt(plaintext: str, key: Optional[str]) -> str:
    if not key:
        key = "tokenforge-default-key"
    key_bytes = key.encode("utf-8")
    data = plaintext.encode("utf-8")
    encrypted = bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))
    return base64.b64encode(encrypted).decode("utf-8")
