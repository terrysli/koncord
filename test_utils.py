"""Utils tests."""

from unittest import TestCase

from utils import clean, get_lemmas

class UtilsTestCase(TestCase):
    def test_clean(self):
        text = """This  should
        all appear  on
        the
        same
        line."""
        clean_text = clean(text)
        self.assertEqual(clean_text, "This should all appear on the same line.")

    def test_get_lemmas(self):
        strings = ["fly", "flew", "sold", "selling", "was"]
        lemmas = get_lemmas(strings)
        self.assertEqual(lemmas, ["fly", "fly", "sell", "sell", "be"])
