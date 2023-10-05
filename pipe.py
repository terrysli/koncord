import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span, Token
from spacy.matcher import Matcher, PhraseMatcher
import re

from categories import STATES, BIZ_TYPES, INCOTERMS
from preambles import preambles


nlp = spacy.load("en_core_web_sm")

########## Labelling entities ##########

entity_ruler = nlp.add_pipe("entity_ruler", before="ner")

# Add more patterns for other ents here
state_patterns = [{"label": "JDX",
                 "pattern": [
                     {"LOWER": "state", "OP": "?"},
                     {"LOWER": "of", "OP": "?"},
                     {"TEXT": {"IN": STATES}}
                 ]
                 }]
entity_patterns = state_patterns
entity_ruler.add_patterns(entity_patterns)


########## Labelling spans ##########

ruler = nlp.add_pipe("span_ruler", before="ner")

biz_type_patterns = [
    {"label": "BIZ_TYPE", "pattern": type} for type in BIZ_TYPES
]

incoterm_patterns = [
    {"label": "INCOTERM", "pattern": term} for term in INCOTERMS
]

span_patterns = [
    *biz_type_patterns,
    *incoterm_patterns,
]
ruler.add_patterns(span_patterns)


doc = nlp(preambles[0])
print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
print("Spans:", [(span.text, span.label_) for span in doc.spans["ruler"]])

Doc.set_extension("defined_terms", default=[])

expression = r'“([^“”]+)”'
for match in re.finditer(expression, doc.text):
    start, end = match.span()
    span = doc.char_span(start, end, label="DT_DECL")
    # This is a Span object or None if match doesn't map to valid token sequence
    doc._.defined_terms.append(doc.char_span(start+1, end-1, label="DEFTERM"))

print("defined terms:", doc._.defined_terms)