import spacy

from preambles import preambles

nlp = spacy.load("en_core_web_sm")
doc = nlp(preambles[0])

print("ents:", [(ent.text, ent.label_) for ent in doc.ents])