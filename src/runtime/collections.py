from typing import List, Any
from src.runtime.values import (
    Value,
    IntValue,
    StringValue,
    CharValue,
    BoolValue,
    ArrayValue,
    ListValue,
    StackValue,
    NULL_VALUE,
    TRUE_VALUE,
    FALSE_VALUE,
)
from src.runtime.function import CallableValue
from src.errors import IndexError, RuntimeError, TypeError


class BoundMethodValue(CallableValue):
    """자료구조 및 문자열 내장 인스턴스 메서드"""

    def __init__(self, target: Value, method_name: str):
        self.target = target
        self.method_name = method_name

    def call(self, interpreter: Any, args: List[Value], line: int, column: int) -> Value:
        src = interpreter.source_code

        # 1. 블루베리스무디레시피 (List) 메서드
        if isinstance(self.target, ListValue):
            return self._call_list_method(args, line, column, src)

        # 2. 울산고래탑 (Stack) 메서드
        if isinstance(self.target, StackValue):
            return self._call_stack_method(args, line, column, src)

        # 3. 서울말 (String) 메서드
        if isinstance(self.target, StringValue):
            return self._call_string_method(args, line, column, src)

        # 4. 사투링고 (Array) 메서드
        if isinstance(self.target, ArrayValue):
            return self._call_array_method(args, line, column, src)

        raise RuntimeError(
            f"'{type(self.target).__name__}' 타입은 메서드 '{self.method_name}'을(를) 지원하지 않습니다.",
            line=line,
            column=column,
            source_code=src,
        )

    def _call_list_method(
        self, args: List[Value], line: int, column: int, src: Any
    ) -> Value:
        lst = self.target.elements
        m = self.method_name

        if m in ("size", "length"):
            return IntValue(len(lst))

        elif m == "push":
            if len(args) != 1:
                raise TypeError(f"push() 메서드는 1개의 인자가 필요합니다.", line=line, column=column, source_code=src)
            lst.append(args[0])
            return args[0]

        elif m == "pop":
            if not lst:
                raise IndexError("빈 리스트에서 pop을 수행할 수 없습니다.", line=line, column=column, source_code=src)
            return lst.pop()

        elif m == "clear":
            lst.clear()
            return NULL_VALUE

        elif m == "insert":
            if len(args) != 2:
                raise TypeError(f"insert(index, item) 메서드는 2개의 인자가 필요합니다.", line=line, column=column, source_code=src)
            if not isinstance(args[0], IntValue):
                raise TypeError("insert의 인덱스는 정수여야 합니다.", line=line, column=column, source_code=src)
            idx = args[0].val
            if not (0 <= idx <= len(lst)):
                raise IndexError(f"인덱스 범위를 벗어났습니다: {idx}", line=line, column=column, source_code=src)
            lst.insert(idx, args[1])
            return NULL_VALUE

        elif m == "remove":
            if len(args) != 1:
                raise TypeError(f"remove() 메서드는 1개의 인자가 필요합니다.", line=line, column=column, source_code=src)
            # 인덱스로 삭제 또는 값으로 삭제 지원
            if isinstance(args[0], IntValue):
                idx = args[0].val
                if 0 <= idx < len(lst):
                    return lst.pop(idx)
            for i, item in enumerate(lst):
                if item == args[0] or getattr(item, 'val', None) == getattr(args[0], 'val', None):
                    return lst.pop(i)
            return NULL_VALUE

        elif m == "contains":
            if len(args) != 1:
                raise TypeError(f"contains() 메서드는 1개의 인자가 필요합니다.", line=line, column=column, source_code=src)
            target_val = getattr(args[0], 'val', args[0])
            for item in lst:
                item_val = getattr(item, 'val', item)
                if item_val == target_val:
                    return TRUE_VALUE
            return FALSE_VALUE

        raise RuntimeError(
            f"블루베리스무디레시피(List)에 알 수 없는 메서드입니다: '{m}'",
            line=line,
            column=column,
            source_code=src,
        )

    def _call_stack_method(
        self, args: List[Value], line: int, column: int, src: Any
    ) -> Value:
        stk = self.target.elements
        m = self.method_name

        if m == "push":
            if len(args) != 1:
                raise TypeError("push() 메서드는 1개의 인자가 필요합니다.", line=line, column=column, source_code=src)
            stk.append(args[0])
            return args[0]

        elif m == "pop":
            if not stk:
                raise IndexError("빈 스택에서 pop을 수행할 수 없습니다.", line=line, column=column, source_code=src)
            return stk.pop()

        elif m == "top":
            if not stk:
                raise IndexError("빈 스택에서 top을 조회할 수 없습니다.", line=line, column=column, source_code=src)
            return stk[-1]

        elif m in ("size", "length"):
            return IntValue(len(stk))

        elif m == "empty":
            return TRUE_VALUE if len(stk) == 0 else FALSE_VALUE

        raise RuntimeError(
            f"울산고래탑(Stack)에 알 수 없는 메서드입니다: '{m}'",
            line=line,
            column=column,
            source_code=src,
        )

    def _call_string_method(
        self, args: List[Value], line: int, column: int, src: Any
    ) -> Value:
        s = self.target.val
        m = self.method_name

        if m in ("length", "size"):
            return IntValue(len(s))

        elif m == "split":
            sep = args[0].val if args and hasattr(args[0], "val") else None
            parts = s.split(sep)
            return ListValue([StringValue(p) for p in parts])

        elif m == "substring":
            if len(args) == 1 and isinstance(args[0], IntValue):
                return StringValue(s[args[0].val :])
            elif len(args) >= 2 and isinstance(args[0], IntValue) and isinstance(args[1], IntValue):
                return StringValue(s[args[0].val : args[1].val])
            raise TypeError("substring은 1개 또는 2개의 정수 인자가 필요합니다.", line=line, column=column, source_code=src)

        elif m == "find":
            if not args or not hasattr(args[0], "val"):
                raise TypeError("find는 찾을 문자열 인자가 필요합니다.", line=line, column=column, source_code=src)
            sub = str(args[0].val)
            return IntValue(s.find(sub))

        raise RuntimeError(
            f"서울말(String)에 알 수 없는 메서드입니다: '{m}'",
            line=line,
            column=column,
            source_code=src,
        )

    def _call_array_method(
        self, args: List[Value], line: int, column: int, src: Any
    ) -> Value:
        arr = self.target.elements
        m = self.method_name

        if m in ("size", "length"):
            return IntValue(len(arr))

        raise RuntimeError(
            f"사투링고(Array)에 알 수 없는 메서드입니다: '{m}'",
            line=line,
            column=column,
            source_code=src,
        )

    def display(self) -> str:
        return f"<bound-method {self.method_name}>"
