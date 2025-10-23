# token class
from lexer import token_types

class Token:
    def __init__(self, value: str, token_type: token_types.TokenType):
        self.value = value
        self.type = token_type

    def __repr__(self):
        return f"({self.value}, {self.type.name})"

    def to_dict(self):
        return {
            "value": self.value,
            "type": self.type.name
        }
