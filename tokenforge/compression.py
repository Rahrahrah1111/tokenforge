import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

PHRASE_DICTIONARY = [
    " the ",
    " and ",
    " you ",
    " that ",
    " with ",
    " for ",
    " are ",
    " your ",
    " have ",
    " this ",
    " not ",
    " from ",
    " will ",
    " can ",
    " what ",
    " about ",
    " would ",
    " should ",
    " please ",
    " thanks ",
    " important ",
    " summary ",
    " instructions ",
    " information ",
    " response ",
    " message ",
    " analyze ",
    " create ",
    " explain ",
    " question ",
    " answer ",
    " context ",
]


@dataclass
class CompressionResult:
    compressed_text: str
    mapping: Dict[str, str]
    original_length: int
    compressed_length: int


def _token_for_index(index: int) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    base = len(alphabet)
    if index < base:
        return f"§{alphabet[index]}"
    return f"§{alphabet[index // base]}{alphabet[index % base]}"


def build_dictionary(level: str) -> List[str]:
    if level == "light":
        return PHRASE_DICTIONARY[:10]
    if level == "aggressive":
        return PHRASE_DICTIONARY + [
            " required ",
            " ensure ",
            " provide ",
            " document ",
            " implement ",
            " feature ",
            " detailed ",
            " settings ",
            " configuration ",
            " description ",
        ]
    return PHRASE_DICTIONARY


def compress_text(text: str, level: str) -> CompressionResult:
    dictionary = build_dictionary(level)
    mapping: Dict[str, str] = {}
    compressed = text
    for index, phrase in enumerate(sorted(dictionary, key=len, reverse=True)):
        token = _token_for_index(index)
        if phrase in compressed:
            compressed = compressed.replace(phrase, token)
            mapping[token] = phrase

    compressed = _compress_whitespace(compressed)
    return CompressionResult(
        compressed_text=compressed,
        mapping=mapping,
        original_length=len(text),
        compressed_length=len(compressed),
    )


def _compress_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def build_decoder_prompt(mapping: Dict[str, str]) -> str:
    if not mapping:
        return "You will receive a compressed message. Respond to it directly."
    pairs = "\n".join(f"{token} => {phrase.strip()}" for token, phrase in mapping.items())
    return (
        "You will receive a compressed message. "
        "Decompress by replacing each token with its phrase before responding.\n"
        "Token map:\n"
        f"{pairs}"
    )
