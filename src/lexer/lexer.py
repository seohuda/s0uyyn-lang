from typing import List, Optional
from src.lexer.token import Token, TokenType, KEYWORDS
from src.errors import LexerError


class Lexer:
    """서윤랭 어휘 분석기 (Lexer)"""

    def __init__(self, source: str):
        self.source: str = source
        self.length: int = len(source)
        self.pos: int = 0
        self.line: int = 1
        self.col: int = 1

        # 키워드 매칭을 위해 길이기준 내림차순 정렬 (Longest-match)
        self._sorted_keywords = sorted(KEYWORDS.keys(), key=len, reverse=True)

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx < self.length:
            return self.source[idx]
        return ""

    def _advance(self) -> str:
        if self.pos >= self.length:
            return ""
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _advance_n(self, n: int) -> None:
        for _ in range(n):
            self._advance()

    def _is_ident_start(self, ch: str) -> bool:
        if not ch:
            return False
        return ch.isalpha() or ch == "_"

    def _is_ident_part(self, ch: str) -> bool:
        if not ch:
            return False
        return ch.isalnum() or ch == "_"

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.pos < self.length:
            ch = self._peek()

            # 1. 공백 문자 스킵
            if ch.isspace():
                self._advance()
                continue

            start_line = self.line
            start_col = self.col
            start_pos = self.pos

            # 2. 주석: !울산말 ... 울산말!
            if self.source.startswith("!울산말", self.pos):
                self._skip_comment(start_line, start_col)
                continue

            # 3. 문자열 리터럴 ("...")
            if ch == '"':
                tokens.append(self._read_string(start_line, start_col))
                continue

            # 4. 문자 리터럴 ('...')
            if ch == "'":
                tokens.append(self._read_char(start_line, start_col))
                continue

            # 5. 서윤랭 확정 키워드 (Longest Match)
            # 특수 키워드('1학년2반', '오?', '당당해지세요.', '왜요ㅗ', '너므많아ㅡㅡㅅ' 등)를 우선 판별
            keyword_token = self._try_read_keyword(start_line, start_col)
            if keyword_token is not None:
                tokens.append(keyword_token)
                continue

            # 6. 숫자 리터럴 (정수 / 실수)
            if ch.isdigit():
                tokens.append(self._read_number(start_line, start_col))
                continue

            # 7. 식별자 (Identifier)
            if self._is_ident_start(ch):
                tokens.append(self._read_identifier(start_line, start_col))
                continue

            # 8. 다중 문자 연산자 (2문자 이상)
            two_chars = self._peek() + self._peek(1)
            if two_chars == "++":
                self._advance_n(2)
                tokens.append(Token(TokenType.PLUS_PLUS, "++", "++", start_line, start_col))
                continue
            if two_chars == "--":
                self._advance_n(2)
                tokens.append(Token(TokenType.MINUS_MINUS, "--", "--", start_line, start_col))
                continue
            if two_chars == "**":
                self._advance_n(2)
                tokens.append(Token(TokenType.POWER, "**", "**", start_line, start_col))
                continue
            if two_chars == "==":
                self._advance_n(2)
                tokens.append(Token(TokenType.EQ_EQ, "==", "==", start_line, start_col))
                continue
            if two_chars == "!=":
                self._advance_n(2)
                tokens.append(Token(TokenType.BANG_EQ, "!=", "!=", start_line, start_col))
                continue
            if two_chars == "<=":
                self._advance_n(2)
                tokens.append(Token(TokenType.LESS_EQ, "<=", "<=", start_line, start_col))
                continue
            if two_chars == ">=":
                self._advance_n(2)
                tokens.append(Token(TokenType.GREATER_EQ, ">=", ">=", start_line, start_col))
                continue
            if two_chars == "&&":
                self._advance_n(2)
                tokens.append(Token(TokenType.AND_AND, "&&", "&&", start_line, start_col))
                continue
            if two_chars == "||":
                self._advance_n(2)
                tokens.append(Token(TokenType.OR_OR, "||", "||", start_line, start_col))
                continue
            if two_chars == "<<":
                self._advance_n(2)
                tokens.append(Token(TokenType.LSHIFT, "<<", "<<", start_line, start_col))
                continue
            if two_chars == ">>":
                self._advance_n(2)
                tokens.append(Token(TokenType.RSHIFT, ">>", ">>", start_line, start_col))
                continue

            # 9. 단일 문자 연산자 및 구분 기호
            single_char_map = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.STAR,
                "/": TokenType.SLASH,
                "%": TokenType.PERCENT,
                "=": TokenType.EQ,
                "<": TokenType.LESS,
                ">": TokenType.GREATER,
                "!": TokenType.BANG,
                "&": TokenType.AMP,
                "|": TokenType.PIPE,
                "^": TokenType.CARET,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
                "[": TokenType.LBRACKET,
                "]": TokenType.RBRACKET,
                ";": TokenType.SEMICOLON,
                ",": TokenType.COMMA,
                ".": TokenType.DOT,
                ":": TokenType.COLON,
            }

            if ch in single_char_map:
                self._advance()
                tokens.append(Token(single_char_map[ch], ch, ch, start_line, start_col))
                continue

            # 인식할 수 없는 문자
            unknown_char = self._advance()
            raise LexerError(
                f"인식할 수 없는 문자입니다: '{unknown_char}'",
                line=start_line,
                column=start_col,
                source_code=self.source,
            )

        tokens.append(Token(TokenType.EOF, "", None, self.line, self.col))
        return tokens

    def _skip_comment(self, start_line: int, start_col: int) -> None:
        """!울산말 ... 울산말! 주석 건너뛰기"""
        self._advance_n(len("!울산말"))
        closing = "울산말!"

        while self.pos < self.length:
            if self.source.startswith(closing, self.pos):
                self._advance_n(len(closing))
                return
            self._advance()

        raise LexerError(
            "닫히지 않은 주석입니다. ('울산말!' 필요)",
            line=start_line,
            column=start_col,
            source_code=self.source,
        )

    def _try_read_keyword(self, start_line: int, start_col: int) -> Optional[Token]:
        for kw in self._sorted_keywords:
            if self.source.startswith(kw, self.pos):
                # 키워드의 마지막 문자가 식별자 문자(알파벳, 한글, 숫자)인 경우,
                # 뒤에 바로 식별자 문자가 이어지면 키워드로 판정하지 않음 (예: 고래고기)
                last_char = kw[-1]
                next_pos = self.pos + len(kw)
                if self._is_ident_part(last_char) and next_pos < self.length:
                    next_char = self.source[next_pos]
                    if self._is_ident_part(next_char):
                        continue

                self._advance_n(len(kw))
                return Token(KEYWORDS[kw], kw, kw, start_line, start_col)
        return None

    def _read_string(self, start_line: int, start_col: int) -> Token:
        self._advance()  # 여는 큰따옴표 건너뛰기
        chars: List[str] = []

        while self.pos < self.length:
            ch = self._peek()
            if ch == '"':
                self._advance()
                value = "".join(chars)
                return Token(TokenType.STRING_LITERAL, f'"{value}"', value, start_line, start_col)
            elif ch == "\\":
                self._advance()
                escaped = self._peek()
                if escaped == "n":
                    chars.append("\n")
                elif escaped == "t":
                    chars.append("\t")
                elif escaped == "r":
                    chars.append("\r")
                elif escaped == '"':
                    chars.append('"')
                elif escaped == "\\":
                    chars.append("\\")
                else:
                    chars.append(escaped)
                self._advance()
            elif ch == "\n":
                raise LexerError(
                    "문자열 리터럴 내부에서 개행을 허용하지 않습니다.",
                    line=self.line,
                    column=self.col,
                    source_code=self.source,
                )
            else:
                chars.append(self._advance())

        raise LexerError(
            "닫히지 않은 문자열 리터럴입니다.",
            line=start_line,
            column=start_col,
            source_code=self.source,
        )

    def _read_char(self, start_line: int, start_col: int) -> Token:
        self._advance()  # 여는 작은따옴표 건너뛰기
        ch = self._peek()
        val = ""
        if ch == "\\":
            self._advance()
            escaped = self._peek()
            if escaped == "n":
                val = "\n"
            elif escaped == "t":
                val = "\t"
            elif escaped == "r":
                val = "\r"
            elif escaped == "'":
                val = "'"
            elif escaped == "\\":
                val = "\\"
            else:
                val = escaped
            self._advance()
        elif ch == "'":
            raise LexerError(
                "빈 문자 리터럴입니다.",
                line=start_line,
                column=start_col,
                source_code=self.source,
            )
        elif self.pos < self.length:
            val = self._advance()
        else:
            raise LexerError(
                "닫히지 않은 문자 리터럴입니다.",
                line=start_line,
                column=start_col,
                source_code=self.source,
            )

        if self._peek() != "'":
            raise LexerError(
                "문자 리터럴은 정확히 하나의 문자여야 합니다.",
                line=start_line,
                column=start_col,
                source_code=self.source,
            )
        self._advance()  # 닫는 작은따옴표 건너뛰기
        return Token(TokenType.CHAR_LITERAL, f"'{val}'", val, start_line, start_col)

    def _read_number(self, start_line: int, start_col: int) -> Token:
        start_pos = self.pos
        while self.pos < self.length and self._peek().isdigit():
            self._advance()

        # 소수점 확인 (다음 문자가 숫자여야 실수로 처리)
        if self._peek() == "." and self._peek(1).isdigit():
            self._advance()  # '.' 소비
            while self.pos < self.length and self._peek().isdigit():
                self._advance()
            raw = self.source[start_pos : self.pos]
            return Token(TokenType.FLOAT_LITERAL, raw, float(raw), start_line, start_col)

        raw = self.source[start_pos : self.pos]
        return Token(TokenType.INT_LITERAL, raw, int(raw), start_line, start_col)

    def _read_identifier(self, start_line: int, start_col: int) -> Token:
        start_pos = self.pos
        while self.pos < self.length and self._is_ident_part(self._peek()):
            self._advance()
        raw = self.source[start_pos : self.pos]
        return Token(TokenType.IDENTIFIER, raw, raw, start_line, start_col)
