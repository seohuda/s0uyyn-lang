from typing import List, Optional, Set
from src.lexer.token import Token, TokenType
from src.ast.nodes import (
    ASTNode,
    Program,
    BlockStmt,
    VariableDecl,
    Assignment,
    ExpressionStmt,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    Param,
    FunctionDecl,
    ClassDecl,
    Literal,
    Identifier,
    BinaryOp,
    UnaryOp,
    UpdateExpr,
    CallExpr,
    ArrayLiteral,
    IndexExpr,
    MemberExpr,
)
from src.errors import SyntaxError

# 타입 키워드 집합
TYPE_KEYWORDS: Set[TokenType] = {
    TokenType.KW_INT,
    TokenType.KW_LONG,
    TokenType.KW_FLOAT,
    TokenType.KW_CHAR,
    TokenType.KW_STRING,
    TokenType.KW_BOOL,
    TokenType.KW_ARRAY,
    TokenType.KW_LIST,
    TokenType.KW_STACK,
}

# 연산자 우선순위 상수
PREC_NONE = 0
PREC_ASSIGN = 1
PREC_OR = 2
PREC_AND = 3
PREC_BIT_OR = 4
PREC_BIT_XOR = 5
PREC_BIT_AND = 6
PREC_EQUALITY = 7
PREC_COMPARISON = 8
PREC_BITSHIFT = 9
PREC_TERM = 10
PREC_FACTOR = 11
PREC_POWER = 12
PREC_UNARY = 13
PREC_POSTFIX = 14

TOKEN_PRECEDENCE = {
    TokenType.EQ: PREC_ASSIGN,
    TokenType.OR_OR: PREC_OR,
    TokenType.AND_AND: PREC_AND,
    TokenType.PIPE: PREC_BIT_OR,
    TokenType.CARET: PREC_BIT_XOR,
    TokenType.AMP: PREC_BIT_AND,
    TokenType.EQ_EQ: PREC_EQUALITY,
    TokenType.BANG_EQ: PREC_EQUALITY,
    TokenType.LESS: PREC_COMPARISON,
    TokenType.LESS_EQ: PREC_COMPARISON,
    TokenType.GREATER: PREC_COMPARISON,
    TokenType.GREATER_EQ: PREC_COMPARISON,
    TokenType.LSHIFT: PREC_BITSHIFT,
    TokenType.RSHIFT: PREC_BITSHIFT,
    TokenType.PLUS: PREC_TERM,
    TokenType.MINUS: PREC_TERM,
    TokenType.STAR: PREC_FACTOR,
    TokenType.SLASH: PREC_FACTOR,
    TokenType.PERCENT: PREC_FACTOR,
    TokenType.POWER: PREC_POWER,
}


class Parser:
    """서윤랭 구문 분석기 (Parser)"""

    def __init__(self, tokens: List[Token], source_code: Optional[str] = None):
        self.tokens: List[Token] = tokens
        self.pos: int = 0
        self.source_code: Optional[str] = source_code

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]  # EOF token

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _advance(self) -> Token:
        token = self._peek()
        if not self._is_at_end():
            self.pos += 1
        return token

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type == token_type

    def _match(self, *token_types: TokenType) -> bool:
        for tt in token_types:
            if self._check(tt):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, error_message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        token = self._peek()
        raise SyntaxError(
            f"{error_message} (발견된 토큰: '{token.lexeme}')",
            line=token.line,
            column=token.column,
            source_code=self.source_code,
        )

    def parse(self) -> Program:
        statements: List[ASTNode] = []
        start_token = self._peek()

        while not self._is_at_end():
            stmt = self._parse_declaration_or_statement()
            if stmt is not None:
                statements.append(stmt)

        return Program(
            line=start_token.line,
            column=start_token.column,
            statements=statements,
        )

    def _parse_declaration_or_statement(self) -> ASTNode:
        token = self._peek()

        # 1. 클래스 선언: 1학년2반 Name { ... }
        if token.type == TokenType.KW_CLASS:
            return self._parse_class_declaration()

        # 2. 함수 선언: 이걸진짜만들었어요? ...
        if token.type == TokenType.KW_FUNCTION:
            return self._parse_function_declaration()

        # 3. 상수 선언: 당당해지세요. type name = expr;
        if token.type == TokenType.KW_CONST:
            return self._parse_const_declaration()

        # 4. 변수 선언: type name [= expr];
        if self._is_type_token(token):
            return self._parse_variable_declaration()

        # 사용자 정의 클래스 타입 변수 선언 검사: Identifier Identifier [= expr];
        if token.type == TokenType.IDENTIFIER and self._peek(1).type == TokenType.IDENTIFIER:
            return self._parse_variable_declaration()

        return self._parse_statement()

    def _is_type_token(self, token: Token) -> bool:
        return token.type in TYPE_KEYWORDS

    def _parse_class_declaration(self) -> ClassDecl:
        kw = self._consume(TokenType.KW_CLASS, "'1학년2반' 키워드가 필요합니다.")
        name_token = self._consume(TokenType.IDENTIFIER, "클래스 이름이 필요합니다.")
        self._consume(TokenType.LBRACE, "클래스 본문 시작을 위한 '{'가 필요합니다.")

        fields: List[VariableDecl] = []
        methods: List[FunctionDecl] = []

        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            if self._check(TokenType.KW_FUNCTION):
                methods.append(self._parse_function_declaration())
            elif self._is_type_token(self._peek()) or (
                self._check(TokenType.IDENTIFIER) and self._peek(1).type == TokenType.IDENTIFIER
            ):
                fields.append(self._parse_variable_declaration())
            else:
                tok = self._peek()
                raise SyntaxError(
                    f"클래스 내부에는 필드 또는 메서드 선언만 올 수 있습니다: '{tok.lexeme}'",
                    line=tok.line,
                    column=tok.column,
                    source_code=self.source_code,
                )

        self._consume(TokenType.RBRACE, "클래스 본문 종료를 위한 '}'가 필요합니다.")
        return ClassDecl(
            line=kw.line,
            column=kw.column,
            name=name_token.lexeme,
            fields=fields,
            methods=methods,
        )

    def _parse_function_declaration(self) -> FunctionDecl:
        kw = self._consume(TokenType.KW_FUNCTION, "'이걸진짜만들었어요?' 키워드가 필요합니다.")

        return_type: Optional[str] = None
        # 선택적 반환 타입 검사
        if self._is_type_token(self._peek()) or (
            self._check(TokenType.IDENTIFIER) and self._peek(1).type == TokenType.IDENTIFIER
        ):
            return_type = self._advance().lexeme

        name_token = self._consume(TokenType.IDENTIFIER, "함수 이름이 필요합니다.")
        self._consume(TokenType.LPAREN, "함수 매개변수 목록을 위한 '('가 필요합니다.")

        params: List[Param] = []
        if not self._check(TokenType.RPAREN):
            while True:
                param_type: Optional[str] = None
                if self._is_type_token(self._peek()) or (
                    self._check(TokenType.IDENTIFIER) and self._peek(1).type == TokenType.IDENTIFIER
                ):
                    param_type = self._advance().lexeme

                param_name = self._consume(TokenType.IDENTIFIER, "매개변수 이름이 필요합니다.").lexeme
                params.append(Param(name=param_name, type_name=param_type))

                if not self._match(TokenType.COMMA):
                    break

        self._consume(TokenType.RPAREN, "매개변수 목록 종료를 위한 ')'가 필요합니다.")
        body = self._parse_block_statement()

        return FunctionDecl(
            line=kw.line,
            column=kw.column,
            name=name_token.lexeme,
            params=params,
            body=body,
            return_type=return_type,
        )

    def _parse_const_declaration(self) -> VariableDecl:
        kw = self._consume(TokenType.KW_CONST, "'당당해지세요.' 키워드가 필요합니다.")

        type_token = self._peek()
        if not (self._is_type_token(type_token) or type_token.type == TokenType.IDENTIFIER):
            raise SyntaxError(
                f"상수 선언에는 타입이 필요합니다: '{type_token.lexeme}'",
                line=type_token.line,
                column=type_token.column,
                source_code=self.source_code,
            )
        self._advance()

        name_token = self._consume(TokenType.IDENTIFIER, "상수 이름이 필요합니다.")
        self._consume(TokenType.EQ, "상수 선언에는 초기화 값 '='이 필수입니다.")
        init_expr = self._parse_expression()
        self._consume(TokenType.SEMICOLON, "문장 종료를 위한 ';'가 필요합니다.")

        return VariableDecl(
            line=kw.line,
            column=kw.column,
            type_name=type_token.lexeme,
            name=name_token.lexeme,
            init=init_expr,
            is_const=True,
        )

    def _parse_variable_declaration(self) -> VariableDecl:
        type_token = self._advance()
        name_token = self._consume(TokenType.IDENTIFIER, "변수 이름이 필요합니다.")

        init_expr: Optional[ASTNode] = None
        if self._match(TokenType.EQ):
            init_expr = self._parse_expression()

        self._consume(TokenType.SEMICOLON, "문장 종료를 위한 ';'가 필요합니다.")
        return VariableDecl(
            line=type_token.line,
            column=type_token.column,
            type_name=type_token.lexeme,
            name=name_token.lexeme,
            init=init_expr,
            is_const=False,
        )

    def _parse_statement(self) -> ASTNode:
        token = self._peek()

        # 블록: { ... }
        if token.type == TokenType.LBRACE:
            return self._parse_block_statement()

        # 조건문: 왜요ㅗ ( ... ) { ... }
        if token.type == TokenType.KW_IF:
            return self._parse_if_statement()

        # 반복문: whale ( ... ) { ... }
        if token.type == TokenType.KW_WHILE:
            return self._parse_while_statement()

        # 반복문: 너므많아ㅡㅡㅅ ( ... ) { ... }
        if token.type == TokenType.KW_FOR:
            return self._parse_for_statement()

        # break: 말걸지마세요;
        if token.type == TokenType.KW_BREAK:
            self._advance()
            self._consume(TokenType.SEMICOLON, "'말걸지마세요' 뒤에 ';'가 필요합니다.")
            return BreakStmt(line=token.line, column=token.column)

        # continue: 꺼져ㅗ;
        if token.type == TokenType.KW_CONTINUE:
            self._advance()
            self._consume(TokenType.SEMICOLON, "'꺼져ㅗ' 뒤에 ';'가 필요합니다.")
            return ContinueStmt(line=token.line, column=token.column)

        # return: 울산행KTX [expr];
        if token.type == TokenType.KW_RETURN:
            return self._parse_return_statement()

        # 표현식 문장: expr;
        expr = self._parse_expression()
        self._consume(TokenType.SEMICOLON, "문장 종료를 위한 ';'가 필요합니다.")
        return ExpressionStmt(line=expr.line, column=expr.column, expr=expr)

    def _parse_block_statement(self) -> BlockStmt:
        lbrace = self._consume(TokenType.LBRACE, "'{'가 필요합니다.")
        statements: List[ASTNode] = []

        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            statements.append(self._parse_declaration_or_statement())

        self._consume(TokenType.RBRACE, "'}'가 필요합니다.")
        return BlockStmt(line=lbrace.line, column=lbrace.column, statements=statements)

    def _parse_if_statement(self) -> IfStmt:
        kw = self._consume(TokenType.KW_IF, "'왜요ㅗ'가 필요합니다.")
        self._consume(TokenType.LPAREN, "조건식을 감싸는 '('가 필요합니다.")
        condition = self._parse_expression()
        self._consume(TokenType.RPAREN, "조건식 종료를 위한 ')'가 필요합니다.")

        then_branch = self._parse_block_or_statement()
        else_branch: Optional[ASTNode] = None

        if self._match(TokenType.KW_ELSE):
            if self._check(TokenType.KW_IF):
                else_branch = self._parse_if_statement()
            else:
                else_branch = self._parse_block_or_statement()

        return IfStmt(
            line=kw.line,
            column=kw.column,
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch,
        )

    def _parse_block_or_statement(self) -> ASTNode:
        if self._check(TokenType.LBRACE):
            return self._parse_block_statement()
        return self._parse_statement()

    def _parse_while_statement(self) -> WhileStmt:
        kw = self._consume(TokenType.KW_WHILE, "'whale'이 필요합니다.")
        self._consume(TokenType.LPAREN, "조건식을 감싸는 '('가 필요합니다.")
        condition = self._parse_expression()
        self._consume(TokenType.RPAREN, "조건식 종료를 위한 ')'가 필요합니다.")
        body = self._parse_block_or_statement()
        return WhileStmt(line=kw.line, column=kw.column, condition=condition, body=body)

    def _parse_for_statement(self) -> ForStmt:
        kw = self._consume(TokenType.KW_FOR, "'너므많아ㅡㅡㅅ'이 필요합니다.")
        self._consume(TokenType.LPAREN, "'('가 필요합니다.")

        # 1. init
        init_node: Optional[ASTNode] = None
        if not self._check(TokenType.SEMICOLON):
            if self._is_type_token(self._peek()) or (
                self._check(TokenType.IDENTIFIER) and self._peek(1).type == TokenType.IDENTIFIER
            ):
                init_node = self._parse_variable_declaration()
            else:
                expr = self._parse_expression()
                self._consume(TokenType.SEMICOLON, "초기화식 뒤에 ';'가 필요합니다.")
                init_node = ExpressionStmt(line=expr.line, column=expr.column, expr=expr)
        else:
            self._consume(TokenType.SEMICOLON, "';'가 필요합니다.")

        # 2. condition
        cond_node: Optional[ASTNode] = None
        if not self._check(TokenType.SEMICOLON):
            cond_node = self._parse_expression()
        self._consume(TokenType.SEMICOLON, "조건식 뒤에 ';'가 필요합니다.")

        # 3. update
        update_node: Optional[ASTNode] = None
        if not self._check(TokenType.RPAREN):
            update_node = self._parse_expression()
        self._consume(TokenType.RPAREN, "')'가 필요합니다.")

        body = self._parse_block_or_statement()
        return ForStmt(
            line=kw.line,
            column=kw.column,
            init=init_node,
            condition=cond_node,
            update=update_node,
            body=body,
        )

    def _parse_return_statement(self) -> ReturnStmt:
        kw = self._consume(TokenType.KW_RETURN, "'울산행KTX'가 필요합니다.")
        value_node: Optional[ASTNode] = None
        if not self._check(TokenType.SEMICOLON):
            value_node = self._parse_expression()
        self._consume(TokenType.SEMICOLON, "'울산행KTX' 문장 종료를 위한 ';'가 필요합니다.")
        return ReturnStmt(line=kw.line, column=kw.column, value=value_node)

    # Pratt / Precedence Climbing 표현식 파서
    def _parse_expression(self, min_prec: int = PREC_NONE) -> ASTNode:
        left = self._parse_prefix()

        while True:
            peek_tok = self._peek()

            # Postfix 연산자 (++, --)
            if peek_tok.type in (TokenType.PLUS_PLUS, TokenType.MINUS_MINUS):
                if min_prec >= PREC_POSTFIX:
                    break
                op_tok = self._advance()
                left = UpdateExpr(
                    line=left.line,
                    column=left.column,
                    target=left,
                    op=op_tok.lexeme,
                    is_prefix=False,
                )
                continue

            # 함수 호출: ( args )
            if peek_tok.type == TokenType.LPAREN:
                if min_prec >= PREC_POSTFIX:
                    break
                left = self._parse_call_expression(left)
                continue

            # 배열/문자열 인덱싱: [ index ]
            if peek_tok.type == TokenType.LBRACKET:
                if min_prec >= PREC_POSTFIX:
                    break
                self._advance()  # '['
                index_expr = self._parse_expression()
                self._consume(TokenType.RBRACKET, "인덱스 종료를 위한 ']'가 필요합니다.")
                left = IndexExpr(
                    line=left.line,
                    column=left.column,
                    target=left,
                    index=index_expr,
                )
                continue

            # 멤버 접근: . member
            if peek_tok.type == TokenType.DOT:
                if min_prec >= PREC_POSTFIX:
                    break
                self._advance()  # '.'
                member_tok = self._consume(TokenType.IDENTIFIER, "멤버 이름이 필요합니다.")
                left = MemberExpr(
                    line=left.line,
                    column=left.column,
                    target=left,
                    member=member_tok.lexeme,
                )
                continue

            # 할당 연산자: = (우결합)
            if peek_tok.type == TokenType.EQ:
                if min_prec > PREC_ASSIGN:
                    break
                eq_tok = self._advance()
                # 할당 대상 유효성 검사 (Identifier, IndexExpr, MemberExpr)
                if not isinstance(left, (Identifier, IndexExpr, MemberExpr)):
                    raise SyntaxError(
                        "잘못된 할당 대상입니다.",
                        line=left.line,
                        column=left.column,
                        source_code=self.source_code,
                    )
                right = self._parse_expression(PREC_ASSIGN)
                left = Assignment(
                    line=left.line,
                    column=left.column,
                    target=left,
                    value=right,
                )
                continue

            # 이항 연산자
            prec = TOKEN_PRECEDENCE.get(peek_tok.type, PREC_NONE)
            if prec < min_prec or prec == PREC_NONE:
                break

            op_tok = self._advance()
            # 거듭제곱(**)은 우결합이므로 동일 우선순위 허용, 그 외는 좌결합
            next_min_prec = prec if op_tok.type == TokenType.POWER else prec + 1
            right = self._parse_expression(next_min_prec)
            left = BinaryOp(
                line=left.line,
                column=left.column,
                left=left,
                op=op_tok.lexeme,
                right=right,
            )

        return left

    def _parse_prefix(self) -> ASTNode:
        token = self._peek()

        # 전위 단항 연산자: +, -, !, ++, --
        if token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.BANG):
            self._advance()
            operand = self._parse_expression(PREC_UNARY)
            return UnaryOp(
                line=token.line,
                column=token.column,
                op=token.lexeme,
                operand=operand,
                is_prefix=True,
            )

        if token.type in (TokenType.PLUS_PLUS, TokenType.MINUS_MINUS):
            self._advance()
            operand = self._parse_expression(PREC_UNARY)
            if not isinstance(operand, (Identifier, IndexExpr, MemberExpr)):
                raise SyntaxError(
                    "증감 연산자의 대상은 변수 또는 인덱스여야 합니다.",
                    line=token.line,
                    column=token.column,
                    source_code=self.source_code,
                )
            return UpdateExpr(
                line=token.line,
                column=token.column,
                target=operand,
                op=token.lexeme,
                is_prefix=True,
            )

        # 괄호 표현식: ( expr )
        if token.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN, "')'가 필요합니다.")
            return expr

        # 배열 리터럴: [ e1, e2, ... ]
        if token.type == TokenType.LBRACKET:
            return self._parse_array_literal()

        # 리터럴들
        if token.type == TokenType.INT_LITERAL:
            self._advance()
            return Literal(
                line=token.line,
                column=token.column,
                value=token.value,
                raw=token.lexeme,
                type_hint="int",
            )

        if token.type == TokenType.FLOAT_LITERAL:
            self._advance()
            return Literal(
                line=token.line,
                column=token.column,
                value=token.value,
                raw=token.lexeme,
                type_hint="float",
            )

        if token.type == TokenType.STRING_LITERAL:
            self._advance()
            return Literal(
                line=token.line,
                column=token.column,
                value=token.value,
                raw=token.lexeme,
                type_hint="string",
            )

        if token.type == TokenType.CHAR_LITERAL:
            self._advance()
            return Literal(
                line=token.line,
                column=token.column,
                value=token.value,
                raw=token.lexeme,
                type_hint="char",
            )

        if token.type == TokenType.KW_TRUE:
            self._advance()
            return Literal(
                line=token.line,
                column=token.column,
                value=True,
                raw=token.lexeme,
                type_hint="bool",
            )

        if token.type == TokenType.KW_FALSE:
            self._advance()
            return Literal(
                line=token.line,
                column=token.column,
                value=False,
                raw=token.lexeme,
                type_hint="bool",
            )

        if token.type == TokenType.KW_NULL:
            self._advance()
            return Literal(
                line=token.line,
                column=token.column,
                value=None,
                raw=token.lexeme,
                type_hint="null",
            )

        # 내장 함수 키워드(오쫄티비, 게히야) 및 일반 식별자
        if token.type in (TokenType.IDENTIFIER, TokenType.KW_PRINT, TokenType.KW_INPUT):
            self._advance()
            return Identifier(line=token.line, column=token.column, name=token.lexeme)

        raise SyntaxError(
            f"예상하지 못한 토큰입니다: '{token.lexeme}'",
            line=token.line,
            column=token.column,
            source_code=self.source_code,
        )

    def _parse_call_expression(self, callee: ASTNode) -> CallExpr:
        lparen = self._consume(TokenType.LPAREN, "'('가 필요합니다.")
        args: List[ASTNode] = []
        if not self._check(TokenType.RPAREN):
            while True:
                args.append(self._parse_expression())
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RPAREN, "함수 호출 종료를 위한 ')'가 필요합니다.")
        return CallExpr(line=lparen.line, column=lparen.column, callee=callee, args=args)

    def _parse_array_literal(self) -> ArrayLiteral:
        lbracket = self._consume(TokenType.LBRACKET, "'['가 필요합니다.")
        elements: List[ASTNode] = []
        if not self._check(TokenType.RBRACKET):
            while True:
                elements.append(self._parse_expression())
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RBRACKET, "']'가 필요합니다.")
        return ArrayLiteral(line=lbracket.line, column=lbracket.column, elements=elements)
