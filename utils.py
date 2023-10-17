import spacy

nlp = spacy.load("en_core_web_sm")

def clean(string):
    """
    Normalizes whitespace by replacing newlines with single spaces.
    """
    return ' '.join(string.split())

def get_lemmas(strings):
    """
    Returns list of lemmas for one-word strings.
    """
    docs = nlp.pipe(strings)
    return [doc[0].lemma_ for doc in docs]
