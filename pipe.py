import spacy
from spacy.language import Language

from references.categories import STATES, BIZ_TYPES, INCOTERMS
from data.preambles import preambles
from utils import clean


nlp = spacy.load("en_core_web_sm")

########## EntityRuler ##########

entity_ruler = nlp.add_pipe("entity_ruler", before="ner")

# Patterns for names of US states
state_patterns = [{"label": "JDX",
                   "pattern": [
                       {"LOWER": "state", "OP": "?"},
                       {"LOWER": "of", "OP": "?"},
                       {"LOWER": {"IN": STATES}}
                   ]
                   }]
# TODO: Add other jurisdiction patterns (e.g., venues)
entity_patterns = state_patterns
entity_ruler.add_patterns(entity_patterns)


########## SpanRuler ##########

ruler = nlp.add_pipe("span_ruler", before="ner")

biz_type_patterns = [
    {"label": "BIZ_TYPE", "pattern": type} for type in BIZ_TYPES
]

incoterm_patterns = [
    {"label": "INCOTERM", "pattern": term} for term in INCOTERMS
]

money_pattern = [
    {"label": "MONEY",
     "pattern": [{"IS_CURRENCY": True},
                 {"TEXT": {"REGEX": r"\d{1,3}(,\d{3})*(\.\d{2})?"}}]
     }
]

span_patterns = [
    *biz_type_patterns,
    *incoterm_patterns,
    *money_pattern
]
ruler.add_patterns(span_patterns)

# Insert text to analyze here
text = clean(preambles[0])
doc = nlp(text)

print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
print("Spans:", [(span.text, span.label_) for span in doc.spans["ruler"]])

