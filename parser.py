from typing import Optional

from constants import RULES, VARIABLES, TERMINALS
from node import Node


class LLOneParser:
    rules = RULES
    non_term_user_def = VARIABLES
    term_user_def = TERMINALS
    start_symbol = "Program"

    def __init__(self, input_string):
        self.input_string = input_string
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

        self.ast_string = self.validate_string_using_stack_buffer()

    @staticmethod
    def remove_left_recursion(diction):
        store = {}
        for lhs in diction:
            alpha_rules = []
            beta_rules = []
            all_rhs = diction[lhs]
            for sub_rhs in all_rhs:
                if sub_rhs[0] == lhs:
                    alpha_rules.append(sub_rhs[1:])
                else:
                    beta_rules.append(sub_rhs)
            if len(alpha_rules) != 0:
                lhs_ = lhs + "'"
                while (lhs_ in diction.keys()) or (lhs_ in store.keys()):
                    lhs_ += "'"
                for b in range(0, len(beta_rules)):
                    beta_rules[b].append(lhs_)
                diction[lhs] = beta_rules
                for a in range(0, len(alpha_rules)):
                    alpha_rules[a].append(lhs_)
                alpha_rules.append(['#'])
                store[lhs_] = alpha_rules
        for left in store:
            diction[left] = store[left]
        return diction

    @staticmethod
    def left_factoring(diction):
        new_dict = {}
        for lhs in diction:
            all_rhs = diction[lhs]
            temp = dict()
            for sub_rhs in all_rhs:
                if sub_rhs[0] not in list(temp.keys()):
                    temp[sub_rhs[0]] = [sub_rhs]
                else:
                    temp[sub_rhs[0]].append(sub_rhs)
            new_rule = []
            tempo_dict = {}
            for term_key in temp:
                all_starting_with_term_key = temp[term_key]
                if len(all_starting_with_term_key) > 1:
                    lhs_ = lhs + "'"
                    while (lhs_ in diction.keys()) or (lhs_ in tempo_dict.keys()):
                        lhs_ += "'"
                    new_rule.append([term_key, lhs_])
                    ex_rules = []
                    for g in temp[term_key]:
                        ex_rules.append(g[1:])
                    tempo_dict[lhs_] = ex_rules
                else:
                    new_rule.append(all_starting_with_term_key[0])
            new_dict[lhs] = new_rule
            for key in tempo_dict.keys():
                new_dict[key] = tempo_dict[key]
        return new_dict

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
        mat = [["" for _ in terminals] for _ in self.diction]

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
        def g(a, n, back=True):
            n2 = Node(arr[0], [], n)
            n.children.append(n2)
            n = n2
            a = a[1:]
            while back and a[0] == ".":
                n = n.parent
                a = a[1:]
            return a, n

        if self.is_ll_one is False:
            return f"\nInput String = \"{self.input_string}\"\n Grammar is not LL(1)"

        stack = [self.start_symbol, '$']
        input_string = self.input_string.split()
        input_string.reverse()
        buffer = ['$'] + input_string
        arr = [self.start_symbol, ]
        node = tree = Node("head", [], None)

        print("{:<180} {:>60}\t{:<60}".format("Buffer", "Stack", "Action"))

        while True:
            if stack == ['$'] and buffer == ['$']:
                print("{:<180} {:>60}\t{:<60}".format(' '.join(buffer), ' '.join(stack), "Valid"))
                if arr[0] == "#":
                    node2 = Node(arr[0], [], node)
                    node.children.append(node2)
                    return tree.print()
            elif stack[0] not in self.term_user_def:
                x = self.nt_list.index(stack[0])
                y = self.tab_term.index(buffer[-1])
                if self.parsing_table[x][y] != '':
                    entry = self.parsing_table[x][y]
                    print("{:<180} {:>60}\t{:<60}".format(
                        ' '.join(buffer), ' '.join(stack), f"T[{stack[0]}][{buffer[-1]}] = {entry}")
                    )
                    if arr[0] == "#":
                        arr, node = g(arr, node)
                    arr, node = g(arr, node, False)
                    arr2 = []
                    for kkk in entry.split("->")[1].split():
                        arr2.append(kkk)
                        arr2.append(".")
                    arr = arr2 + arr
                    lhs_rhs = entry.split("->")
                    lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                    entry_rhs = lhs_rhs[1].split()
                    stack = entry_rhs + stack[1:]
                else:
                    return f"Invalid String! No rule at Table[{stack[0]}][{buffer[-1]}]."
            else:
                if stack[0] == buffer[-1]:
                    print("{:<180} {:>60}\t{:<60}".format(' '.join(buffer), ' '.join(stack), f"Matched:{stack[0]}"))
                    if arr[0] == "#":
                        arr, node = g(arr, node)
                    arr, node = g(arr, node)
                    buffer = buffer[:-1]
                    stack = stack[1:]
                else:
                    return "Invalid String! Unmatched terminal symbols"

    def get_ast_string(self):
        return self.ast_string
