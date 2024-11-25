from .models.malt_parser import *
from .models.dependency_to_semantic import relation_extract
from .models.logical_parser import logical_parse
from .models.semantic_parser import generate_procedures
from .models.answer import answer


def get_questions(path):
    questions = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            line = line.replace("\n", "")
            questions.append(line)
    return questions

def write_to_file(string, path):
    with open(path, "a", encoding="utf-8") as file:
        file.write(string)

def main():
    queries = get_questions("nlp/input/questions.txt")
    malt_parse = MaltParser()
    RIGHT_ARC = malt_parse.RIGHT_ARC
    LEFT_ARC = malt_parse.LEFT_ARC
    for i in range(1,6):
        file_path = f"nlp/output/p2-q-{i}.txt"
        with open(file_path, "w", encoding="utf-8"):
            pass

    output1 = "Trước hết ta định nghĩa các phép RIGHT_ARC và LEFT_ARC sau đây:\n\n"
    output1 += "RIGHT_ARC: \nCó dạng (H,R,T), nghĩa là, từ bên trái là H, , mối quan hệ RIGHT_ARC của chúng là R, từ bên phải là T\n"
    for i in RIGHT_ARC:
        if len(RIGHT_ARC[i]) > 0:
            for j in RIGHT_ARC[i]:
                output1 += ''.join([f"{i:{18}}", f"{RIGHT_ARC[i][j]:{18}}", f"{j:{18}}"]) + "\n"
    output1 += "\n\nLEFT_ARC: \nCó dạng H R T, nghĩa là, từ bên trái là H, mối quan hệ LEFT_ARC của chúng là R, từ bên phải là T\n"
    for i in LEFT_ARC:
        if len(LEFT_ARC[i]) > 0:
            for j in LEFT_ARC[i]:
                output1 += ''.join([f"{i:{18}}", f"{LEFT_ARC[i][j]:{18}}", f"{j:{18}}"]) + "\n"
    output1 += "\nSau khi đã định nghĩa, sử dụng giải thuật MaltParser để phân tích câu."
    output1 += "\n\nMaltParser là một giải thuật phân tích cú pháp phụ thuộc dựa trên hệ thống chuyển trạng thái. Giải thuật sử dụng ngăn xếp (stack) và bộ đệm (buffer) để duyệt qua các từ trong câu. Các phép chuyển chính bao gồm:\n"
    output1 += "- SHIFT: Di chuyển từ đầu của buffer lên stack.\n"
    output1 += "- RIGHT_ARC: Tạo quan hệ phụ thuộc từ đỉnh stack đến từ đầu buffer và di chuyển từ buffer lên stack.\n"
    output1 += "- LEFT_ARC: Tạo quan hệ phụ thuộc từ từ đầu buffer đến đỉnh stack và loại bỏ đỉnh stack.\n"
    output1 += "- REDUCE: Loại bỏ từ đỉnh stack khi từ này đã được xử lý.\n"
    output1 += "Giải thuật lặp lại các phép chuyển trạng thái cho đến khi buffer rỗng và stack chỉ còn ROOT, trả về cây phụ thuộc hoàn chỉnh.\n"
    write_to_file(output1, f"nlp/output/p2-q-1.txt")

    for query in queries:
        output = "Câu hỏi: " + query + "\n"
        context_deps = malt_parse.parse(query)
        output2 = ""
        for x in context_deps:
            output2 += str(x) + "\n"
        output2 += "\n\n"
        write_to_file(output + output2, f"nlp/output/p2-q-2.txt")

        output3 = ""
        relations = relation_extract(context_deps)
        for x in relations:
            output3 += str(x) + "\n"
        output3 += "\n\n"
        write_to_file(output + output3, f"nlp/output/p2-q-3.txt")

        sem = logical_parse(relations)
        output4 = str(sem) + "\n"
        procedure = generate_procedures(sem)
        output4 += str(procedure) + "\n\n\n"
        write_to_file(output + output4, f"nlp/output/p2-q-4.txt")

        output5 = "Trả lời: " + answer(procedure) + "\n\n\n"
        write_to_file(output + output5, f"nlp/output/p2-q-5.txt")


if __name__ == "__main__":
    main()