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
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int" , "float"}:
            self.parse_type_spec()
            self.expect(TokenType.IDENTIFIER)
            self.parse_param_list_tail()
        else:
            raise ParserError("Syntax error")
    def parse_param_list_tail(self) -> None:
        tok = self.peek()
        if tok is not None and tok.value == ')':
            return
        self.expect(lexeme=',')
        self.parse_type_spec()
        self.expect(TokenType.IDENTIFIER)
        self.parse_param_list_tail()
    def parse_type_spec(self) -> None:
        tok = self.peek()
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int" , "float", "void"}:
            self.advance()
        else:
            raise ParserError("Syntax error")
    # CompoundStmt   → '{' LocalDeclList StmtList '}'
    def parse_compound_stmt(self) -> None:
        raise NotImplementedError("parse_compound_stmt not implemented yet")
    

    def parse_expr(self) -> None:
        """Expr → AssignExpr"""
        return self.parse_assign_expr()

    def parse_assign_expr(self) -> None:
        """AssignExpr → ID = AssignExpr | OrExpr"""
        # Check if this is an assignment: ID = AssignExpr
        if (self.peek() is not None and self.peek().type == TokenType.IDENTIFIER and
            self.peek(1) is not None and self.peek(1).value == '='):
            # Assignment: consume ID and = then parse right-hand side
            self.advance()  # consume ID
            self.advance()  # consume =
            return self.parse_assign_expr()
        else:
            # Not an assignment, parse as OrExpr
            return self.parse_or_expr()



    def parse_or_expr(self) -> None:
        """OrExpr → AndExpr OrExprTail"""
        self.parse_and_expr()
        self.parse_or_expr_tail()

    def parse_or_expr_tail(self) -> None:
        """OrExprTail → || AndExpr OrExprTail | ε"""
        tok = self.peek()
        if tok is not None and tok.value == '||':
            self.advance()  # consume ||
            self.parse_and_expr()
            self.parse_or_expr_tail()
        # else: epsilon case, just return

    def parse_and_expr(self) -> None:
        """AndExpr → RelExpr AndExprTail"""
        self.parse_rel_expr()
        self.parse_and_expr_tail()

    def parse_and_expr_tail(self) -> None:
        """AndExprTail → && RelExpr AndExprTail | ε"""
        tok = self.peek()
        if tok is not None and tok.value == '&&':
            self.advance()  # consume &&
            self.parse_rel_expr()
            self.parse_and_expr_tail()
        # else: epsilon case, just return

    def parse_rel_expr(self) -> None:
        """RelExpr → AddExpr RelOpTail"""
        self.parse_add_expr()
        self.parse_rel_op_tail()

    def parse_rel_op_tail(self) -> None:
        """RelOpTail → RelOp AddExpr | ε"""
        tok = self.peek()
        if tok is not None and tok.value in {'<', '<=', '>', '>=', '==', '!='}:
            self.advance()  # consume relational operator
            self.parse_add_expr()
        # else: epsilon case, just return

    def parse_add_expr(self) -> None:
        """AddExpr → Term AddExprTail"""
        self.parse_term()
        self.parse_add_expr_tail()

    def parse_add_expr_tail(self) -> None:
        """AddExprTail → + Term AddExprTail | - Term AddExprTail | ε"""
        tok = self.peek()
        if tok is not None and tok.value in {'+', '-'}:
            self.advance()  # consume + or -
            self.parse_term()
            self.parse_add_expr_tail()
        # else: epsilon case, just return

    def parse_term(self) -> None:
        """Term: parse primary expression (ID, number, parenthesized expr, function call, etc.)"""
        tok = self.peek()
        if tok is None:
            raise ParserError("Unexpected end of input in expression")
        
        if tok.type == TokenType.IDENTIFIER:
            self.advance()
            # Check for function call: ID (...)
            next_tok = self.peek()
            if next_tok is not None and next_tok.value == '(':
                self.advance()  # consume (
                self.parse_arg_list()
                self.expect(lexeme=')')
        elif tok.type == TokenType.NUMBER:
            self.advance()
        elif tok.value == '(':
            self.advance()  # consume (
            self.parse_expr()
            self.expect(lexeme=')')
        else:
            raise ParserError(f"Unexpected token in expression: {tok.value!r}")

    def parse_arg_list(self) -> None:
        """Parse function argument list (simplified)"""
        tok = self.peek()
        if tok is not None and tok.value == ')':
            # Empty argument list
            return
        # Parse first argument
        self.parse_expr()
        # Parse remaining arguments
        self.parse_arg_list_tail()

    def parse_arg_list_tail(self) -> None:
        """Parse remaining function arguments"""
        tok = self.peek()
        if tok is not None and tok.value == ',':
            self.advance()  # consume ,
            self.parse_expr()
            self.parse_arg_list_tail()   
    


   
             


               
        
       

    # Stmt, IfStmt, WhileStmt, ForStmt, ReturnStmt, Expr, etc.
    # Add more parse_* methods following your grammar as needed.
