from spacy.tokens import Doc
from spacy.matcher import Matcher, PhraseMatcher
import re

from utils import get_lemmas

Doc.set_extension("defined_terms", default=[], force=True)

def label_defterms(nlp, doc):
    label_dt_decl(doc)
    label_defterm_instances(nlp, doc)
    label_defterm_lemmas(nlp, doc)


def label_dt_decl(doc):
    """
    Matches phrases in quotes, labels them as DT_DECL (defined term
    declarations, and adds the terms (w/out quotes) into defined_terms extension
    attribute of doc.
    """
    expression = r'[“"][^“”"]+\.?[”"]'
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end, label="DT_DECL")
        # This is a Span object or None if match doesn't map to valid token
        # sequence
        if span is not None:
            # Removes surrounding quotes
            span = doc.char_span(start+1, end-1)
            # Removes period if inside quotes
            if span.text[-1] == '.':
                span = doc.char_span(start+1, end-2)
            span.label_ = "DEFTERM"
            doc._.defined_terms.append(span)

    print("defined terms:", doc._.defined_terms)

def label_defterm_instances(nlp, doc):
    """
    Finds all instances of defined terms in doc and labels them as DEFTERMS.
    """
    # Matches all strings in defined terms attribute
    def_term_matcher = PhraseMatcher(nlp.vocab)
    def_term_patterns = [nlp.make_doc(term.text)
                         for term in doc._.defined_terms]
    def_term_matcher.add("DefinedTerms", def_term_patterns)

    # Labels all spans matching defined terms as "DEFTERM"
    matches = def_term_matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        span.label_ = "DEFTERM"
        print("defined term found:", span.text, span.label_)

def label_defterm_lemmas(nlp, doc):
    """
    Finds all instances of words that share lemmas with defined terms but are
    not exactly defined terms, and labels them as DEFTERMS.
    """
    # Matches all single tokens with shared lemmas as defined terms.
    defterm_lemma_matcher = Matcher(nlp.vocab)
    lower_defterms = [term.text.lower() for term in doc._.defined_terms]
    lemmas = get_lemmas(lower_defterms)
    print("lemmas:", lemmas)
    defterm_lemma_patterns = [[{"LEMMA": lemma}] for lemma in lemmas]
    defterm_lemma_matcher.add("DefinedTermsLemmas", defterm_lemma_patterns)

    matches = defterm_lemma_matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        span.label_ = "DEFTERM"
        print("defined term found:", span.text, span.label_)
