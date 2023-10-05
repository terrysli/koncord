import spacy

from preambles import preambles

nlp = spacy.load("en_core_web_sm")
doc = nlp('This is a "test to separate" tokens from their quotes.')

print ([(token.i, token.text) for token in doc])