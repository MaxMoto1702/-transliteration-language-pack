# Russian transliteration dictionary for IntelliJ IDEA

This repository builds a strict, offline dictionary for IntelliJ IDEA spelling
inspection. It accepts Russian words written with one canonical Latin mapping.
For example, `horosho` is accepted, while `khorosho` is not.

## Install

1. Build the dictionary with `python3 scripts/build_dictionary.py`.
2. In IntelliJ IDEA, open **Settings | Editor | Natural Languages | Spelling**.
3. Click **+** and select `dist/ru-translit.dic`.

The dictionary is a plain UTF-8 `.dic` word list, which IDEA supports as a
custom dictionary. It has no network access and does not replace IDEA's
built-in English or Russian dictionaries.

## Canonical transliteration

| Cyrillic | Latin | Cyrillic | Latin |
| --- | --- | --- | --- |
| ж | `zh` | х | `h` |
| ц | `c` | ч | `ch` |
| ш | `sh` | щ | `sch` |
| ё | `yo` | ю | `yu` |
| я | `ya` | й, ы | `y` |
| э | `e` | ь, ъ | omitted |

All remaining letters use their usual one-letter Latin representation. The
mapping is deliberately strict: variants such as `kh`, `ts`, `shch`, `ju`, and
`ja` are not emitted.

## Build and test

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_dictionary.py
```

The build downloads the pinned, gzip-compressed CSpell word list from
`Goudron/ru-spelling-dictionary` on the first run, verifies its SHA-256 hash,
and saves it under the ignored `source/` directory. The generated distribution
includes provenance and MPL-2.0 licensing notices.

## Source and license

The source word list is release `v1.0.8` of
[Goudron/ru-spelling-dictionary](https://github.com/Goudron/ru-spelling-dictionary),
commit `69a18ae079084f11569f5190ac2080289055ef5e`. It is derived from the
project's Russian Hunspell dictionary and distributed under MPL-2.0 with
additional upstream notices. See `dist/NOTICE.md` and `dist/LICENSE-MPL-2.0.txt`
after building.

