# Scanner
import re
class Scanner:
    def __init__(self):
        self.keywords = [
            "int", "float", "char", "double", "if", "else", "for", "while",
            "do", "return", "void", "switch", "case", "break", "continue",
            "struct", "typedef", "static", "const", "unsigned", "signed"
        ]
        self.operators = [
            "+", "-", "*", "/", "%", "=", "==", "!=", ">", "<", ">=", "<=",
            "&&", "||", "++", "--", "&", "|", "!", "^"
        ]
        self.special_characters = [
            "(", ")", "{", "}", "[", "]", ";", ",", ".", "#"
        ]

    def is_keyword(self, word: str):
        return word in self.keywords

    def is_operator(self, char: str):
        return char in self.operators

    def is_special_character(self, char: str):
        return char in self.special_characters

    def is_identifier(self, word: str):
        return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', word) is not None

    def is_numeric_constant(self, word: str):
        return re.match(r'^\d+(\.\d+)?$', word) is not None

    def is_character_constant(self, word: str):
        return re.match(r"^'.'$", word) is not None

    def is_comment(self, text: str):
        return text.startswith("//") or (text.startswith("/*") and text.endswith("*/"))

    def is_whitespace(self, char: str):
        return char.isspace()

    def is_newline(self, char: str):
        return char == '\n'
