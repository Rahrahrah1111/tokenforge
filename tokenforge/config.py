from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CompressionLevel(str, Enum):
    LIGHT = "light"
    STANDARD = "standard"
    AGGRESSIVE = "aggressive"


@dataclass
class ForgeConfig:
    compression_level: CompressionLevel = CompressionLevel.STANDARD
    auto_compress: bool = True
    enable_privacy: bool = True
    include_decoder_prompt: bool = True
    enable_encryption: bool = True
    encryption_key: Optional[str] = None
