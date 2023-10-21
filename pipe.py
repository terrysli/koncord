from rulers import call_rulers
from defterms import label_defterms

def run_pipe(text):
    nlp, doc = call_rulers(text)
    label_defterms(nlp, doc)

    return doc

def process_file(path):
    """
    Runs the entire modified pipeline on a file.
    """

    with open(path, encoding="utf8") as f:
        text = f.read()
    run_pipe(text)



