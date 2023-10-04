import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span, Token
from spacy.matcher import Matcher, PhraseMatcher

from categories import STATES, BIZ_TYPES, INCOTERMS
from preambles import preambles

nlp = spacy.load("en_core_web_sm")

########## Labelling entities ##########

entity_ruler = nlp.add_pipe("entity_ruler", before="ner")

# Add more patterns for other ents here
jdx_patterns = [{"label": "JDX", "pattern": [{"TEXT": {"IN": STATES}}]}]
entity_patterns = jdx_patterns
entity_ruler.add_patterns(entity_patterns)

doc = nlp(preambles[0])
print([(ent.text, ent.label_) for ent in doc.ents])


########## Labelling spans ##########

ruler = nlp.add_pipe("span_ruler", before="ner")

# Matches ASCII tokens enclosed in quotation marks
defined_term_patterns = [
    {"label": "DEFTERM",
     "pattern": [
         {"ORTH": '“'},
         {"IS_ASCII": True, "OP": "+"},
         {"ORTH": '”'}
     ]},
    {"label": "DEFTERM",
     "pattern": [
         {"ORTH": '"'},
         {"IS_ASCII": True, "OP": "+"},
         {"ORTH": '"'}
     ]},
]

biz_type_patterns = [
    {"label": "BIZ_TYPE", "pattern": [{"TEXT": {"IN": BIZ_TYPES}}]},
]

incoterm_patterns = [
    {"label": "INCOTERM", "pattern": [{"TEXT": {"IN": INCOTERMS}}]},
]

span_patterns = [
    *defined_term_patterns,
    *biz_type_patterns,
    *incoterm_patterns
]
ruler.add_patterns(span_patterns)

doc = nlp(preambles[0])
print([(span.text, span.label_) for span in doc.spans["ruler"]])
