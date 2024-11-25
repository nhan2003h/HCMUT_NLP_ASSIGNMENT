from .data import *
from .malt_parser import Dependency

class Relation:
    """
    Represents a relationship between two entities in a semantic structure.
    """
    def __init__(self, relation_type: str, left: str, right: str):
        self.type = relation_type  # e.g., AGENT
        self.left = left           # e.g., s1
        self.right = right         # e.g., đến
    
    def __str__(self) -> str:
        return f"({self.left} {self.type} {self.right})"

class SEM:
    """
    Represents a semantic structure with a predicate, variable, and optional relations.
    """
    def __init__(self, predicate: str, variable: str, relations=None):
        self.predicate = predicate
        self.variable = variable
        self.relations = relations if relations else []
    
    def __str__(self) -> str:
        return f"({self.predicate} {self.variable}" \
               + f"{' ' + ' '.join(map(str, self.relations)) if self.relations else ''})"

def create_variable(name: str, existing_vars: "list[str]") -> str:
    """
    Creates a unique variable name based on the given name and existing variables.
    """
    prefix = name[0].lower()
    index = 1
    while True:
        var = f"{prefix}{index}"
        if var not in existing_vars:
            return var
        index += 1

def create_sem(word: str, variables: "list[str]") -> tuple:
    """
    Creates a semantic structure (SEM) or returns the original word if it's not a NAME.
    """
    var = create_variable(word, variables)
    if POS[word] != NAME:
        return word, None
    sem = SEM(POS[word], var, [word])
    return sem, var

def handle_dependent_sem(dependent: str, variables: "list[str]", relation_type: str) -> tuple:
    """
    Handles the creation of a semantic structure for a dependent and updates variables.
    """
    sem, var = create_sem(dependent, variables)
    if var:
        variables.append(var)
    return Relation(relation_type, "s1", sem)

def relation_extract(dependencies: "list[Dependency]") -> "list[Relation]":
    """
    Extracts semantic relationships from a list of dependencies.
    """
    relations = []
    variables = []

    for dep in dependencies:
        # QUERY
        if dep.relation == "query":
            relations.append(Relation("QUERY", "s1", dep.tail))

        elif dep.relation == "noun_query":
            has_query = any(rel.type == "QUERY" for rel in relations)
            rel_type = "CO_QUERY" if has_query else "QUERY"
            relations.append(Relation(rel_type, "s1", dep.head))

        # ROOT
        elif dep.relation == "root":
            variables.append("s1")
            relations.append(Relation("PRED", "s1", dep.tail))

        # SUBJ
        elif dep.relation == "subj" and dep.tail in PRONOUN:
            relations.append(Relation("AGENT", "s1", dep.tail))

        # NMOD
        elif dep.relation == "nmod":
            relation_type = "DES" if POS[dep.tail] == NAME else "THEME"
            relations.append(handle_dependent_sem(dep.tail, variables, relation_type))

        # POBJ
        elif dep.relation == "pobj":
            if dep.head in ["từ", "tới"]:
                relation_type = "SRC" if dep.head == "từ" else "DES"
                relations.append(handle_dependent_sem(dep.tail, variables, relation_type))

    return relations
