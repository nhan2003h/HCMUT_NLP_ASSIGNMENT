from .data import *
import re
from unicodedata import normalize

class Dependency:
    def __init__(self, relation: str, head: str, tail: str):
        self.relation = relation
        self.head = head
        self.tail = tail

    def __str__(self) -> str:
        return f"\"{self.head}\" --{self.relation} -> \"{self.tail}\""

class MaltParser:
    ROOT = "ROOT"
    
    RIGHT_ARC = {
        N: {Q: "noun_query", NAME: "nmod"},
        V: {PUNC: "punc", NAME: "nmod", PP: "pp", YN: "yesno", 
            N: "dobj", ADV: "adv", V: "vmod", Q: "query"},
        Q: [],
        PP: {N: "pobj", NAME: "pobj", PP: "pmod"},
        NAME: [],
        ROOT: {V: "root"},
        YN: [],
        ADV: [],
        P: [],
        DET: [],
        AUX: [],
    }

    LEFT_ARC = {
        N: {V: "subj", NAME: "nmod"},
        V: [],
        Q: {N: "noun_query"},
        PP: [],
        NAME: [],
        ROOT: [],
        YN: [],
        ADV: {V: "adv"},
        P: {N: "det"},
        DET: {N: "det"},
        AUX: [],
    }

    @staticmethod
    def tokenize(text: str, debug: bool = False) -> "list[str]":
        # Normalize and preprocess text
        text = normalize("NFC", text).lower()
        text = re.sub(r"\s{2,}", " ", text)
        text = re.sub(r"(.)\?", r"\1 ?", text)

        # Replace tokens based on the dictionary
        for pattern, replacement in TOKEN_DICT.items():
            text = re.sub(pattern, replacement, text)

        # Filter valid tokens
        tokens = [token for token in text.split(" ") if token in POS]

        if debug:
            print(tokens)
            print(" ".join(POS[token] for token in tokens))
        return tokens

    def parse_dependencies(self, tokens: "list[str]") -> "list[Dependency]":
        buffer = tokens[:]
        stack = [self.ROOT]
        dependencies = []
        root_verb = None

        while buffer:
            top_stack = stack[-1]
            next_buffer = buffer[0]

            top_type = POS[top_stack] if top_stack != self.ROOT else self.ROOT
            next_type = POS[next_buffer]

            # Determine root verb if not set
            if next_type == V and root_verb is None:
                root_verb = next_buffer

            # Handle tuple types for ambiguous POS
            next_type = next_type[0] if isinstance(next_type, tuple) and root_verb == next_buffer else next_type
            top_type = top_type[0] if isinstance(top_type, tuple) and root_verb == top_stack else top_type

            dependency = None

            # RIGHT_ARC
            if next_type in self.RIGHT_ARC.get(top_type, {}):
                relation = self.RIGHT_ARC[top_type][next_type]
                dependency = Dependency(relation, top_stack, next_buffer)
                stack.append(buffer.pop(0))

            # LEFT_ARC
            elif next_type in self.LEFT_ARC.get(top_type, {}):
                relation = self.LEFT_ARC[top_type][next_type]
                dependency = Dependency(relation, next_buffer, top_stack)
                stack.pop()

            # SHIFT
            elif top_type in [V, self.ROOT, PP, NAME, N, P]:
                if top_type == PP and next_type in [YN, PUNC, V]:
                    stack.pop()
                elif top_type == NAME and next_type in [PP, V]:
                    stack.pop()
                else:
                    stack.append(buffer.pop(0))

            # REDUCE
            else:
                stack.pop()

            if dependency:
                dependencies.append(dependency)

        return dependencies

    def parse(self, sentence: str) -> "list[Dependency]":
        tokens = self.tokenize(sentence)
        return self.parse_dependencies(tokens)