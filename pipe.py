from rulers import call_rulers
from matchers import label_dt_decl, label_defterms, label_defterms_lemmas

def process(text):
    nlp, doc = call_rulers(text)
    label_dt_decl(doc)
    label_defterms(nlp, doc)
    label_defterms_lemmas(nlp, doc)

    return doc
