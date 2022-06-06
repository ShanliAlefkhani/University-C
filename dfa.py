from constants import *


class DFA:
    def __init__(self, transition_function=None, final_states=None, language=None, token=None):
        if transition_function:
            self.transition_function = transition_function
            self.final_states = final_states
            return
        self.create_dfa(language, token)

    def create_dfa(self, language, token):
        tf = {0: {}}
        fs = {}
        state = last_state = 0

        for word in language:
            for c in word:
                flag = False
                for q, v in tf[state].items():
                    if c == q:
                        state = v
                        flag = True
                        break
                if not flag:
                    last_state += 1
                    tf[state] = {**tf[state], c: last_state}
                    state = last_state
                    tf = {**tf, last_state: {}}
            fs.setdefault(state, token)
            state = 0

        self.transition_function = tf
        self.final_states = fs

    @staticmethod
    def match(x: str, q: str):
        x = x.lower()
        q = q.lower()
        if x == q:
            return True
        if ((q == "0-9" and "0" <= x <= "9")
                or (q == "1-9" and "1" <= x <= "9")
                or (q == "a-z" and "a" <= x <= "z")
                or (q == "a-f" and "a" <= x <= "f")):
            return True
        return False

    def run(self, s):
        state = 0
        try:
            for x in s:
                flag = True
                for q, v in self.transition_function[state].items():
                    if self.match(x, q):
                        state = v
                        flag = False
                        break
                if flag:
                    return None
            return self.final_states[state]
        except KeyError:
            return None


keywords = ["def", "if", "else", "while", "return", "break", "continue", "int", "bool", "void", "true", "false"]
symbols = ["*", "+", "-", "||", "&&", "=", "==", ">", "<", ">=", "<=", "/", "%", "!", "!=", "(", ")", "[", "]", "{", "}", ";", "//", "/*", "*/", "\"", ","]

dfa_key = DFA(language=keywords, token=T_KEY)
dfa_sym = DFA(language=symbols, token=T_SYM)
dfa_id = DFA(transition_function=TF_ID, final_states=FS_ID)
dfa_dec = DFA(transition_function=TF_DEC, final_states=FS_DEC)
dfa_hex = DFA(transition_function=TF_HEX, final_states=FS_HEX)