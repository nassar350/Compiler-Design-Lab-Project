# C Compiler Frontend: Lexical Analyzer (Scanner) + Syntax Analyzer (Parser)

A comprehensive compiler frontend implementation in Python that performs both lexical analysis and syntax analysis for C-like source code. The project consists of a complete scanner (tokenizer) and a recursive-descent parser that validates syntax according to a formal grammar specification.

---

## 🗂 Project Structure

```
Design Project (Scanner + Parser)/
│
├── src/
│   ├── lexer/
│   │   ├── token.py            # Token class definition
│   │   ├── token_types.py      # Token type enum
│   │   ├── scanner.py          # Helper methods for token classification
│   │   └── tokenizer.py        # Main tokenizer logic (lexical analysis)
│   │
│   ├── parser/
│   │   ├── Grammar.txt         # Formal BNF grammar specification
│   │   └── parser.py           # Recursive-descent parser implementation
│   │
│   ├── IO/
│   │   ├── file_reader.py      # Reads source code from file
│   │   └── file_writer.py      # Writes tokens to output file
│   │
│   ├── main.py                 # Entry point (CLI) - integrates scanner + parser
│   ├── SourceCode.c            # Sample C source code for testing
│   └── result.json             # Token output file
│
└── Readme.md
```
---

## ⚡ Features

### Lexical Analyzer (Scanner)
- **Comprehensive Token Recognition:**
  - **Keywords** (`int`, `float`, `void`, `if`, `else`, `while`, `for`, `return`)
  - **Identifiers** (variable/function names)
  - **Operators** (`+`, `-`, `*`, `/`, `=`, `==`, `!=`, `<`, `<=`, `>`, `>=`, `&&`, `||`)
  - **Numeric Constants** (integers and floats)
  - **Character Constants** (`'a'`, `'1'`)
  - **Special Characters** (`(){}[];,#.`)
  - **Comments** (`// single-line`, `/* multi-line */`)
  - **Whitespace & Newlines**
- Token statistics and summary reporting
- JSON output for token sequences

### Syntax Analyzer (Parser)
- **Recursive-Descent Parser** implementation
- **Complete Grammar Support** for C-like syntax:
  - Program structure with declarations
  - Variable declarations (single and multiple)
  - Function declarations with parameters
  - Compound statements with local variables
  - Control flow statements (`if`/`else`, `while`, `for`, `return`)
  - Expression parsing with proper precedence:
    - Assignment expressions
    - Logical operators (`||`, `&&`)
    - Relational operators (`<`, `<=`, `>`, `>=`, `==`, `!=`)
    - Arithmetic operators (`+`, `-`, `*`, `/`)
  - Function calls with arguments
  - Parenthesized expressions
- **Smart Trivia Handling**: Automatically skips comments, whitespace, and newlines during parsing
- **Comprehensive Error Reporting**: Clear syntax error messages with context
- **Lookahead Support**: Multi-token lookahead for disambiguation

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
- `input_file.c` → Source code file to tokenize and parse
- `-o tokens_output.json` → Optional output file to save tokens

### Execution Flow

1. **Lexical Analysis**: Source code is tokenized into a stream of tokens
2. **Token Statistics**: Display token counts by type
3. **Syntax Analysis**: Parser validates the token stream against grammar rules
4. **Result**: Outputs "Syntax: OK" if valid, or reports syntax errors with details
5. **Output**: Optionally writes tokens to specified file

### Example

```bash
python .\main.py .\SourceCode.c
```

---

## 📊 Example Output

### Sample Input (SourceCode.c)
```c
int main() {
    int x, y;
    if (x == 42) {
        x = x - 3;
    } else {
        y = 3.1;
    }
    return 0;
}
```

### Console Output
```
Total Tokens: 45

Token Type Counts:
  KEYWORD         : 5
  IDENTIFIER      : 6
  OPERATOR        : 5
  NUMERIC_CONSTANT: 3
  SPECIAL_CHARACTER: 20
  COMMENT         : 3
  WHITESPACE      : 2
  NEWLINE         : 1

Tokens:
[Token (int,TokenType.KEYWORD), Token (main,TokenType.IDENTIFIER), ...]

==============================

Syntax: OK
✅ Tokens written to result.json
```
---

## 🔧 How It Works

### Phase 1: Lexical Analysis (Scanner)

1. `main.py` reads the input source file via `file_reader.py`
2. `Tokenizer` uses regex patterns and helper methods in `Scanner` to classify each lexeme
3. Tokens are stored as instances of the `Token` class with an associated `TokenType`
4. A summary of token counts by type is displayed
5. Token stream is passed to the parser

### Phase 2: Syntax Analysis (Parser)

1. `Parser` receives the token stream from the tokenizer
2. Implements recursive-descent parsing based on formal grammar (`Grammar.txt`)
3. Each non-terminal in the grammar has a corresponding `parse_*` method
4. Parser automatically skips trivia (comments, whitespace, newlines) during analysis
5. Uses lookahead to disambiguate grammar productions (e.g., variable vs function declaration)
6. Validates proper nesting of scopes and statement structures
7. Reports syntax errors with descriptive messages if validation fails
8. Confirms successful parse with "Syntax: OK" message

### Key Parser Features

- **Trivia Handling**: `_skip_trivia()` automatically ignores whitespace/comments between tokens
- **Lookahead**: `peek(n)` allows multi-token lookahead for parsing decisions
- **Error Recovery**: Clear error messages indicating expected vs actual tokens
- **Grammar Coverage**: Full implementation of C-like syntax including expressions, statements, and declarations

---

## 📊 Token Types

| Token Type            | Example                     | Description                               |
|-----------------------|-----------------------------|-------------------------------------------|
| KEYWORD               | `int`, `float`, `if`, `while` | Reserved words in the language          |
| IDENTIFIER            | `x`, `main`, `myVar`        | Variable or function names                |
| OPERATOR              | `+`, `-`, `==`, `&&`        | Arithmetic, relational, logical operators |
| NUMERIC_CONSTANT      | `42`, `3.14`                | Integer or floating-point numbers         |
| CHARACTER_CONSTANT    | `'a'`, `'1'`                | Single character literals                 |
| SPECIAL_CHARACTER     | `(`, `)`, `{`, `}`, `;`     | Punctuation and delimiters               |
| COMMENT               | `// ...`, `/* ... */`       | Single-line or multi-line comments       |
| WHITESPACE            | ` `, `\t`                   | Spaces and tabs                          |
| NEWLINE               | `\n`                        | Line breaks                              |

---

## 📝 Grammar Specification

The parser implements a complete C-like grammar defined in `Grammar.txt`. Key grammar rules include:

### Program Structure
```
Program        → DeclList EOF
DeclList       → Decl DeclList | ε
Decl           → VarDecl | FunDecl
```

### Declarations
```
VarDecl        → TypeSpec ID VarDeclTail ;
FunDecl        → TypeSpec ID ( ParamList ) CompoundStmt
TypeSpec       → int | float | void
```

### Statements
```
Stmt           → ExprStmt | CompoundStmt | IfStmt | WhileStmt | ForStmt | ReturnStmt
IfStmt         → if ( Expr ) Stmt ElsePart
WhileStmt      → while ( Expr ) Stmt
ForStmt        → for ( ForInitExpr ; ForCondExpr ; ForIterExpr ) Stmt
ReturnStmt     → return ExprOpt ;
```

### Expressions (with precedence)
```
Expr           → AssignExpr
AssignExpr     → ID = AssignExpr | OrExpr
OrExpr         → AndExpr OrExprTail
AndExpr        → RelExpr AndExprTail
RelExpr        → AddExpr RelOpTail
AddExpr        → Term AddExprTail
Term           → Factor TermTail
Factor         → ( Expr ) | ID FactorTail | Literal
```

*See `Grammar.txt` for complete grammar specification.*

---

## 🛠 Implementation Details

### Parser Architecture

- **Class**: `Parser` in `parser.py`
- **Method**: Recursive-descent with predictive parsing
- **Token Management**: 
  - `peek(n)` - Look ahead n tokens (skipping trivia)
  - `advance()` - Consume current token
  - `expect(type, lexeme)` - Validate and consume expected token
- **Error Handling**: Raises `ParserError` with descriptive messages

### Key Parser Methods

| Method | Grammar Rule | Description |
|--------|--------------|-------------|
| `parse_program()` | Program → DeclList EOF | Entry point |
| `parse_decl()` | Decl → VarDecl \| FunDecl | Declaration with lookahead |
| `parse_compound_stmt()` | CompoundStmt → { ... } | Scoped block |
| `parse_expr()` | Expr → AssignExpr | Expression entry |
| `parse_assign_expr()` | AssignExpr → ID = ... | Assignment with lookahead |
| `parse_factor()` | Factor → ... | Primary expressions |

### Lookahead Strategy

The parser uses lookahead to disambiguate:
- **Variable vs Function**: After `TypeSpec ID`, checks for `(` to distinguish
- **Assignment vs Expression**: After `ID`, checks for `=` operator
- **Statement boundaries**: Identifies statement types by first keyword/symbol

---

## 🧪 Testing

### Test File: `SourceCode.c`
The project includes a sample C source file with:
- Variable declarations (single and multiple)
- Function definitions
- Control structures (`if`/`else`)
- Expressions with operators
- Comments (single-line and multi-line)
- Return statements

### Running Tests
```bash
cd src
python main.py SourceCode.c -o result.json
```

Expected output: `Syntax: OK` (indicates successful parsing)

---

## 🎯 Current Status

### ✅ Completed Features

**Scanner (Lexical Analyzer):**
- ✅ Complete tokenization of C-like syntax
- ✅ All token types recognized (keywords, identifiers, operators, literals, special chars)
- ✅ Single-line and multi-line comment handling
- ✅ Token statistics and reporting
- ✅ JSON output generation

**Parser (Syntax Analyzer):**
- ✅ Full recursive-descent parser implementation
- ✅ Complete grammar coverage for C-like language
- ✅ Variable declarations (single and multiple)
- ✅ Function declarations with parameters
- ✅ Compound statements with local scopes
- ✅ Control flow (`if`/`else`, `while`, `for`, `return`)
- ✅ Expression parsing with proper precedence
- ✅ Assignment expressions
- ✅ Logical operators (`||`, `&&`)
- ✅ Relational operators (`<`, `<=`, `>`, `>=`, `==`, `!=`)
- ✅ Arithmetic operators (`+`, `-`, `*`, `/`)
- ✅ Function calls with arguments
- ✅ Parenthesized expressions
- ✅ Trivia handling (auto-skip whitespace/comments)
- ✅ Multi-token lookahead support
- ✅ Comprehensive error reporting

---

## 🐛 Known Issues

- Parser does not currently track line numbers for error reporting
- No recovery mechanism - parsing stops at first syntax error
- Limited test coverage for edge cases
- Character constants recognized but not fully validated

---

## 🚧 Future Enhancements

1. **Full C Compliance**: Extend grammar to support complete C syntax
2. **Optimization Passes**: Implement compiler optimization techniques
3. **Target Code Generation**: Generate executable code for specific architectures
4. **Interactive Mode**: REPL for testing expressions and statements
5. **Debug Mode**: Verbose output showing parser state transitions
6. **Performance**: Optimize tokenization and parsing for large files

---

## 📚 References

- **Compiler Design Theory**: Aho, Sethi, Ullman - "Compilers: Principles, Techniques, and Tools"
- **Recursive-Descent Parsing**: Top-down predictive parsing technique
- **C Language Specification**: ANSI C / ISO C standards
- **Python Implementation**: Modern Python 3.7+ features (type hints, f-strings)

---

## 👥 Project Information

**Course**: Compiler Design Lab  
**Institution**: College  
**Branch**: main  
**Last Updated**: December 11, 2025

---

## 📄 License

This project is developed for educational purposes as part of a Compiler Design course.
