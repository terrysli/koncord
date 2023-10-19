"""
Matchers and functions to label indemnities and indemnification provisions.
"""

from spacy.matcher import Matcher


def label_indem(nlp, doc):
    patterns = [
        # "shall/will indemnify/defend"
        [
            {"LOWER": {"IN": ["shall", "will"]}},
            {"LOWER": {"IN": ["indemnify", "defend"]}}
        ],
        # "shall/will hold harmless"
        [
            {"LOWER": {"IN": ["shall", "will"]}},
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
    for match_id, start, end in matches:
        print("indemnification found:", doc[start:end].sent.text)
