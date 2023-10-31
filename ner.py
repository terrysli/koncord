"""Named entity recognizers."""

import spacy

nlp = spacy.load("en_core_web_sm")

def run_ner(doc):
    ner = nlp.get_pipe("ner")
    doc = ner(doc)
