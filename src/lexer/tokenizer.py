# Logic tokenize

import re
from lexer.token import Token
import lexer.token_types as token_types
from lexer.scanner import Scanner

class Tokenizer:
    def __init__(self):
        self.scanner = Scanner()

        self.token_pattern = re.compile(
            r"""
            (//[^\n]*)                        # Single-line comment
            |(/\*.*?\*/)                      # Multi-line comment
            |('[^']')                         # Character constant
            |(\d+\.\d+|\d+)                   # Numeric constant (float/int)
            |([A-Za-z_][A-Za-z0-9_]*)         # Identifiers and keywords
            |(==|!=|>=|<=|\+\+|--|&&|\|\|)    # Multi-char operators
            |([+\-*/%=><!&|^])                # Single-char operators
            |([\(\){}\[\];,\.#])              # Special characters
            |(\s+)                            # Whitespace
            """,
            re.DOTALL | re.VERBOSE
        )

    def tokenize(self, code: str):
        tokens = []
        for match in re.finditer(self.token_pattern, code):
            lexeme = match.group(0)

            if self.scanner.is_comment(lexeme):
                token_type = token_types.TokenType.COMMENT
            elif self.scanner.is_keyword(lexeme):
                token_type = token_types.TokenType.KEYWORD
            elif self.scanner.is_operator(lexeme):
                token_type = token_types.TokenType.OPERATOR
            elif self.scanner.is_special_character(lexeme):
                token_type = token_types.TokenType.SPECIAL_CHARACTER
            elif self.scanner.is_character_constant(lexeme):
                token_type = token_types.TokenType.CHARACTER_CONSTANT
            elif self.scanner.is_numeric_constant(lexeme):
                token_type = token_types.TokenType.NUMERIC_CONSTANT
            elif self.scanner.is_identifier(lexeme):
                token_type = token_types.TokenType.IDENTIFIER
            elif self.scanner.is_whitespace(lexeme):
                token_type = token_types.TokenType.WHITESPACE
            else:
                token_type = token_types.TokenType.IDENTIFIER

            tokens.append(Token(lexeme, token_type))

        return tokens