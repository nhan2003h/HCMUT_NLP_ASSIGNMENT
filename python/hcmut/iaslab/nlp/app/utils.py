from . import task_1, task_2
import os

def test(**kwargs):
    print("hello NLP")
    input_file_path = 'hcmut/iaslab/nlp/data/rules.txt'
    output_file_path = 'nlp/output/grammar.txt'
    # print(f"Current working directory: {os.getcwd()}")
    # cfg = task_1.read_grammar(input_file_path, output_file_path)
    
    # task_1.generate_sentences(cfg, 10000)
    
    # task_1.parse_sentences(cfg, 'hcmut/iaslab/nlp/data/sentences.txt')  
    
    task_2.main()
    
if __name__ == "__main__":
    test()