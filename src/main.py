#!/usr/bin/env python

import argparse
import sys
from lexer.tokenizer import Tokenizer
from IO.file_reader import read_source
from IO.file_writer import write_tokens
from lexer.token_types import TokenType
from parser.parser import Parser, ParserError

def print_summary(tokens):
    print(f"Total Tokens: {len(tokens)}", end="\n\n")

    # Statistics
    stats = {}
    for t in tokens:
        stats[t.type] = stats.get(t.type, 0) + 1

    print("Token Type Counts:")
    for token_type in TokenType:
        count = stats.get(token_type, 0)
        print(f"  {token_type.name:<12}: {count}")

    print("\nTokens:")
    print(tokens)

    print("==============================\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument(
        "-o", "--output",
        required=False
    )

    args = parser.parse_args()

    # INPUT
    try:
        source_code = read_source(args.input_file)
    except FileNotFoundError:
        print(f"❌ Error: File '{args.input_file}' not found.")
        sys.exit(1)

    # TOKENIZATION
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(source_code)
    
    # PARSING
    parser = Parser(tokens)
    try:
        parser.parse_program()
        parser.expect_eof()
        print("Syntax is correct. ✅\n")
    except ParserError as e:
        print(f"{e}. ❌\n")

    # OUTPUT
    if args.output:
        try:
            write_tokens(tokens, args.output)
        except ValueError as ve:
            print(f"❌ Error: {ve}")
            sys.exit(1)
        print(f"✅ Tokens written to {args.output}")

if __name__ == "__main__":
    main()
