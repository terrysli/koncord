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
    patterns = [
        [{"IS_TITLE": True,
          "IS_SENT_START": False,
          "OP": "{1,3}"}]
    ]

    matcher = Matcher(nlp.vocab)
    matcher.add("UndefinedTermsMatcher", patterns)
    matches = matcher(doc)
    defterms_strings = [term.text for term in doc._.defterms]
    for match_id, start, end in matches:
        span = doc[start:end]
        # Returns true if no token in span is part of an entity
        no_tokens_in_entity = True
        for token in span:
            if token.ent_type_:
                no_tokens_in_entity = False
        if (span.text not in defterms_strings) and no_tokens_in_entity:
            span.label_ = "UNDEFINED"
            doc._.undefined.append(span)

    # print("undefined terms:", doc._.undefined)
