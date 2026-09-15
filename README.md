# Russian transliteration dictionary for IntelliJ IDEA

This repository builds a strict, offline dictionary for IntelliJ IDEA spelling
inspection. It accepts Russian words written with one canonical Latin mapping.
For example, `horosho` is accepted, while `khorosho` is not.

## Настройка в IntelliJ IDEA

1. Склонируйте репозиторий или скачайте файл
   `dist/ru-translit.dic`. Чтобы создать его из исходников, выполните
   `python3 scripts/build_dictionary.py` в корне проекта.
2. Откройте настройки IDEA: **File | Settings** на Windows/Linux или
   **IntelliJ IDEA | Settings** на macOS.
3. Перейдите в **Editor | Natural Languages | Spelling**.
4. В секции **Custom Dictionaries** нажмите **+** (или `Alt+Insert`) и
   выберите файл `ru-translit.dic`.
5. Нажмите **Apply**, затем **OK**. Если проверка орфографии была отключена,
   включите inspection **Spelling** через **Editor | Inspections**.

После установки откройте комментарий, строку или Markdown-файл: `horosho` и
`privet` не будут подсвечены как ошибки, а `khorosho` останется опечаткой.
Чтобы убрать словарь, вернитесь в **Custom Dictionaries**, выберите
`ru-translit.dic` и нажмите **-** (или `Alt+Delete`).

Это простой UTF-8 `.dic`, поддерживаемый IDEA как custom dictionary. Он
работает локально, не отправляет текст в сеть и не заменяет встроенные
английский или русский словари.

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
