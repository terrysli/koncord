from spacy.matcher import Matcher


def label_indem(nlp, doc):
    patterns = [
        [
            {"LOWER": {"IN": ["shall", "will"]}},
            {"LOWER": {"IN": ["indemnify", "defend"]}}
        ],
        [
            {"LOWER": {"IN": ["shall", "will"]}},
            {"LOWER": "hold"},
            {"LOWER": "harmless"}
        ],
    ]

    matcher = Matcher(nlp.vocab)
    matcher.add("IndemnitiesMatcher", patterns)
    matches = matcher(doc)
    for match_id, start, end in matches:
        print("indemnity found:", doc[start:end].sent.text)
