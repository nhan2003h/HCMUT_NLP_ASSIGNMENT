from .dependency_to_semantic import SEM

class Procedure:
    def __init__(self, name: str, args: "list[str]"):
        self.name = name
        self.args = args

    def __str__(self):
        args_str = ' '.join(map(str, self.args)) if isinstance(self.args, list) else self.args
        return f"({self.name} {args_str})"

MAP_WORD_TO_DATA_VAR = {
    "tour": "TOUR",
    "tới": "ATIME",
    "từ": "DTIME",
    "đà_nẵng": "DN",
    "hồ_chí_minh": "HCM",
    "nha_trang": "NT",
    "phú_quốc": "PQ",
    "phương_tiện": "BY",
    "bao_lâu": "RUN-TIME",
    "bao_nhiêu": "COUNT",
    "ngày": "DATE",
    "có": "LIST",
    "nhắc": "LIST",
    "đi": "LIST",
}

def generate_procedures(sem: SEM) -> "list[Procedure]":
    subject = extract_subject(sem)
    destination = extract_destination(sem)
    source = extract_source(sem)
    procedures: "list[Procedure]" = []

    if subject == "TOUR":
        if destination:
            procedures.append(Procedure(f"{subject} {destination}", ["?x"]))
        else:
            procedures.append(Procedure(subject, ["?x"]))
        return Procedure("PRINT-ALL", ["?x"] + procedures)

    if subject == "RUN-TIME":
        procedures.append(Procedure(subject, ["?x"]))
        if source:
            procedures.append(Procedure("DTIME", ["?x", source, "?t"]))
        if destination:
            procedures.append(Procedure("ATIME", ["?x", destination, "?t"]))
        return Procedure("PRINT-ALL", ["?x"] + procedures)

    if subject in {"BY", "DATE"}:
        if subject:
            if destination:
                procedures.append(Procedure(f"{subject} {destination}", ["?x"]))
            else:
                procedures.append(Procedure(subject, ["?x"]))
        return Procedure("PRINT-ALL", ["?x"] + procedures)

def extract_subject(sem: SEM) -> str:
    which_subject = find_semantic_unit_by_predicate(sem, "WHICH")
    if which_subject and which_subject.relations:
        if isinstance(which_subject.relations[0], SEM):
            return MAP_WORD_TO_DATA_VAR[which_subject.relations[0].relations[0]]
        return MAP_WORD_TO_DATA_VAR[which_subject.relations[0]]

def extract_destination(sem: SEM) -> str:
    destination = find_semantic_unit_by_predicate(sem, "TO-LOC")
    if destination and destination.relations:
        return MAP_WORD_TO_DATA_VAR[destination.relations[0].relations[0]]

def extract_source(sem: SEM) -> str:
    source = find_semantic_unit_by_predicate(sem, "FROM-LOC")
    if source and source.relations:
        return MAP_WORD_TO_DATA_VAR[source.relations[0].relations[0]]

def find_semantic_unit_by_predicate(sem: SEM, predicate: str) -> SEM:
    if sem.predicate == predicate:
        return sem
    for relation in sem.relations:
        if isinstance(relation, SEM):
            result = find_semantic_unit_by_predicate(relation, predicate)
            if result:
                return result
