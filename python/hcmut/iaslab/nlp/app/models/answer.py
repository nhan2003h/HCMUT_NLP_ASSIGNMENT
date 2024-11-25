from .semantic_parser import Procedure
from .data import *

def answer(procedure: Procedure):
    TOUR_DATA, ATIME_DATA, DTIME_DATA, RUNTIME_DATA, BY_DATA = load_data()
    
    q_type = None

    tour_query = []
    
    if procedure.name == "PRINT-ALL":
        for pro in procedure.args:
            if isinstance(pro, Procedure) and "TOUR" in pro.name:
                tour_tokens = pro.name.split(" ")
                if len(tour_tokens) > 1:
                    tour_query = [tour_tokens[1]]
                    q_type = "TOUR"
                else:
                    tour_query = [x for x in TOUR_DATA]
                    q_type = "TOUR"

            elif isinstance(pro, Procedure) and pro.name == "ATIME":
                args = pro.args

                if "?" not in args[1]:
                    tour_query.append(args[1])

            elif isinstance(pro, Procedure) and pro.name == "DTIME":
                args = pro.args

                if "?" not in args[1]:
                    tour_query.append(args[1])

            elif isinstance(pro, Procedure) and pro.name == "RUN-TIME":
                q_type = "RUN-TIME"

            elif isinstance(pro, Procedure) and "BY" in pro.name:
                tour_tokens = pro.name.split(" ")
                if len(tour_tokens) > 1:
                    tour_query = [tour_tokens[1]]
                    q_type = "BY"
                else:
                    tour_query = [x for x in TOUR_DATA]
                    q_type = "BY"

            elif isinstance(pro, Procedure) and "DATE" in pro.name:
                tour_tokens = pro.name.split(" ")
                if len(tour_tokens) > 1:
                    tour_query = [tour_tokens[1]]
                    q_type = "DATE"
                else:
                    tour_query = [x for x in TOUR_DATA]
                    q_type = "DATE"

    ans_string = ""

    if q_type == "TOUR" and tour_query:
        def ignore_escape(string: str) -> str:
            return string.replace("\"", "")
        
        count = 0
        list_tour = []
        for (dt_key, dt_value), (at_key, at_value) in zip(DTIME_DATA.items(), ATIME_DATA.items()):
            if dt_key not in tour_query:
                continue
            for i in zip(dt_value, at_value):
                list_tour.append("Tour " + (TOUR_DATA[dt_key] if dt_key in TOUR_DATA else dt_key) 
                                 + " - " + (TOUR_DATA[i[0][0]] if i[0][0] in TOUR_DATA else i[0][0]) 
                                 + " khởi hành lúc " + ignore_escape(i[0][1])
                                 + " và đến nơi lúc " + ignore_escape(i[1][1]))
                count += 1
        ans_string += "Có " + str(count) + " tour. \n"
        ans_string += ",\n".join(list_tour) + "."
        
    elif q_type == "TOUR":
        ans_string += "Không tìm thấy."

    elif q_type == "RUN-TIME":
        if tour_query[0] in RUNTIME_DATA and RUNTIME_DATA[tour_query[0]][0] == tour_query[1]:
            ans_string += "Đi từ " + (TOUR_DATA[tour_query[0]] if tour_query[0] in TOUR_DATA else tour_query[0]) + " đến " + (TOUR_DATA[tour_query[1]] if tour_query[1] in TOUR_DATA else tour_query[1])
            ans_string += " mất " + RUNTIME_DATA[tour_query[0]][1] + "."

        elif tour_query[1] in RUNTIME_DATA and RUNTIME_DATA[tour_query[1]][0] == tour_query[0]:
            ans_string += "Đi từ " + (TOUR_DATA[tour_query[0]] if tour_query[0] in TOUR_DATA else tour_query[0]) + " đến " + (TOUR_DATA[tour_query[1]] if tour_query[1] in TOUR_DATA else tour_query[1])
            ans_string += " mất " + RUNTIME_DATA[tour_query[1]][1] + "."
        else:
            ans_string += "Không tìm thấy."
    
    elif q_type == "BY" and tour_query:
        for tour in tour_query:
            ans_string += "Tour " + (TOUR_DATA[tour] if tour in TOUR_DATA else tour) + " đi bằng " + (ENG_WORD[BY_DATA[tour]])  + "."

    elif q_type == "DATE" and tour_query:

        def get_date(string: str) -> str:
            string = string.replace("\"", "")
            tokens = string.split(" ")
            for token in tokens:
                if '/' in token:
                    return token
            return ""
        
        list_tour = []
        for at_key, at_value in ATIME_DATA.items():
            if at_key not in tour_query:
                continue
            list_tour.append("Tour " + (TOUR_DATA[at_key] if at_key in TOUR_DATA else at_key) 
                                 + " có thể đi vào các ngày ")
            temp = []
            for i in at_value:
                temp.append(get_date(i[1]))
            list_tour[-1] += ", ".join(temp)
        ans_string += ",\n".join(list_tour) + "."

    return ans_string

def load_data(path=None):
    TOUR = {}
    ATIME = {}
    DTIME = {}
    RUNTIME = {}
    BY = {}
    path = "nlp/input/database.txt"
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.replace('(', '').replace(')', '')
            line = line.replace('HCMC', 'HCM')
            line = line.replace("\n", "")
            
            tokens = line.split(" ")

            if tokens[0] == "TOUR":
                for i in range(len(tokens)):
                    if tokens[i] == 'TOUR':
                        TOUR.update({tokens[i+1]: tokens[i+2]})
                        i += 2
                        continue

            if tokens[0] == "DTIME":
                for i in range(len(tokens)):
                    if tokens[i] == 'DTIME':
                        if tokens[i+1] not in DTIME:
                            DTIME.update({tokens[i+1]: [(tokens[i+2], tokens[i+3] + " " + tokens[i+4])]}) 
                        else:
                            DTIME[tokens[i+1]].append((tokens[i+2], tokens[i+3] + " " + tokens[i+4]))
                        i += 3
                        continue
                    elif tokens[i] == 'ATIME':
                        if tokens[i+1] not in ATIME:
                            ATIME.update({tokens[i+1]: [(tokens[i+2], tokens[i+3] + " " + tokens[i+4])]}) 
                        else:
                            ATIME[tokens[i+1]].append((tokens[i+2], tokens[i+3] + " " + tokens[i+4]))
                        i += 3
                        continue

            if tokens[0] == "RUN-TIME":
                RUNTIME.update({tokens[1]: (tokens[2], tokens[4] + " " + tokens[5])})

            if tokens[0] == "BY":
                BY.update({tokens[1]: tokens[2]})
                
    return TOUR, ATIME, DTIME, RUNTIME, BY