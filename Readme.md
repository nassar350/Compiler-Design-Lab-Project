# C-like Lexer / Tokenizer in Python

A simple lexer/tokenizer for C-like source code implemented in Python. This project parses source code into tokens, classifies them by type, and optionally writes them to an output file. Useful as the first step for building a compiler or interpreter.

---

## 🗂 Project Structure

```
project/
│
├── lexer/
│   ├── token.py            # Token class definition
│   ├── token_types.py      # Token type enum
│   ├── scanner.py          # Helper methods for token classification
│   └── tokenizer.py        # Main tokenizer logic
│
├── IO/
│   ├── file_reader.py      # Reads source code from file
│   └── file_writer.py      # Writes tokens to output file
│
├── main.py                 # Entry point (CLI) for tokenizing a source file
└── README.md
```
---

## ⚡ Features

- Tokenizes C-like source code into:
  - **Keywords** (`int`, `float`, `if`, etc.)
  - **Identifiers** (variable/function names)
  - **Operators** (`+`, `==`, `&&`, etc.)
  - **Numeric Constants** (integers and floats)
  - **Character Constants** (`'a'`, `'1'`)
  - **Special Characters** (`(){}[];,#.`)
  - **Comments** (`// single-line`, `/* multi-line */`)
  - **Whitespace & Newlines**
- Provides a summary of token counts by type.
- Optionally writes tokenized output to a file.

---

## 💻 Requirements

- Python 3.7+
- No external dependencies (uses built-in modules like `re` and `argparse`)

---

## 🚀 Usage

### Command-Line Interface

```bash
python main.py input_file.c -o tokens_output.json
```
- input_file.c → Source code file to tokenize
- -o tokens_output.txt → Optional output file to save tokens
---

## 📊 Example Output

```
Total Tokens: 23

Token Type Counts:
  KEYWORD          : 3
  IDENTIFIER       : 5
  OPERATOR         : 4
  NUMERIC_CONSTANT : 3
  CHARACTER_CONSTANT: 1
  SPECIAL_CHARACTER: 6
  COMMENT          : 1
  WHITESPACE       : 4

Tokens:
[Token (int,TokenType.KEYWORD), Token (main,TokenType.IDENTIFIER), ...]
```
---

## 🔧 How It Works

1. main.py reads the input source file.

2. Tokenizer uses regex patterns and helper methods in Scanner to classify each lexeme.

3. Tokens are stored as instances of the Token class with an associated TokenType.

4. A summary of token counts is printed.

5. If an output file is specified, tokens are written to that file.

---

## 📊 Token Types

| Token Type            | Example                  | Description                               |
|-----------------------|-------------------------|-------------------------------------------|
| KEYWORD               | `int`, `float`, `if`     | Reserved words in the language            |
| IDENTIFIER            | `x`, `main`, `myVar`     | Variable or function names                |
| OPERATOR              | `+`, `==`, `&&`          | Arithmetic, logical, or relational operators |
| NUMERIC_CONSTANT      | `10`, `3.14`             | Integer or floating-point numbers        |
| CHARACTER_CONSTANT    | `'a'`                    | Single character constants                |
| SPECIAL_CHARACTER     | `(`, `)`, `{`, `}`       | Symbols used in syntax                     |
| COMMENT               | `// comment`, `/* comment */` | Single-line or multi-line comments    |
| WHITESPACE / NEWLINE  | ` `, `\n`                | Spaces, tabs, and newline characters     |

---