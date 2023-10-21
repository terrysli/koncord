"""Indemnification labelers tests."""

import spacy
from unittest import TestCase

from indemnifications import label_indem

class IndemnificationsTestCase(TestCase):

    def setUp(self):
        self.nlp = spacy.load("en_core_web_sm")

    def test_label_indem(self):
        doc = self.nlp("Seller shall hold Buyer harmless from infringement.")
        results = label_indem(self.nlp, doc)
        self.assertEqual(results[0].text,
                         "Seller shall hold Buyer harmless from infringement.")


