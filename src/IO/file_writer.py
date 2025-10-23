#!/usr/bin/env python

import json

def _serialize(tokens):
    return [t.to_dict() for t in tokens]


def write_tokens(tokens, file_path):
    file_ext = file_path.split('.')[-1].lower()

    if file_ext not in ['json']:
        raise ValueError(f"Unsupported file extension: .{file_ext}")

    data = _serialize(tokens)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

