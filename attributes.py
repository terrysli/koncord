import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span, Token
from spacy.matcher import Matcher, PhraseMatcher

from categories import STATES, BIZ_TYPES, INCOTERMS
from clauses import preamble1 as text

# Load a spaCy model
nlp = spacy.load("en_core_web_sm")

# Process a sample text
doc = nlp.make_doc(text)

########## Defined Terms ##########

defined_term_matcher = Matcher(nlp.vocab)

smart__quotes_pattern = [
    {"ORTH": '“'},
    {"IS_ASCII": True, "OP": "+"},
    {"ORTH": '”'}
]
dumb_quotes_pattern = [
    {"ORTH": '"'},
    {"IS_ASCII": True, "OP": "+"},
    {"ORTH": '"'}
]
defined_term_matcher.add(
    "DEFINED_TERM",
    [smart__quotes_pattern, dumb_quotes_pattern]
    )

def get_is_defined_term(span):
    return span in span.doc._.defined_terms

Span.set_extension("is_defined_term", getter=get_is_defined_term)

def get_defined_terms(doc):
    matches = defined_term_matcher(doc)
    defined_terms = [Span(doc, start, end) for match_id, start, end in matches]
    return defined_terms

Doc.set_extension("defined_terms", getter=get_defined_terms)

print(len(doc._.defined_terms), "defined terms found:")
for term in doc._.defined_terms:
    print (term.text, term._.is_defined_term)


########## Jurisdictions ##########

state_matcher = PhraseMatcher(nlp.vocab)
state_patterns = list(nlp.pipe(STATES))
state_matcher.add("STATE", state_patterns)
matches = state_matcher(doc)
print(len(matches), f"jurisdiction{'' if len(matches) == 1 else 's'} found:")
for match_id, start, end in matches:
    span = Span(doc, start, end, label="JDX")
    print(span, span.label_)


########## Business Types ##########

biz_type_matcher = PhraseMatcher(nlp.vocab)
biz_type_patterns = list(nlp.pipe(BIZ_TYPES))
biz_type_matcher.add("BUSINESS_TYPE", biz_type_patterns)

matches = biz_type_matcher(doc)
print(len(matches), f"business type{'' if len(matches) == 1 else 's'}:",
      [doc[start:end] for match_id, start, end in matches])


########## Incoterms ##########

incoterm_matcher = PhraseMatcher(nlp.vocab)
incoterm_patterns = list(nlp.pipe(INCOTERMS))
incoterm_matcher.add("INCOTERM", incoterm_patterns)
matches = incoterm_matcher(doc)
print(len(matches), f"Incoterm{'' if len(matches) == 1 else 's'} found:")
for match_id, start, end in matches:
    span = Span(doc, start, end, label="INCOTERM")
    print(span, span.label_)
