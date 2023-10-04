import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span, Token
from spacy.matcher import Matcher, PhraseMatcher

from categories import STATES, BIZ_TYPES, INCOTERMS
from preambles import preambles

nlp = spacy.load("en_core_web_sm")

jdx_ruler = nlp.add_pipe("entity_ruler", before="ner")
state_matcher = PhraseMatcher(nlp.vocab)
state_patterns = [{
    "label": "JDX",
    "pattern": [{"TEXT": {"IN": STATES}}]
}]
jdx_ruler.add_patterns(state_patterns)

doc = nlp(preambles[0])
print([(ent.text, ent.label_) for ent in doc.ents])

