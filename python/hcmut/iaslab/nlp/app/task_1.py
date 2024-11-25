import nltk
from nltk import CFG
from nltk.parse.generate import generate
from pyvi import ViTokenizer
import os
# read grammar from file
def read_grammar(input_grammar_file, output_grammar_file):
    with open(input_grammar_file, 'r', encoding="utf-8") as f:
        grammar = f.read()
    with open(output_grammar_file, 'w', encoding="utf-8") as f:
        f.write(grammar)
    with open(output_grammar_file, 'r', encoding="utf-8") as f:
        grammar = f.read()
    return CFG.fromstring(grammar)

# generate sentences from grammar and save to output/samples.txt
def generate_sentences(grammar, num_sentences=10000):
    
    sentences = []
    for sentence in generate(grammar, n=num_sentences):
        sentence_str = ' '.join(sentence)
        sentences.append(sentence_str)
        
    output_path = 'nlp/output/samples.txt'
    # Print current working directory and output path for debugging
    try:   
        with open(output_path, 'w', encoding="utf-8") as f:
            f.write('\n'.join(sentences))
        # while (1):
        #     pass
        
        print("Done! Generated " + str(num_sentences) + " sentences in output/samples.txt!")
    except Exception as e:
        print(f"Error! Cannot write to file {output_path}! Exception: {e}")
        
# parse sentence and return the tree
def parse(grammar, sentence):
    tokens = ViTokenizer.tokenize(sentence)
    tokens_list = tokens.split()
    
    for i in range(len(tokens_list)):
        if '_' in tokens_list[i]:
            tokens_list[i] = tokens_list[i].replace('_', ' ')
    # print(tokens_list)     
    parser = nltk.ChartParser(grammar)
    
    for tree in parser.parse(tokens_list):
        return tree
    
    return None

# read file from input/sentences.txt and parse it and save to output/parsed-results.txt
def parse_sentences(grammar, file_path):
    file_path = 'hcmut/iaslab/nlp/data/sentences.txt'
    with open(file_path, 'r', encoding="utf-8") as f:
        sentences = f.readlines()
    # print(sentences)
    try:
        with open('nlp/output/parsed-results.txt', 'w', encoding="utf-8") as f:
            for sentence in sentences:
                tree = parse(grammar, sentence)
                # print(tree)
                f.write('======================================================================\n')
                f.write("The sentence: " + sentence + "\n")
                f.write("Parsed rule:\n")
                if tree is not None:
                    f.write(str(tree) + '\n')
                else:
                    f.write("Cannot parse:" + sentence + '\n')
        
        print("Done! Parsed sentences in output/parsed-results.txt!")
    except Exception as e:
        print("Error Cannot write to file output/parsed-results.txt!" + str(e))