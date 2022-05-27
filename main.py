import sys
from dfa import DFA
from constants import *

if __name__ == '__main__':
    keywords = ["def", "if", "else", "while", "return", "break", "continue", "int", "bool", "void", "true", "false"]
    symbols = ["*", "+", "-", "||", "&&", "=", "==", ">", "<", ">=", "<=", "/", "%", "!", "!=", "(", ")", "[", "]", "{", "}", ";"]

    dfa_key = DFA(language=keywords, token=T_KEY)
    dfa_sym = DFA(language=symbols, token=T_SYM)
    dfa_id = DFA(transition_function=TF_ID, final_states=FS_ID)
    dfa_dec = DFA(transition_function=TF_DEC, final_states=FS_DEC)
    dfa_hex = DFA(transition_function=TF_HEX, final_states=FS_HEX)

    input_file_address = sys.argv[1]
    input_file_content = open(input_file_address).read()
    words = input_file_content.split()

    tokens = []
    symbols_table = []

    for word in words:
        start = 0
        end = len(word)
        while start != end:
            s = word[start:end]
            token = dfa_key.run(s) or dfa_sym.run(s) or dfa_id.run(s) or dfa_dec.run(s) or dfa_hex.run(s)
            if not token:
                end -= 1
                continue
            start = end
            end = len(word)
            if token is T_SYM:
                tokens.append((token, s))
            else:
                if s not in symbols_table:
                    symbols_table.append(s)
                tokens.append((token, symbols_table.index(s)))

    print(tokens)
    print(symbols_table)
