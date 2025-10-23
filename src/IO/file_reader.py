#!/usr/bin/env python

def read_source(file_path):
    with open(file_path, 'r') as file:
        txt = file.readlines()
    return ''.join(one.strip() + '\n' for one in txt)


if __name__ == "__main__":
    # Example usage
    source = read_source("SourceCode.c")
    print(source)
