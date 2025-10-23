#!/usr/bin/env python

def read_source(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

if __name__ == "__main__":
    # Example usage
    source = read_source("SourceCode.c")
    print(source)
