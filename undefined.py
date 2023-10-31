"""
Matchers and functions to label undefined terms.
"""

from spacy.tokens import Doc
from spacy.matcher import Matcher

Doc.set_extension("undefined", default=[], force=True)

def label_undefined(nlp, doc):
    """
    Finds and labels undefined terms, i.e., capitalized non-named entities that
    do not have a corresponding defined term declaration.
    """
    patterns = [{"IS_TITLE": True, "OP": "+"}]

    matcher = Matcher(nlp.vocab)
    matcher.add("UndefinedTermsMatcher", patterns)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start, end]
        if span not in doc._.defterms and span not in doc.ents:
            span.label_ = "UNDEFINED"
            doc._.undefined.append(span)

    print("undefined terms:", doc._.undefined)

