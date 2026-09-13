from dataclasses import dataclass
from typing import Any, List, Dict, Optional


class Value:
    """서윤랭 런타임 값의 최상위 클래스"""

    def display(self) -> str:
        return str(self)

    def is_truthy(self) -> bool:
        return True


@dataclass
class IntValue(Value):
    val: int

    def display(self) -> str:
        return str(self.val)

    def is_truthy(self) -> bool:
        return self.val != 0

    def __repr__(self) -> str:
        return f"IntValue({self.val})"


@dataclass
class LongValue(Value):
    val: int

    def display(self) -> str:
        return str(self.val)

    def is_truthy(self) -> bool:
        return self.val != 0

    def __repr__(self) -> str:
        return f"LongValue({self.val})"


@dataclass
class FloatValue(Value):
    val: float

    def display(self) -> str:
        # 소수점 형식 표시
        if self.val.is_integer():
            return f"{self.val:.1f}"
        return str(self.val)

    def is_truthy(self) -> bool:
        return self.val != 0.0

    def __repr__(self) -> str:
        return f"FloatValue({self.val})"


@dataclass
class CharValue(Value):
    val: str

    def display(self) -> str:
        return self.val

    def is_truthy(self) -> bool:
        return len(self.val) > 0

    def __repr__(self) -> str:
        return f"CharValue({self.val!r})"


@dataclass
class StringValue(Value):
    val: str

    def display(self) -> str:
        return self.val

    def is_truthy(self) -> bool:
        return len(self.val) > 0

    def __repr__(self) -> str:
        return f"StringValue({self.val!r})"


@dataclass
class BoolValue(Value):
    val: bool

    def display(self) -> str:
        return "짘자" if self.val else "안히"

    def is_truthy(self) -> bool:
        return self.val

    def __repr__(self) -> str:
        return f"BoolValue({self.val})"


@dataclass
class NullValue(Value):
    def display(self) -> str:
        return "남친"

    def is_truthy(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "NullValue()"


@dataclass
class ArrayValue(Value):
    elements: List[Value]

    def display(self) -> str:
        inner = ", ".join(e.display() for e in self.elements)
        return f"[{inner}]"

    def is_truthy(self) -> bool:
        return len(self.elements) > 0

    def __repr__(self) -> str:
        return f"ArrayValue({self.elements!r})"


@dataclass
class ListValue(Value):
    elements: List[Value]

    def display(self) -> str:
        inner = ", ".join(e.display() for e in self.elements)
        return f"[{inner}]"

    def is_truthy(self) -> bool:
        return len(self.elements) > 0

    def __repr__(self) -> str:
        return f"ListValue({self.elements!r})"


@dataclass
class StackValue(Value):
    elements: List[Value]

    def display(self) -> str:
        inner = ", ".join(e.display() for e in self.elements)
        return f"Stack([{inner}])"

    def is_truthy(self) -> bool:
        return len(self.elements) > 0

    def __repr__(self) -> str:
        return f"StackValue({self.elements!r})"


# 싱글톤 Null 상수
NULL_VALUE = NullValue()
TRUE_VALUE = BoolValue(True)
FALSE_VALUE = BoolValue(False)
