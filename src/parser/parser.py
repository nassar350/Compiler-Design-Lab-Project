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

    def peek(self, n=0) -> Token | None:
        """Return the n-th non-trivia token from current position without consuming it.
        Handles lookahead that skips comments/whitespace/newlines.
        Returns None if there are fewer than n+1 non-trivia tokens remaining.
        """
        # Start at first non-trivia token from current position
        self._skip_trivia()
        idx = self.pos

        # If n == 0, just return current non-trivia token (if any)
        if n == 0:
            if idx < len(self.tokens):
                return self.tokens[idx]
            return None

        # Walk forward, counting only non-trivia tokens
        remaining = n
        while idx < len(self.tokens) and remaining > 0:
            idx += 1
            # Skip any trivia we encounter at the new index
            while idx < len(self.tokens) and self._is_trivia(self.tokens[idx]):
                idx += 1
            # We have advanced by one non-trivia token
            remaining -= 1

        # After advancing, return the token at idx if within bounds
        if idx < len(self.tokens):
            return self.tokens[idx]
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
            raise ParserError("Syntax Error")

        if type_ is not None and tok.type is not type_:
            raise ParserError("Syntax Error")

        if lexeme is not None and tok.value != lexeme:
            raise ParserError("Syntax Error")

        if advance:
            self.pos += 1
        return tok

    def expect_eof(self) -> None:
        """Ensure there are no remaining non-trivia tokens."""
        if self.peek() is not None:
            tok = self.peek()
            raise ParserError("Syntax Error")
    

    # --- Grammer Implementation ---

    # Program → DeclList EOF
    def parse_program(self) -> None:
        """Entry point: Program → DeclList (for now, just consume tokens).

        This is intentionally minimal. You will progressively replace the
        body with calls to the real grammar methods (parse_decl_list, etc.).
        """
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax Error")

        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int" , "float", "void"}:
            self.parse_decl_list()
            self.expect_eof()
        else :
            raise ParserError("Syntax Error")

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
            raise ParserError("Syntax Error")

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
            raise ParserError("Syntax Error")

    # VarDecl        → TypeSpec ID VarDeclTail ';'
    def parse_var_decl(self) -> None:
        tok = self.peek()
        if tok is not None and tok.type == TokenType.KEYWORD and tok.value in {"int", "void", "float"}:
            self.parse_type_spec()
            self.expect(TokenType.IDENTIFIER)
            self.parse_var_decl_tail()
            self.expect(lexeme=';')
        else:
            raise ParserError("Syntax Error")

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
            raise ParserError("Syntax Error")

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
            raise ParserError("Syntax Error")

    # CompoundStmt   → '{' LocalDeclList StmtList '}'
    def parse_compound_stmt(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax Error")
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
                raise ParserError("Syntax Error")
        else:
            raise ParserError("Syntax Error")

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
            raise ParserError("Syntax Error")

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
            raise ParserError("Syntax Error")

        self.expect(TokenType.KEYWORD, lexeme='while')
        self.expect(lexeme='(')
        self.parse_expr()
        self.expect(lexeme=')')
        self.parse_stmt()

    # ForStmt        → 'for' '(' ExprStmt ExprStmt ExprOpt ')' Stmt
    def parse_for_stmt(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax Error")

        self.expect(TokenType.KEYWORD, lexeme='for')
        self.expect(lexeme='(')
        self.parse_expr_stmt()
        self.parse_expr_stmt()
        self.parse_expr_opt()
        self.expect(lexeme=')')
        self.parse_stmt()

    # ReturnStmt     → 'return' ExprOpt ';'
    def parse_return_stmt(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax Error")

        self.expect(TokenType.KEYWORD, lexeme='return')
        self.parse_expr_opt()
        self.expect(lexeme=';')

    # ExprOpt       → Expr | ε
    def parse_expr_opt(self) -> None:
        tok = self.peek()
        if tok is not None and (tok.type == TokenType.IDENTIFIER 
                                or tok.type == TokenType.NUMERIC_CONSTANT
                                or tok.value == '('):
            self.parse_expr()
        else:
            return

    # Expr          → AssignExpr
    def parse_expr(self) -> None:
        """Expr → AssignExpr"""
        return self.parse_assign_expr()

    # AssignExpr    → ID = AssignExpr | OrExpr
    def parse_assign_expr(self) -> None:
        """AssignExpr → ID = AssignExpr | OrExpr"""
        # Check if this is an assignment: ID = AssignExpr
        tok = self.peek()

        if (tok is not None and tok.type == TokenType.IDENTIFIER and 
            self.peek(1) is not None and self.peek(1).value == '='):
            self.expect(type_=TokenType.IDENTIFIER)
        else:
            return self.parse_or_expr()
        last_pos = self.pos
        next_tok = self.peek()
        if next_tok is not None and next_tok.value == '=':
            self.expect(lexeme='=')
            return self.parse_assign_expr()
        else:
            self.pos = last_pos
            # Not an assignment, parse as OrExpr
            return self.parse_or_expr()

    # OrExpr        → AndExpr OrExprTail
    def parse_or_expr(self) -> None:
        """OrExpr → AndExpr OrExprTail"""
        self.parse_and_expr()
        self.parse_or_expr_tail()

    # OrExprTail    → || AndExpr OrExprTail | ε
    def parse_or_expr_tail(self) -> None:
        """OrExprTail → || AndExpr OrExprTail | ε"""
        tok = self.peek()
        if tok is not None and tok.value == '||':
            self.expect(lexeme='||')
            self.parse_and_expr()
            self.parse_or_expr_tail()
        # else: epsilon case, just return

    # AndExpr       → RelExpr AndExprTail
    def parse_and_expr(self) -> None:
        """AndExpr → RelExpr AndExprTail"""
        self.parse_rel_expr()
        self.parse_and_expr_tail()

    # AndExprTail   → && RelExpr AndExprTail | ε
    def parse_and_expr_tail(self) -> None:
        """AndExprTail → && RelExpr AndExprTail | ε"""
        tok = self.peek()
        if tok is not None and tok.value == '&&':
            self.expect(lexeme='&&')
            self.parse_rel_expr()
            self.parse_and_expr_tail()
        # else: epsilon case, just return

    # RelExpr       → AddExpr RelOpTail
    def parse_rel_expr(self) -> None:
        """RelExpr → AddExpr RelOpTail"""
        self.parse_add_expr()
        self.parse_rel_op_tail()

    # RelOpTail     → RelOp AddExpr | ε
    def parse_rel_op_tail(self) -> None:
        """RelOpTail → RelOp AddExpr | ε"""
        tok = self.peek()
        if tok is not None and tok.value in {'<', '<=', '>', '>=', '==', '!='}:
            self.parse_rel_op()
            self.parse_add_expr()
        # else: epsilon case, just return

    # RelOp         → '<' | '<=' | '>' | '>=' | '==' | '!='
    def parse_rel_op(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax Error")

        valid_ops = {'<', '<=', '>', '>=', '==', '!='}
        if tok.value in valid_ops:
            self.advance()
            return tok.value
        else:
            raise ParserError("Syntax Error")

    # AddExpr       → Term AddExprTail
    def parse_add_expr(self) -> None:
        """AddExpr → Term AddExprTail"""
        self.parse_term()
        self.parse_add_expr_tail()

    # AddExprTail   → + Term AddExprTail | - Term AddExprTail | ε
    def parse_add_expr_tail(self) -> None:
        """AddExprTail → + Term AddExprTail | - Term AddExprTail | ε"""
        tok = self.peek()
        if tok is not None and tok.value in {'+', '-'}:
            self.advance()  # consume + or -
            self.parse_term()
            self.parse_add_expr_tail()
        # else: epsilon case, just return

    # Term          → Factor TermTail
    def parse_term(self) -> None:
        self.parse_factor()
        self.parse_term_tail()
    
    # TermTail → * Factor TermTail | / Factor TermTail | ε
    def parse_term_tail(self) -> None:
        tok = self.peek()
        if tok is None:
            return  # ε case
        
        if tok.value == '*':
            self.expect(lexeme='*') 
        elif tok.value == '/':
            self.expect(lexeme='/')
        else:
            return  # ε case

        self.parse_factor()
        self.parse_term_tail()
        # else: ε case (no * or /)
    
    # Factor → ( Expr ) | ID FactorTail | Literal
    def parse_factor(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax Error")
        
        if tok.value == '(':
            self.expect(lexeme='(')
            self.parse_expr()  # parse the expression inside parentheses
            self.expect(lexeme=')')  # consume ')'
        elif tok.type == TokenType.IDENTIFIER:
            self.expect(type_=TokenType.IDENTIFIER)
            self.parse_factor_tail()  # check for function call
        elif tok.type == TokenType.NUMERIC_CONSTANT:
            self.parse_literal()
        else:
            raise ParserError("Syntax Error")
    
    # FactorTail → ( ArgList ) | ε
    def parse_factor_tail(self) -> None:
        tok = self.peek()
        if tok is None:
            return  # ε case (end of input)
        
        if tok.value == '(':
            self.expect(lexeme='(')  # consume '('
            self.parse_arg_list()  # parse the argument list
            self.expect(lexeme=')')  # consume ')'
        else:
            return
    
    # ArgList → Expr ArgListTail | ε
    def parse_arg_list(self) -> None:
        tok = self.peek()
        if tok is None or tok.value == ')':
            return  # ε case (empty argument list)

        self.parse_expr()  # parse first expression
        self.parse_arg_list_tail()  # parse remaining arguments
    
    # ArgListTail → , Expr ArgListTail | ε
    def parse_arg_list_tail(self) -> None:
        tok = self.peek()
        if tok is None or tok.value == ')':
            return  # ε case (no more arguments)
        
        if tok.value == ',':
            self.expect(lexeme=',')  # consume ','
            self.parse_expr()  # parse next expression
            self.parse_arg_list_tail()  # recursive call for more arguments
        else:
            raise ParserError("Syntax Error")
    
    # Literal → INT_CONST | FLOAT_CONST
    def parse_literal(self) -> None:
        tok = self.peek()
        if tok is None:
            raise ParserError("Syntax Error")
        
        self.expect(type_=TokenType.NUMERIC_CONSTANT)

    