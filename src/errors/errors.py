from dataclasses import dataclass
from typing import Optional


@dataclass
class SourceLocation:
    line: int
    column: int
    source_code: Optional[str] = None


class SeoyunError(Exception):
    """서윤랭 기본 에러 클래스"""

    def __init__(
        self,
        message: str,
        line: int = 1,
        column: int = 1,
        source_code: Optional[str] = None,
        source_line: Optional[str] = None,
    ):
        self.message = message
        self.line = line
        self.column = column
        self.source_code = source_code
        self.source_line = source_line
        super().__init__(self.format_message())

    def _get_snippet(self) -> Optional[str]:
        if self.source_line is not None:
            return self.source_line
        if self.source_code is not None:
            lines = self.source_code.splitlines()
            if 0 < self.line <= len(lines):
                return lines[self.line - 1]
        return None

    def format_message(self) -> str:
        error_name = self.__class__.__name__
        snippet = self._get_snippet()

        header = f"서윤랭 {error_name}\n\n{self.line}번째 줄 {self.column}번째 문자 근처: {self.message}"
        if snippet is not None:
            # 한글 등 유니코드 전각 문자 고려: 출력 너비에 맞게 캐럿 위치 조정
            caret_spaces = ""
            for ch in snippet[: max(0, self.column - 1)]:
                # 한글/전각 문자는 2칸, 영문/기호는 1칸, 탭은 4칸
                if ord(ch) > 127:
                    caret_spaces += "  "
                elif ch == "\t":
                    caret_spaces += "    "
                else:
                    caret_spaces += " "
            return f"{header}\n\n{snippet}\n{caret_spaces}^"
        return header


class LexerError(SeoyunError):
    pass


class SyntaxError(SeoyunError):
    pass


class TypeError(SeoyunError):
    pass


class NameError(SeoyunError):
    pass


class RuntimeError(SeoyunError):
    pass


class IndexError(SeoyunError):
    pass


class ConstAssignmentError(SeoyunError):
    pass
