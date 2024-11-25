from .dependency_to_semantic import Relation, SEM

def logical_parse(relations: "list[Relation]") -> SEM:
    mapping: "dict[str, Relation]" = {}
    for relation in relations:
        mapping[relation.type] = relation

    sem = None
    agent_sem = None

    if mapping["QUERY"].right == "tour":
        agent = mapping["QUERY"]
        agent_sem = SEM("THEME","", [SEM("WHICH", "", [agent.right])])

    elif mapping["QUERY"].right == "bao_lâu":
        agent = mapping["QUERY"]
        agent_sem = SEM("HOW-LONG","", [SEM("WHICH", "", [agent.right])])

    elif mapping["QUERY"].right == "bao_nhiêu":
        agent = mapping["QUERY"]
        agent_sem = SEM("QUANT","", [SEM("HOW-MANY", "", [agent.right])])

    elif mapping["QUERY"].right == "phương_tiện":
        agent = mapping["QUERY"]
        agent_sem = SEM("INSTR","", [SEM("WHICH", "", [agent.right])])

    elif mapping["QUERY"].right == "ngày":
        agent = mapping["QUERY"]
        agent_sem = SEM("DATE","", [SEM("WHICH", "", [agent.right])])

    if "CO_QUERY" in mapping and mapping["CO_QUERY"].right == "tour":
        agent = mapping["CO_QUERY"]
        agent_sem.relations.append(SEM("WHICH", "", [agent.right]))

    pred = mapping["PRED"]
    if "THEME" in mapping:

        theme = mapping["THEME"]
        theme_sem = SEM("THEME", "", [theme.right])

        pred_sem_relations = list(filter(None.__ne__,
                                [agent_sem, theme_sem]))
        pred_sem = SEM(pred.right, pred.left, pred_sem_relations)

        sem = SEM("WH-QUERY", "", [pred_sem])

    elif "SRC" in mapping or "DES" in mapping:
        src_sem = None
        des_sem = None
        if "SRC" in mapping:
            src_sem = SEM("FROM-LOC", "", [mapping["SRC"].right])
        if "DES" in mapping:
            des_sem = SEM("TO-LOC", "", [mapping["DES"].right])

        pred_sem_relations = list(filter(None.__ne__,
                                [agent_sem, src_sem, des_sem]))
        pred_sem = SEM(pred.right, pred.left, pred_sem_relations)

        sem = SEM("WH-QUERY", "", [pred_sem])

    else:
        agent_s = []
        if "AGENT" in mapping:
            agent_ = mapping["AGENT"]
            agent_s = [SEM("AGENT", pred.left, [agent_.right])]

        pred_sem_relations = list(filter(None.__ne__,
                                [agent_sem]))
        
        pred_sem = SEM(pred.right, pred.left, agent_s + pred_sem_relations)

        sem = SEM("WH-QUERY", "", [pred_sem])

    return sem