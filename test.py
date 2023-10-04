import spacy

nlp = spacy.blank("en")
ruler = nlp.add_pipe("span_ruler")
patterns = [{"label": "ORG", "pattern": "Apple"},
            {"label": "GPE", "pattern": [{"LOWER": "san"}, {"LOWER": "francisco"}]}]
ruler.add_patterns(patterns)

doc = nlp("Apple is opening its first big office in San Francisco.")
print([(span.text, span.label_) for span in doc.spans["ruler"]])