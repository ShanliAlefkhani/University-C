from constants import T_KEY, T_SYM


def convert_tokens(tokens, symbols_table):
    parser_input_list = []
    for t in tokens:
        if t[0] is T_KEY:
            parser_input_list.append(symbols_table[t[1]])
        elif t[0] is T_SYM:
            if t[1] in ["//", "*/", "/*"]:
                continue
            parser_input_list.append(t[1])
        else:
            parser_input_list.append(t[0])
    return parser_input_list
