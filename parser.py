from typing import Optional

from constants import RULES, VARIABLES, TERMINALS


class LLOneParser:
    rules = RULES
    non_term_user_def = VARIABLES
    term_user_def = TERMINALS
    sample_input_string = "def int T_ID ( ) { return ! T_ID == T_HEX ; }"
    start_symbol = "Program"

    def __init__(self):
        self.diction = {}
        for rule in self.rules:
            k = rule.split("->")
            self.diction[k[0].strip()] = [y.split() for y in k[1].split(' | ')]
        self.diction = self.remove_left_recursion(self.diction)
        self.diction = self.left_factoring(self.diction)
        self.nt_list = list(self.diction.keys())
        self.k = {}
        self.firsts = {y: [self.first(sub) for sub in self.diction[y]] for y in self.diction.keys()}
        self.follows = {nt: self.follow(nt) for nt in self.diction}

        self.parsing_table, self.is_ll_one, self.tab_term = self.create_parse_table()

        self.validate_string_using_stack_buffer()

    @staticmethod
    def remove_left_recursion(diction):
        store = {}
        for lhs in diction:
            alphaRules = []
            betaRules = []
            allrhs = diction[lhs]
            for subrhs in allrhs:
                if subrhs[0] == lhs:
                    alphaRules.append(subrhs[1:])
                else:
                    betaRules.append(subrhs)
            if len(alphaRules) != 0:
                lhs_ = lhs + "'"
                while (lhs_ in diction.keys()) or (lhs_ in store.keys()):
                    lhs_ += "'"
                for b in range(0, len(betaRules)):
                    betaRules[b].append(lhs_)
                diction[lhs] = betaRules
                for a in range(0, len(alphaRules)):
                    alphaRules[a].append(lhs_)
                alphaRules.append(['#'])
                store[lhs_] = alphaRules
        for left in store:
            diction[left] = store[left]
        return diction

    @staticmethod
    def left_factoring(diction):
        newDict = {}
        for lhs in diction:
            allrhs = diction[lhs]
            temp = dict()
            for subrhs in allrhs:
                if subrhs[0] not in list(temp.keys()):
                    temp[subrhs[0]] = [subrhs]
                else:
                    temp[subrhs[0]].append(subrhs)
            new_rule = []
            tempo_dict = {}
            for term_key in temp:
                allStartingWithTermKey = temp[term_key]
                if len(allStartingWithTermKey) > 1:
                    lhs_ = lhs + "'"
                    while (lhs_ in diction.keys()) or (lhs_ in tempo_dict.keys()):
                        lhs_ += "'"
                    new_rule.append([term_key, lhs_])
                    ex_rules = []
                    for g in temp[term_key]:
                        ex_rules.append(g[1:])
                    tempo_dict[lhs_] = ex_rules
                else:
                    new_rule.append(allStartingWithTermKey[0])
            newDict[lhs] = new_rule
            for key in tempo_dict:
                newDict[key] = tempo_dict[key]
        return newDict

    def first(self, rule) -> Optional[list]:
        if self.k.get(rule.__str__()):
            return self.k.get(rule.__str__())
        if not rule or not len(rule):
            return None
        if rule[0] in self.term_user_def:
            return [rule[0]]
        elif rule[0] == '#':
            return ['#']
        if rule[0] in self.nt_list:
            firsts = []
            for itr in self.diction[rule[0]]:
                firsts.extend(self.first(itr))

            if '#' in firsts and len(rule) > 1:
                firsts.remove('#')
                if (ans_new := self.first(rule[1:])) is not None:
                    firsts.extend(ans_new)
            self.k[rule.__str__()] = firsts
            return firsts

    def follow(self, nt) -> list:
        follows = []
        if nt == self.start_symbol:
            follows.append('$')
        for curNT in self.diction:
            rhs = self.diction[curNT]
            res = None
            for sub_rule in rhs:
                while nt in sub_rule:
                    index_nt = sub_rule.index(nt)
                    sub_rule = sub_rule[index_nt + 1:]
                    if len(sub_rule) != 0:
                        res = self.first(sub_rule)
                        if '#' in res:
                            res.remove('#')
                            if ans_new := self.follow(curNT):
                                res.extend(ans_new)
                    elif nt != curNT:
                        res = self.follow(curNT)
                    if res:
                        follows.extend(res)
        return list(set(follows))

    def create_parse_table(self):
        nt_list = self.nt_list
        terminals = self.term_user_def
        terminals.append('$')
        mat = [["" for y in terminals] for x in self.diction]

        is_ll_one = True

        for lhs, rhs in self.diction.items():
            for y in rhs:
                res = self.first(y)
                if '#' in res:
                    res.remove('#')
                    res.extend(self.follows[lhs])
                for c in res:
                    xnt = nt_list.index(lhs)
                    yt = terminals.index(c)
                    if mat[xnt][yt] == '':
                        mat[xnt][yt] = mat[xnt][yt] + f"{lhs}->{' '.join(y)}"
                    elif f"{lhs}->{' '.join(y)}" not in mat[xnt][yt]:
                        if lhs == "E1":
                            continue
                        is_ll_one = False
                        mat[xnt][yt] = mat[xnt][yt] + f",{lhs}->{' '.join(y)}"

        return mat, is_ll_one, terminals

    def validate_string_using_stack_buffer(self):
        if self.is_ll_one is False:
            return f"\nInput String = \"{self.sample_input_string}\"\n Grammar is not LL(1)"

        stack = [self.start_symbol, '$']

        input_string = self.sample_input_string.split()
        input_string.reverse()
        buffer = ['$'] + input_string

        print("{:>40} {:>40} {:>40}".format("Buffer", "Stack", "Action"))

        while True:
            if stack == ['$'] and buffer == ['$']:
                print("{:>40} {:>40} {:>40}".format(' '.join(buffer), ' '.join(stack), "Valid"))
                return "\nValid String!"
            elif stack[0] not in self.term_user_def:
                x = self.nt_list.index(stack[0])
                y = self.tab_term.index(buffer[-1])
                if self.parsing_table[x][y] != '':
                    entry = self.parsing_table[x][y]
                    print("{:>40} {:>40} {:>45}".format(' '.join(buffer), ' '.join(stack),
                                                        f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
                    lhs_rhs = entry.split("->")
                    lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                    entryrhs = lhs_rhs[1].split()
                    stack = entryrhs + stack[1:]
                else:
                    return f"\nInvalid String! No rule at Table[{stack[0]}][{buffer[-1]}]."
            else:
                if stack[0] == buffer[-1]:
                    print("{:>40} {:>40} {:>40}".format(' '.join(buffer), ' '.join(stack), f"Matched:{stack[0]}"))
                    buffer = buffer[:-1]
                    stack = stack[1:]
                else:
                    return "\nInvalid String! " \
                           "Unmatched terminal symbols"


if __name__ == "__main__":
    LLOneParser()
