## token categories
from enum import Enum

class TokenType(Enum):
    KEYWORD = "Keyword"
    IDENTIFIER = "Identifier"
    OPERATOR = "Operator"
    NUMERIC_CONSTANT = "Numeric Constant"
    CHARACTER_CONSTANT = "Character Constant"
    SPECIAL_CHARACTER = "Special Character"
    COMMENT = "Comment"
    WHITESPACE = "White Space"
    NEWLINE = "New line"
