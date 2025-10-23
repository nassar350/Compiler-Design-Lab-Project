#!/usr/bin/env python

import json
from lexer.token import Token
from lexer.token_types import TokenType

def _serialize(tokens):
    return [t.to_dict() for t in tokens]


def write_tokens(tokens, file_path):
    file_ext = file_path.split('.')[-1].lower()

    if not file_ext in ['json']:
        raise ValueError(f"Unsupported file extension: .{file_ext}")

    data = _serialize(tokens)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

