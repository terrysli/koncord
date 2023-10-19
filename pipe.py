from rulers import call_rulers
from matchers import label_defterms

def process_str(text):
    """
    Runs the entire modified pipeline on a given string.
    """
    nlp, doc = call_rulers(text)
    label_defterms(nlp, doc)

    return doc

def process_file(path):
    """
    Runs the entire modified pipeline on a file.
    """

    with open(path, encoding="utf8") as f:
        text = f.read()

    print("text:", text)
    nlp, doc = call_rulers(text)
    label_defterms(nlp, doc)

    return doc

