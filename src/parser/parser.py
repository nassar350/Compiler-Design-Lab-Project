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

    def expect(self, type_: TokenType | None = None, lexeme: str | None = None, advance: bool = True) -> Token:
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

        if advance:
            self.pos += 1
        return tok

    def expect_eof(self) -> None:
        """Ensure there are no remaining non-trivia tokens."""
        if self.peek() is not None:
            tok = self.peek()
            raise ParserError(f"Unexpected extra token {tok.value!r} of type {tok.type.name}")
    

    # --- Grammer Implementation ---

    # Program → DeclList EOF
    def parse_program(self) -> None:
        """Entry point: Program → DeclList (for now, just consume tokens).

        This is intentionally minimal. You will progressively replace the
        body with calls to the real grammar methods (parse_decl_list, etc.).
        """
        tok = self.peek()
        if tok is None:
            raise ParserError("Empty input: no tokens to parse")

        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int" , "float", "void"}:
            self.parse_decl_list()
            self.expect_eof()
        else :
            raise ParserError(f"Unexpected token {tok.value!r} of type {tok.type.name}")

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
        tok = self.peek()
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int" , "float", "void"}:
            #lookahead to decide between VarDecl and FunDecl
            self.parse_type_spec()
            id_token = self.expect(TokenType.IDENTIFIER)
            next_token = self.peek()
            if next_token is not None and next_token.value == '(':
                # Function declaration
                self.expect(lexeme='(')
                self.parse_param_list()
                self.expect(lexeme=')')
                self.parse_compound_stmt()
            else:
                # Variable declaration
                self.parse_var_decl_tail()
                self.expect(lexeme=';')
        else:
            raise ParserError("Syntax error in declaration")

    # VarDecl        → TypeSpec ID VarDeclTail ';'
    def parse_var_decl(self) -> None:
        tok = self.peek()
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int", "void", "float"}:
            self.parse_type_spec()
            self.expect(TokenType.IDENTIFIER)
            self.parse_var_decl_tail()
            self.expect(lexeme=';')
        else:
            raise ParserError("Syntax error in variable declaration")

    # VarDeclTail    → (',' ID)*
    def parse_var_decl_tail(self) -> None:
        tok = self.peek()
        if tok is not None and tok.value == ';':
            return 
        self.expect(lexeme=',')
        self.expect(TokenType.IDENTIFIER)
        self.parse_var_decl_tail()

    # ParamList      → (TypeSpec ID (',' TypeSpec ID)*)?
    def parse_param_list(self) -> None:
        tok = self.peek()
        if tok is not None and ((tok.type == TokenType.KEYWORD and tok.value == "void") or tok.value == ')'):
            if tok.value == "void":
                self.advance()
            return
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int", "void", "float"}:
            self.parse_type_spec()
            self.expect(TokenType.IDENTIFIER)
            self.parse_param_list_tail()
        else:
            raise ParserError("Syntax error")

    # ParamListTail  → (',' TypeSpec ID)*
    def parse_param_list_tail(self) -> None:
        tok = self.peek()
        if tok is not None and tok.value == ')':
            return
        self.expect(lexeme=',')
        self.parse_type_spec()
        self.expect(TokenType.IDENTIFIER)
        self.parse_param_list_tail()

    # TypeSpec       → 'int' | 'float' | 'void'
    def parse_type_spec(self) -> None:
        tok = self.peek()
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int" , "float", "void"}:
            self.advance()
        else:
            raise ParserError("Syntax error")

    # CompoundStmt   → '{' LocalDeclList StmtList '}'
    def parse_compound_stmt(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax error")
        self.expect(lexeme='{')
        self.parse_local_decl_list()
        self.parse_stmt_list()
        self.expect(lexeme='}')

    # LocalDeclList → (VarDecl)*
    def parse_local_decl_list(self) -> None:
        tok = self.peek()
        # TODO: here you take a look ahead to decide whether to parse VarDecl or return (find better way?)
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int" , "float" , "void"}:
            self.parse_var_decl()
            self.parse_local_decl_list()
        else:
            return

    # StmtList      → (Stmt)*
    # ID, '{',  if, while, for, return
    def parse_stmt_list(self) -> None:
        tok = self.peek()
        if tok is None:
            return
        if tok is not None and (tok.type == TokenType.KEYWORD and tok.value in {"if", "while", "for", "return"}) or tok.value == '{' or tok.type == TokenType.IDENTIFIER:
            self.parse_stmt()
            self.parse_stmt_list()
        else:
            return

    # Stmt          → ExprStmt | CompoundStmt | IfStmt | WhileStmt | ForStmt | ReturnStmt
    def parse_stmt(self) -> None:
        tok = self.peek()
        if tok is not None:
            if tok.value == '{':
                self.parse_compound_stmt()
            elif tok.type == TokenType.KEYWORD and tok.value == "if":
                self.parse_if_stmt()
            elif tok.type == TokenType.KEYWORD and tok.value == "while":
                self.parse_while_stmt()
            elif tok.type == TokenType.KEYWORD and tok.value == "for":
                self.parse_for_stmt()
            elif tok.type == TokenType.KEYWORD and tok.value == "return":
                self.parse_return_stmt()
            elif tok.type == TokenType.IDENTIFIER:
                self.parse_expr_stmt()
            else:
                raise ParserError("Syntax error in statement")
        else:
            raise ParserError("Syntax error in statement")

    # ExprStmt      → Expr ';' | ';'
    def parse_expr_stmt(self) -> None:
        tok = self.peek()
        if tok is not None and tok.value == ';':
            self.expect(lexeme=';')
            return
        else:
            self.parse_expr()
            self.expect(lexeme=';')

    # IfStmt         → 'if' '(' Expr ')' Stmt ElsePart
    def parse_if_stmt(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax error in if statement")

        self.expect(TokenType.KEYWORD, lexeme='if')
        self.expect(lexeme='(')
        self.parse_expr()
        self.expect(lexeme=')')
        self.parse_stmt()
        self.parse_else_part()

    # ElsePart      → 'else' Stmt | ε
    def parse_else_part(self) -> None:
        tok = self.peek()
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value == 'else':
            self.expect(lexeme='else')
            self.parse_stmt()
        else:
            return

    # WhileStmt      → 'while' '(' Expr ')' Stmt
    def parse_while_stmt(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax error in while statement")

        self.expect(TokenType.KEYWORD, lexeme='while')
        self.expect(lexeme='(')
        self.parse_expr()
        self.expect(lexeme=')')
        self.parse_stmt()

    # ForStmt        → 'for' '(' ExprStmt ExprStmt Expr ')' Stmt
    def parse_for_stmt(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax error in for statement")

        self.expect(TokenType.KEYWORD, lexeme='for')
        self.expect(lexeme='(')
        self.parse_expr_stmt()
        self.parse_expr_stmt()
        self.parse_expr()
        self.expect(lexeme=')')
        self.parse_stmt()

    # ReturnStmt     → 'return' ExprOpt ';'
    def parse_return_stmt(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax error in return statement")

        self.expect(TokenType.KEYWORD, lexeme='return')
        self.parse_expr_opt()
        self.expect(lexeme=';')



    # Stmt, IfStmt, WhileStmt, ForStmt, ReturnStmt, Expr, etc.
    # Add more parse_* methods following your grammar as needed.
