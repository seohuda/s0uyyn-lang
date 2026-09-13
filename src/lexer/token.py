from enum import Enum, auto
from dataclasses import dataclass
from typing import Any


class TokenType(Enum):
    # Special
    EOF = auto()

    # Literals
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    CHAR_LITERAL = auto()

    # Identifier
    IDENTIFIER = auto()

    # Keywords - Types
    KW_INT = auto()       # e의2승
    KW_LONG = auto()      # 울산큰고래
    KW_FLOAT = auto()     # 고래
    KW_CHAR = auto()      # 오?
    KW_STRING = auto()    # 서울말
    KW_BOOL = auto()      # 아진짜ㅏ요

    # Keywords - Values
    KW_TRUE = auto()      # 짘자
    KW_FALSE = auto()     # 안히
    KW_NULL = auto()      # 남친

    # Keywords - Collections
    KW_ARRAY = auto()     # 사투링고
    KW_LIST = auto()      # 블루베리스무디레시피
    KW_STACK = auto()     # 울산고래탑

    # Keywords - IO
    KW_PRINT = auto()     # 오쫄티비
    KW_INPUT = auto()     # 게히야

    # Keywords - Control Flow
    KW_IF = auto()        # 왜요ㅗ
    KW_ELSE = auto()      # 실어요
    KW_WHILE = auto()     # whale
    KW_FOR = auto()       # 너므많아ㅡㅡㅅ
    KW_BREAK = auto()     # 말걸지마세요
    KW_CONTINUE = auto()  # 꺼져ㅗ
    KW_RETURN = auto()    # 울산행KTX

    # Keywords - Declarations
    KW_FUNCTION = auto()  # 이걸진짜만들었어요?
    KW_CONST = auto()     # 당당해지세요.
    KW_CLASS = auto()     # 1학년2반

    # Operators
    PLUS = auto()         # +
    MINUS = auto()        # -
    STAR = auto()         # *
    SLASH = auto()        # /
    PERCENT = auto()      # %
    POWER = auto()        # **

    PLUS_PLUS = auto()    # ++
    MINUS_MINUS = auto()  # --

    EQ = auto()           # =
    EQ_EQ = auto()        # ==
    BANG_EQ = auto()      # !=
    LESS = auto()         # <
    GREATER = auto()      # >
    LESS_EQ = auto()      # <=
    GREATER_EQ = auto()   # >=

    AND_AND = auto()      # &&
    OR_OR = auto()        # ||
    BANG = auto()         # !

    AMP = auto()          # &
    PIPE = auto()         # |
    CARET = auto()        # ^
    LSHIFT = auto()       # <<
    RSHIFT = auto()       # >>

    # Delimiters
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    SEMICOLON = auto()    # ;
    COMMA = auto()        # ,
    DOT = auto()          # .
    COLON = auto()        # :


# 서윤랭 확정 키워드 테이블
KEYWORDS: dict[str, TokenType] = {
    "e의2승": TokenType.KW_INT,
    "울산큰고래": TokenType.KW_LONG,
    "고래": TokenType.KW_FLOAT,
    "오?": TokenType.KW_CHAR,
    "서울말": TokenType.KW_STRING,
    "아진짜ㅏ요": TokenType.KW_BOOL,
    "짘자": TokenType.KW_TRUE,
    "안히": TokenType.KW_FALSE,
    "남친": TokenType.KW_NULL,
    "사투링고": TokenType.KW_ARRAY,
    "블루베리스무디레시피": TokenType.KW_LIST,
    "울산고래탑": TokenType.KW_STACK,
    "오쫄티비": TokenType.KW_PRINT,
    "게히야": TokenType.KW_INPUT,
    "왜요ㅗ": TokenType.KW_IF,
    "실어요": TokenType.KW_ELSE,
    "whale": TokenType.KW_WHILE,
    "너므많아ㅡㅡㅅ": TokenType.KW_FOR,
    "말걸지마세요": TokenType.KW_BREAK,
    "꺼져ㅗ": TokenType.KW_CONTINUE,
    "울산행KTX": TokenType.KW_RETURN,
    "이걸진짜만들었어요?": TokenType.KW_FUNCTION,
    "당당해지세요.": TokenType.KW_CONST,
    "1학년2반": TokenType.KW_CLASS,
}


@dataclass
class Token:
    type: TokenType
    lexeme: str
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, lexeme={self.lexeme!r}, value={self.value!r}, line={self.line}, col={self.column})"
