from rulers import call_rulers
from defterms import label_defterms
from undefined import label_undefined
from ner import run_ner

def run_pipe(text):
    nlp, doc = call_rulers(text)
    label_defterms(nlp, doc)
    run_ner(doc)
    label_undefined(nlp, doc)
    summarize(doc)

    return doc

def process_file(path):
    """
    Runs the entire modified pipeline on a file.
    """

    with open(path, encoding="utf8") as f:
        text = f.read()
    run_pipe(text)

def summarize(doc):
    """
    Prints summary of entities and spans.
    """

    print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
    print("Spans:", [(span.text, span.label_) for span in doc.spans["ruler"]])
    print("Defined Terms:", doc._.defterms)
    print("Undefined Terms:", doc._.undefined)



