# token class
from lexer import token_types

class Token:
    def __init__(self, value: str, token_type: token_types.TokenType, line: int | None = None, column: int | None = None):
        self.value = value
        self.type = token_type
        self.line = line
        self.column = column

    def __repr__(self):
        loc = f"@{self.line}:{self.column}" if self.line is not None and self.column is not None else ""
        return f"({self.value}, {self.type.name}{(' ' + loc) if loc else ''})"

    def to_dict(self):
        return {
            "value": self.value,
            "type": self.type.name,
            "line": self.line,
            "column": self.column,
        }
