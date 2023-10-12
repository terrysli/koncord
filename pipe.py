import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span, Token
from spacy.matcher import Matcher, PhraseMatcher
import re

from categories import STATES, BIZ_TYPES, INCOTERMS
from data.preambles import preambles


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

raw_text = preambles[0]
text = ' '.join(raw_text.split())  # normalizes whitespace
doc = nlp(text)

print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
print("Spans:", [(span.text, span.label_) for span in doc.spans["ruler"]])


########## Labelling defined terms ##########

Doc.set_extension("defined_terms", default=[])

expression = r'“([^“”]+)”'
for match in re.finditer(expression, doc.text):
    start, end = match.span()
    span = doc.char_span(start, end, label="DT_DECL")
    # This is a Span object or None if match doesn't map to valid token sequence
    doc._.defined_terms.append(doc.char_span(start+1, end-1, label="DEFTERM"))

print("defined terms:", doc._.defined_terms)

# Matches all strings in defined terms attribute
def_term_matcher = PhraseMatcher(nlp.vocab)
def_term_patterns = [nlp.make_doc(term.text) for term in doc._.defined_terms]
def_term_matcher.add("DefinedTerms", def_term_patterns)

# Labels all spans matching defined terms as "DEFTERM"
matches = def_term_matcher(doc)
for match_id, start, end in matches:
    span = doc[start:end]
    span.label_ = "DEFTERM"
    # print("defined term found:", span.text, span.label_)
