from categories import BIZ_TYPES, INCOTERMS

defined_term_patterns = [
    {"label": "DT_DECL",
    # TODO: Get this regexp to correctly capture tokens within quotes
    # "pattern": [{"text": {"regexp": '(?<=")[^"]+(?=")'}}
     "pattern": [
         {"TEXT": '“'},
         {"IS_ASCII": True, "IS_TITLE": True, "OP": "+"},
         {"TEXT": '”'}
     ]},
    {"label": "DT_DECL",
     "pattern": [
         {"TEXT": '"'},
         {"IS_ASCII": True, "IS_TITLE": True, "OP": "+"},
         {"TEXT": '"'}
    ]},
]

biz_type_patterns = [
    {"label": "BIZ_TYPE", "pattern": [{"TEXT": {"IN": BIZ_TYPES}}]},
]

incoterm_patterns = [
    {"label": "INCOTERM", "pattern": [{"TEXT": {"IN": INCOTERMS}}]},
]