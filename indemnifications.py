"""
Matchers and functions to label indemnities and indemnification provisions.
"""

from spacy.matcher import Matcher


def label_indem(nlp, doc):
    patterns = [
        # "shall/will indemnify/defend"
        [
            {"LOWER": {"IN": ["shall", "will", "must"]}},
            {"LOWER": {"IN": ["indemnify", "defend"]}}
        ],
        # "shall/will hold harmless"
        [
            {"LOWER": {"IN": ["shall", "will", "must"]}},
            {"LOWER": "hold"},
            {"OP": "*"},
            {"LOWER": "harmless"}
        ],
        # "agrees to indemnify/defend"
        [
            {"LOWER": "agrees"},
            {"LOWER": "to"},
            {"LOWER": {"IN": ["indemnify", "defend"]}}
        ]
    ]

    matcher = Matcher(nlp.vocab)
    matcher.add("IndemnificationMatcher", patterns)
    matches = matcher(doc)
    indemnifications = []
    for match_id, start, end in matches:
        sent = doc[start:end].sent
        indemnifications.append(sent)
        print("indemnification found:", sent.text)

    return indemnifications
