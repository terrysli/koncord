from rulers import call_rulers
from matchers import label_defterms

def process(text):
    """
    Runs the entire modified pipeline on a given string.
    """
    nlp, doc = call_rulers(text)
    label_defterms(nlp, doc)

    return doc
