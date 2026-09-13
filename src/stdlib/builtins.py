import sys
from typing import List, Any
from src.runtime.values import (
    Value,
    IntValue,
    LongValue,
    FloatValue,
    CharValue,
    StringValue,
    BoolValue,
    ArrayValue,
    ListValue,
    StackValue,
    NULL_VALUE,
    TRUE_VALUE,
    FALSE_VALUE,
)
from src.runtime.function import BuiltinFunctionValue
from src.errors import TypeError, RuntimeError, IndexError


def _fn_print(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    """오쫄티비: 여러 인자를 공백으로 구분하여 출력하고 개행"""
    out_str = " ".join(arg.display() for arg in args)
    print(out_str, file=interpreter.stdout)
    return NULL_VALUE


def _fn_input(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    """게히야: 표준 입력에서 한 줄을 읽어 문자열로 반환"""
    prompt = args[0].display() if args else ""
    try:
        line_read = interpreter.stdin.readline()
        if not line_read:
            return StringValue("")
        # 개행 제거
        line_read = line_read.rstrip("\r\n")
        return StringValue(line_read)
    except Exception as e:
        raise RuntimeError(f"입력 중 오류가 발생했습니다: {e}", line=line, column=column, source_code=interpreter.source_code)


def _fn_len(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if len(args) != 1:
        raise TypeError(f"len()은 1개의 인자가 필요하지만 {len(args)}개가 주어졌습니다.", line=line, column=column, source_code=interpreter.source_code)
    arg = args[0]
    if isinstance(arg, (StringValue, CharValue)):
        return IntValue(len(arg.val))
    if isinstance(arg, (ArrayValue, ListValue, StackValue)):
        return IntValue(len(arg.elements))
    raise TypeError(f"'{type(arg).__name__}' 타입은 len()을 지원하지 않습니다.", line=line, column=column, source_code=interpreter.source_code)


def _fn_abs(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if len(args) != 1:
        raise TypeError(f"abs()은 1개의 인자가 필요합니다.", line=line, column=column, source_code=interpreter.source_code)
    arg = args[0]
    if isinstance(arg, (IntValue, LongValue)):
        return IntValue(abs(arg.val))
    if isinstance(arg, FloatValue):
        return FloatValue(abs(arg.val))
    raise TypeError(f"abs()의 인자는 숫자여야 합니다.", line=line, column=column, source_code=interpreter.source_code)


def _fn_min(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if not args:
        raise TypeError("min()은 최소 1개 이상의 인자가 필요합니다.", line=line, column=column, source_code=interpreter.source_code)
    if len(args) == 1 and isinstance(args[0], (ArrayValue, ListValue)):
        items = args[0].elements
        if not items:
            raise IndexError("빈 컬렉션에서 min을 구할 수 없습니다.", line=line, column=column, source_code=interpreter.source_code)
        smallest = items[0]
        for it in items[1:]:
            if _extract_scalar(it) < _extract_scalar(smallest):
                smallest = it
        return smallest

    smallest = args[0]
    for arg in args[1:]:
        if _extract_scalar(arg) < _extract_scalar(smallest):
            smallest = arg
    return smallest


def _fn_max(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if not args:
        raise TypeError("max()은 최소 1개 이상의 인자가 필요합니다.", line=line, column=column, source_code=interpreter.source_code)
    if len(args) == 1 and isinstance(args[0], (ArrayValue, ListValue)):
        items = args[0].elements
        if not items:
            raise IndexError("빈 컬렉션에서 max를 구할 수 없습니다.", line=line, column=column, source_code=interpreter.source_code)
        biggest = items[0]
        for it in items[1:]:
            if _extract_scalar(it) > _extract_scalar(biggest):
                biggest = it
        return biggest

    biggest = args[0]
    for arg in args[1:]:
        if _extract_scalar(arg) > _extract_scalar(biggest):
            biggest = arg
    return biggest


def _fn_sort(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if len(args) != 1 or not isinstance(args[0], (ArrayValue, ListValue)):
        raise TypeError("sort()는 배열 또는 리스트 1개를 인자로 받아야 합니다.", line=line, column=column, source_code=interpreter.source_code)
    items = args[0].elements
    items.sort(key=_extract_scalar)
    return args[0]


def _fn_reverse(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if len(args) != 1 or not isinstance(args[0], (ArrayValue, ListValue)):
        raise TypeError("reverse()는 배열 또는 리스트 1개를 인자로 받아야 합니다.", line=line, column=column, source_code=interpreter.source_code)
    args[0].elements.reverse()
    return args[0]


def _fn_split(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if not args or not isinstance(args[0], StringValue):
        raise TypeError("split()의 첫 번째 인자는 문자열이어야 합니다.", line=line, column=column, source_code=interpreter.source_code)
    s = args[0].val
    sep = args[1].val if len(args) > 1 and hasattr(args[1], "val") else None
    parts = s.split(sep)
    return ListValue([StringValue(p) for p in parts])


# 기본 형변환 함수
def _fn_to_int(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if len(args) != 1:
        raise TypeError("int()는 1개의 인자가 필요합니다.", line=line, column=column, source_code=interpreter.source_code)
    arg = args[0]
    if isinstance(arg, (IntValue, LongValue)):
        return IntValue(arg.val)
    if isinstance(arg, FloatValue):
        return IntValue(int(arg.val))
    if isinstance(arg, StringValue):
        try:
            return IntValue(int(arg.val.strip()))
        except ValueError:
            raise TypeError(f"문자열 '{arg.val}'을(를) 정수로 변환할 수 없습니다.", line=line, column=column, source_code=interpreter.source_code)
    if isinstance(arg, CharValue):
        return IntValue(ord(arg.val))
    raise TypeError(f"'{type(arg).__name__}'을(를) 정수로 변환할 수 없습니다.", line=line, column=column, source_code=interpreter.source_code)


def _fn_to_long(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    res = _fn_to_int(interpreter, args, line, column)
    return LongValue(res.val)


def _fn_to_float(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if len(args) != 1:
        raise TypeError("float()는 1개의 인자가 필요합니다.", line=line, column=column, source_code=interpreter.source_code)
    arg = args[0]
    if isinstance(arg, FloatValue):
        return arg
    if isinstance(arg, (IntValue, LongValue)):
        return FloatValue(float(arg.val))
    if isinstance(arg, StringValue):
        try:
            return FloatValue(float(arg.val.strip()))
        except ValueError:
            raise TypeError(f"문자열 '{arg.val}'을(를) 실수로 변환할 수 없습니다.", line=line, column=column, source_code=interpreter.source_code)
    raise TypeError(f"'{type(arg).__name__}'을(를) 실수로 변환할 수 없습니다.", line=line, column=column, source_code=interpreter.source_code)


def _fn_to_string(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if len(args) != 1:
        raise TypeError("string()은 1개의 인자가 필요합니다.", line=line, column=column, source_code=interpreter.source_code)
    return StringValue(args[0].display())


def _fn_to_char(interpreter: Any, args: List[Value], line: int, column: int) -> Value:
    if len(args) != 1:
        raise TypeError("char()는 1개의 인자가 필요합니다.", line=line, column=column, source_code=interpreter.source_code)
    arg = args[0]
    if isinstance(arg, (IntValue, LongValue)):
        return CharValue(chr(arg.val))
    if isinstance(arg, StringValue) and len(arg.val) == 1:
        return CharValue(arg.val)
    if isinstance(arg, CharValue):
        return arg
    raise TypeError(f"'{type(arg).__name__}'을(를) 문자로 변환할 수 없습니다.", line=line, column=column, source_code=interpreter.source_code)


def _extract_scalar(v: Value) -> Any:
    return getattr(v, "val", 0)


def register_builtins(env: Any) -> None:
    """글로벌 환경에 내장 함수 등록"""
    builtins = {
        # 서윤랭 입출력 확정 키워드
        "오쫄티비": _fn_print,
        "게히야": _fn_input,

        # 알고리즘 함수
        "len": _fn_len,
        "abs": _fn_abs,
        "min": _fn_min,
        "max": _fn_max,
        "sort": _fn_sort,
        "reverse": _fn_reverse,
        "split": _fn_split,

        # 형변환 함수
        "int": _fn_to_int,
        "to_int": _fn_to_int,
        "long": _fn_to_long,
        "to_long": _fn_to_long,
        "float": _fn_to_float,
        "to_float": _fn_to_float,
        "string": _fn_to_string,
        "to_string": _fn_to_string,
        "char": _fn_to_char,
        "to_char": _fn_to_char,
    }

    for name, fn in builtins.items():
        env.define(name, BuiltinFunctionValue(name, fn), "", False)
