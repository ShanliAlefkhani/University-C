from dfa import *


class Tokenizer:
    def __init__(self, decaf_code):
        self.decaf_code = decaf_code
        self.tokens = []
        self.symbols_table = []
        self.comment = False
        self.string = False
        self.current_string = ""
        self.start = 0
        self.end = len(decaf_code)

    def is_space(self, s):
        if s.isspace():
            if self.string:
                self.current_string += s
            self.start += len(s)
            self.end = len(self.decaf_code)
            return True
        return False

    def process_token(self, s, token):
        if token is T_SYM:
            if s == "*/":
                self.comment = False
            if not self.comment:
                self.tokens.append((token, s))
            if s == "\"":
                x = self.start + self.decaf_code[self.start+1:].find("\"") + 1
                while self.decaf_code[x-1] == "\\":
                    x += self.decaf_code[x+1:].find("\"") + 1
                self.tokens.append((T_STR, self.decaf_code[self.start+1:x]))
                self.tokens.append((token, s))
                self.end = x + 1
            if s == "/*":
                self.comment = True
            if s == "//":
                self.end += self.decaf_code[self.start:].find("\n")
        else:
            if self.string:
                self.current_string += s
            if not self.comment and not self.string:
                if s not in self.symbols_table:
                    self.symbols_table.append(s)
                self.tokens.append((token, self.symbols_table.index(s) + 1))

    def run(self):
        while self.start != self.end:
            s = self.decaf_code[self.start:self.end]
            if self.is_space(s):
                continue
            token = dfa_key.run(s) or dfa_sym.run(s) or dfa_id.run(s) or dfa_dec.run(s) or dfa_hex.run(s)
            if token:
                self.process_token(s, token)
                self.start = self.end
                self.end = len(self.decaf_code)
            else:
                self.end -= 1
        return self.tokens, self.symbols_table
