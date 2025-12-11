from lexer.token import Token
from lexer.token_types import TokenType


class ParserError(Exception):
    """Raised when a syntax error is encountered during parsing."""
    pass


class Parser:
    """Recursive-descent parser skeleton for C-like syntax checking.

    Usage:
        parser = Parser(tokens)
        parser.parse_program()  # raises ParserError on syntax error
    """

    def __init__(self, tokens: list[Token]):
        # Keep all tokens, but parser methods should *skip* comments/whitespace/newlines.
        self.tokens = tokens
        self.pos = 0

    # --- Core helpers -----------------------------------------------------

    def _is_trivia(self, token: Token) -> bool:
        return token.type in {
            TokenType.COMMENT,
            TokenType.WHITESPACE,
            TokenType.NEWLINE,
        }

    def _skip_trivia(self) -> None:
        while self.pos < len(self.tokens) and self._is_trivia(self.tokens[self.pos]):
            self.pos += 1

    def peek(self) -> Token | None:
        """Return current non-trivia token without consuming it, or None at end."""
        self._skip_trivia()
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self) -> Token | None:
        """Consume and return current non-trivia token, or None at end."""
        tok = self.peek()
        if tok is not None:
            # peek() already skipped trivia and positioned on a real token
            self.pos += 1
        return tok

    def expect(self, type_: TokenType | None = None, lexeme: str | None = None) -> Token:
        """Consume one token and validate type and/or lexeme.
        - If type_ is not None: token.type must equal it.
        - If lexeme is not None: token.value must equal it.
        """
        tok = self.peek()
        if tok is None:
            raise ParserError("Unexpected end of input")

        if type_ is not None and tok.type is not type_:
            raise ParserError(f"Expected token type {type_.name}, got {tok.type.name} ({tok.value!r})")

        if lexeme is not None and tok.value != lexeme:
            raise ParserError(f"Expected '{lexeme}', got {tok.value!r}")

        self.pos += 1
        return tok

    # --- Grammar entry point ----------------------------------------------

    def parse_program(self) -> None:
        """Entry point: Program → DeclList (for now, just consume tokens).

        This is intentionally minimal. You will progressively replace the
        body with calls to the real grammar methods (parse_decl_list, etc.).
        """
        # TODO: implement according to your grammar, e.g.:
        #   self.parse_decl_list()
        #   self.expect_eof()
        # For now, just verify that there is at least one token.
        if self.peek() is None:
            # Empty input is considered an error for now
            raise ParserError("Empty input: no tokens to parse")
        tok = self.peek()
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int" , "float", "void"}:
            self.parse_decl_list()
            self.expect_eof()
        else :
            raise ParserError(f"Unexpected token {tok.value!r} of type {tok.type.name}")
        

    def expect_eof(self) -> None:
        """Ensure there are no remaining non-trivia tokens."""
        if self.peek() is not None:
            tok = self.peek()
            raise ParserError(f"Unexpected extra token {tok.value!r} of type {tok.type.name}")

    # --- Placeholders for grammar rules -----------------------------------
    # Below are stubs you can fill in based on the agreed grammar.

    # Program        → DeclList EOF
    def parse_decl_list(self) -> None:
        tok = self.peek()
        #base case 
        if tok is None:
            return
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int" , "float", "void"}:
            self.parse_decl()
            self.parse_decl_list()
        else:
            raise ParserError("Syntax error")
    # Decl           → VarDecl | FunDecl
    def parse_decl(self) -> None:
        raise NotImplementedError("parse_decl not implemented yet")

    # VarDecl        → TypeSpec ID VarDeclTail ';'
    def parse_var_decl(self) -> None:
        raise NotImplementedError("parse_var_decl not implemented yet")

    # FunDecl        → TypeSpec ID '(' ParamList ')' CompoundStmt
    def parse_fun_decl(self) -> None:
        raise NotImplementedError("parse_fun_decl not implemented yet")

    # TypeSpec       → 'int' | 'float' | 'void'
    def parse_type_spec(self) -> None:
        raise NotImplementedError("parse_type_spec not implemented yet")

    # CompoundStmt   → '{' LocalDeclList StmtList '}'
    def parse_compound_stmt(self) -> None:
        raise NotImplementedError("parse_compound_stmt not implemented yet")

    # Stmt, IfStmt, WhileStmt, ForStmt, ReturnStmt, Expr, etc.
    # Add more parse_* methods following your grammar as needed.
