from dataclasses import dataclass
from typing import Dict, Optional, Any
from src.runtime.values import (
    Value,
    IntValue,
    LongValue,
    FloatValue,
    CharValue,
    StringValue,
    BoolValue,
    NullValue,
    ArrayValue,
    ListValue,
    StackValue,
    NULL_VALUE,
)
from src.errors import NameError, TypeError, ConstAssignmentError


@dataclass
class VariableBinding:
    name: str
    type_name: str
    value: Value
    is_const: bool = False


class Environment:
    """스코프(Scope) 환경 클래스"""

    def __init__(self, parent: Optional["Environment"] = None, is_function_boundary: bool = False):
        self.parent: Optional["Environment"] = parent
        self.is_function_boundary: bool = is_function_boundary
        self.bindings: Dict[str, VariableBinding] = {}

    def define(
        self,
        name: str,
        value: Optional[Value],
        type_name: str,
        is_const: bool = False,
        line: int = 1,
        column: int = 1,
        source_code: Optional[str] = None,
    ) -> None:
        if name in self.bindings:
            raise NameError(
                f"현재 스코프에 이미 선언된 식별자입니다: '{name}'",
                line=line,
                column=column,
                source_code=source_code,
            )

        # 초기값이 제공되지 않은 경우 타입별 기본값 설정
        if value is None:
            value = self._get_default_value(type_name)

        coerced_value = self._check_and_coerce_type(type_name, value, line, column, source_code)
        self.bindings[name] = VariableBinding(
            name=name,
            type_name=type_name,
            value=coerced_value,
            is_const=is_const,
        )

    def assign(
        self,
        name: str,
        value: Value,
        line: int = 1,
        column: int = 1,
        source_code: Optional[str] = None,
    ) -> None:
        if name in self.bindings:
            binding = self.bindings[name]
            if binding.is_const:
                raise ConstAssignmentError(
                    f"상수 '{name}'에는 값을 재할당할 수 없습니다.",
                    line=line,
                    column=column,
                    source_code=source_code,
                )
            coerced_value = self._check_and_coerce_type(
                binding.type_name, value, line, column, source_code
            )
            binding.value = coerced_value
            return

        if self.parent is not None:
            self.parent.assign(name, value, line, column, source_code)
            return

        raise NameError(
            f"선언되지 않은 변수입니다: '{name}'",
            line=line,
            column=column,
            source_code=source_code,
        )

    def get(
        self,
        name: str,
        line: int = 1,
        column: int = 1,
        source_code: Optional[str] = None,
    ) -> Value:
        if name in self.bindings:
            return self.bindings[name].value

        if self.parent is not None:
            return self.parent.get(name, line, column, source_code)

        raise NameError(
            f"선언되지 않은 식별자입니다: '{name}'",
            line=line,
            column=column,
            source_code=source_code,
        )

    def contains_key(self, name: str) -> bool:
        if name in self.bindings:
            return True
        if self.parent is not None:
            return self.parent.contains_key(name)
        return False

    def _get_default_value(self, type_name: str) -> Value:
        if type_name == "e의2승":
            return IntValue(0)
        elif type_name == "울산큰고래":
            return LongValue(0)
        elif type_name == "고래":
            return FloatValue(0.0)
        elif type_name == "오?":
            return CharValue("\0")
        elif type_name == "서울말":
            return StringValue("")
        elif type_name == "아진짜ㅏ요":
            return BoolValue(False)
        elif type_name == "사투링고":
            return ArrayValue([])
        elif type_name == "블루베리스무디레시피":
            return ListValue([])
        elif type_name == "울산고래탑":
            return StackValue([])
        return NULL_VALUE

    def _check_and_coerce_type(
        self,
        expected_type: str,
        value: Value,
        line: int,
        column: int,
        source_code: Optional[str],
    ) -> Value:
        # 타입이 명시되지 않은 경우(예: 암시적 변수나 매개변수) 그대로 통과
        if not expected_type:
            return value

        # null (남친) 허용
        if isinstance(value, NullValue):
            return value

        if expected_type == "e의2승":
            if isinstance(value, IntValue):
                return value
            if isinstance(value, LongValue):
                return IntValue(value.val)
            if isinstance(value, StringValue):
                try:
                    return IntValue(int(value.val.strip()))
                except ValueError:
                    pass
            raise TypeError(
                f"'e의2승'(int) 타입 변수에 '{type(value).__name__}' 값을 할당할 수 없습니다.",
                line=line,
                column=column,
                source_code=source_code,
            )

        if expected_type == "울산큰고래":
            if isinstance(value, (LongValue, IntValue)):
                return LongValue(value.val)
            if isinstance(value, StringValue):
                try:
                    return LongValue(int(value.val.strip()))
                except ValueError:
                    pass
            raise TypeError(
                f"'울산큰고래'(long) 타입 변수에 '{type(value).__name__}' 값을 할당할 수 없습니다.",
                line=line,
                column=column,
                source_code=source_code,
            )

        if expected_type == "고래":
            if isinstance(value, FloatValue):
                return value
            if isinstance(value, (IntValue, LongValue)):
                return FloatValue(float(value.val))
            if isinstance(value, StringValue):
                try:
                    return FloatValue(float(value.val.strip()))
                except ValueError:
                    pass
            raise TypeError(
                f"'고래'(float) 타입 변수에 '{type(value).__name__}' 값을 할당할 수 없습니다.",
                line=line,
                column=column,
                source_code=source_code,
            )

        if expected_type == "오?":
            if isinstance(value, CharValue):
                return value
            if isinstance(value, StringValue) and len(value.val) == 1:
                return CharValue(value.val)
            raise TypeError(
                f"'오?'(char) 타입 변수에 '{type(value).__name__}' 값을 할당할 수 없습니다.",
                line=line,
                column=column,
                source_code=source_code,
            )

        if expected_type == "서울말":
            if isinstance(value, StringValue):
                return value
            if isinstance(value, CharValue):
                return StringValue(value.val)
            raise TypeError(
                f"'서울말'(string) 타입 변수에 '{type(value).__name__}' 값을 할당할 수 없습니다.",
                line=line,
                column=column,
                source_code=source_code,
            )

        if expected_type == "아진짜ㅏ요":
            if isinstance(value, BoolValue):
                return value
            raise TypeError(
                f"'아진짜ㅏ요'(bool) 타입 변수에 '{type(value).__name__}' 값을 할당할 수 없습니다.",
                line=line,
                column=column,
                source_code=source_code,
            )

        if expected_type == "사투링고":
            if isinstance(value, ArrayValue):
                return value
            if isinstance(value, ListValue):
                return ArrayValue(list(value.elements))
            raise TypeError(
                f"'사투링고'(Array) 타입 변수에 '{type(value).__name__}' 값을 할당할 수 없습니다.",
                line=line,
                column=column,
                source_code=source_code,
            )

        if expected_type == "블루베리스무디레시피":
            if isinstance(value, ListValue):
                return value
            if isinstance(value, ArrayValue):
                return ListValue(list(value.elements))
            raise TypeError(
                f"'블루베리스무디레시피'(List) 타입 변수에 '{type(value).__name__}' 값을 할당할 수 없습니다.",
                line=line,
                column=column,
                source_code=source_code,
            )

        if expected_type == "울산고래탑":
            if isinstance(value, StackValue):
                return value
            if isinstance(value, (ArrayValue, ListValue)):
                return StackValue(list(value.elements))
            raise TypeError(
                f"'울산고래탑'(Stack) 타입 변수에 '{type(value).__name__}' 값을 할당할 수 없습니다.",
                line=line,
                column=column,
                source_code=source_code,
            )

        # 사용자 정의 클래스 인스턴스 또는 미지정 타입
        return value
