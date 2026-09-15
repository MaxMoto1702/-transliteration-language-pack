import gzip
import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_dictionary.py"
SPEC = importlib.util.spec_from_file_location("build_dictionary", MODULE_PATH)
build_dictionary = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(build_dictionary)


class TransliterationTest(unittest.TestCase):
    def test_canonical_mapping(self):
        self.assertEqual("privet", build_dictionary.transliterate("привет"))
        self.assertEqual("horosho", build_dictionary.transliterate("хорошо"))
        self.assertEqual("schaste", build_dictionary.transliterate("счастье"))
        self.assertEqual("obyom", build_dictionary.transliterate("объём"))

    def test_strict_alternatives_are_not_generated_by_mapping(self):
        self.assertNotEqual("khorosho", build_dictionary.transliterate("хорошо"))
        self.assertNotEqual("tsar", build_dictionary.transliterate("цар"))
        self.assertNotEqual("shchaste", build_dictionary.transliterate("счастье"))

    def test_source_word_filter(self):
        self.assertTrue(build_dictionary.is_source_word("рок-н-ролл"))
        self.assertFalse(build_dictionary.is_source_word("hello"))
        self.assertFalse(build_dictionary.is_source_word("hello-привет"))
        self.assertFalse(build_dictionary.is_source_word(""))

    def test_generate_words_deduplicates_and_filters(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "words.gz"
            with gzip.open(source, "wt", encoding="utf-8") as output:
                output.write("хорошо\nХОРОШО\nпривет\nhello\n\n")
            self.assertEqual(
                {"horosho", "privet"}, build_dictionary.generate_words(source)
            )


if __name__ == "__main__":
    unittest.main()
