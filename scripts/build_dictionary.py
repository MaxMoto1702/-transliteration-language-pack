#!/usr/bin/env python3
"""Build the strict Russian-to-Latin custom dictionary for IntelliJ IDEA."""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source"
DIST_DIR = ROOT / "dist"

UPSTREAM_VERSION = "v1.0.8"
UPSTREAM_COMMIT = "69a18ae079084f11569f5190ac2080289055ef5e"
WORDLIST_URL = (
    "https://raw.githubusercontent.com/Goudron/ru-spelling-dictionary/"
    f"{UPSTREAM_COMMIT}/cspell/dictionaries/ru_RU.txt.gz"
)
LICENSE_URL = (
    "https://raw.githubusercontent.com/Goudron/ru-spelling-dictionary/"
    f"{UPSTREAM_COMMIT}/LICENSE"
)
WORDLIST_SHA256 = "3519d33eb85dc5d3821b9d1af7b33ef723579e72f4633d495d41762a4b7dd2b7"
WORDLIST_PATH = SOURCE_DIR / "ru_RU.txt.gz"
LICENSE_PATH = SOURCE_DIR / "upstream-LICENSE.txt"

LETTER_MAPPING = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e",
    "ё": "yo", "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k",
    "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "c",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "",
    "э": "e", "ю": "yu", "я": "ya",
}
TRANSLITERATION = str.maketrans(LETTER_MAPPING)
CYRILLIC_LETTERS = frozenset(LETTER_MAPPING)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)


def ensure_source() -> None:
    if not WORDLIST_PATH.exists():
        print(f"Downloading {WORDLIST_URL}", file=sys.stderr)
        download(WORDLIST_URL, WORDLIST_PATH)
    actual_hash = sha256(WORDLIST_PATH)
    if actual_hash != WORDLIST_SHA256:
        raise ValueError(
            f"Unexpected SHA-256 for {WORDLIST_PATH}: {actual_hash}; "
            f"expected {WORDLIST_SHA256}"
        )
    if not LICENSE_PATH.exists():
        print(f"Downloading {LICENSE_URL}", file=sys.stderr)
        download(LICENSE_URL, LICENSE_PATH)


def transliterate(word: str) -> str:
    """Return the only allowed compact Latin spelling for a Russian word."""
    return word.lower().translate(TRANSLITERATION)


def is_source_word(word: str) -> bool:
    """Keep Cyrillic words and punctuation IDEA can tokenize within a word."""
    return bool(word) and any(char in CYRILLIC_LETTERS for char in word) and all(
        char in CYRILLIC_LETTERS or char in "-'" for char in word
    )


def generate_words(wordlist_path: Path) -> set[str]:
    words: set[str] = set()
    with gzip.open(wordlist_path, mode="rt", encoding="utf-8") as source:
        for raw_word in source:
            word = raw_word.strip().lower()
            if is_source_word(word):
                latin = transliterate(word)
                if latin and any("a" <= char <= "z" for char in latin):
                    words.add(latin)
    return words


def write_distribution(words: set[str]) -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    dictionary_path = DIST_DIR / "ru-translit.dic"
    dictionary_path.write_text("\n".join(sorted(words)) + "\n", encoding="utf-8")
    shutil.copyfile(LICENSE_PATH, DIST_DIR / "LICENSE-MPL-2.0.txt")
    (DIST_DIR / "NOTICE.md").write_text(
        "# Notices\n\n"
        "`ru-translit.dic` is a modified derivative of the Russian word list from "
        "Goudron/ru-spelling-dictionary, release v1.0.8. The source is available "
        "at https://github.com/Goudron/ru-spelling-dictionary and is licensed "
        "under MPL-2.0; see LICENSE-MPL-2.0.txt. The original upstream BSD-style "
        "and LibreOffice-family notices are retained in that file.\n",
        encoding="utf-8",
    )
    (DIST_DIR / "provenance.json").write_text(
        json.dumps(
            {
                "format": "plain UTF-8 IntelliJ custom dictionary",
                "upstream_repository": "https://github.com/Goudron/ru-spelling-dictionary",
                "upstream_version": UPSTREAM_VERSION,
                "upstream_commit": UPSTREAM_COMMIT,
                "source_wordlist_url": WORDLIST_URL,
                "source_wordlist_sha256": WORDLIST_SHA256,
                "generated_word_count": len(words),
                "mapping": {
                    "zh": "ж", "h": "х", "c": "ц", "ch": "ч", "sh": "ш",
                    "sch": "щ", "yu": "ю", "ya": "я", "yo": "ё",
                    "y": "й, ы", "e": "э", "omitted": "ь, ъ",
                },
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    ensure_source()
    words = generate_words(WORDLIST_PATH)
    write_distribution(words)
    print(f"Generated {len(words):,} words in {DIST_DIR / 'ru-translit.dic'}")


if __name__ == "__main__":
    main()
