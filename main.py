import sys
from tokenizer import Tokenizer
from parser import LLOneParser

if __name__ == '__main__':
    input_file_address = "source.decaf"  # sys.argv[1]
    decaf_code = open(input_file_address).read()

    decaf_tokenizer = Tokenizer(decaf_code)
    tokens, symbols_table = decaf_tokenizer.run()

    LLOneParser(tokens)

    tokens_file = open("source_tokens.txt", "w")
    symbols_table_file = open("source_symbols_table.txt", "w")

    tokens_string = "\n".join(["\t".join(list(map(str, tokens[i]))) for i in range(len(tokens))])
    tokens_file.write(tokens_string)

    symbols_table_string = "\n".join([str(i + 1) + "\t" + s for i, s in enumerate(symbols_table)])
    symbols_table_file.write(symbols_table_string)
