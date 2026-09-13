from dataclasses import dataclass
from typing import List, Callable, Optional, Any
from src.runtime.values import Value, NullValue, NULL_VALUE
from src.runtime.environment import Environment
from src.ast.nodes import FunctionDecl
from src.interpreter.control_flow import ReturnSignal
from src.errors import TypeError, RuntimeError


@dataclass
class CallFrame:
    function_name: str
    line: int
    column: int


class CallableValue(Value):
    """호출 가능한 값의 추상 클래스"""

    def call(self, interpreter: Any, args: List[Value], line: int, column: int) -> Value:
        raise NotImplementedError


class FunctionValue(CallableValue):
    """사용자 정의 서윤랭 함수"""

    def __init__(self, decl: FunctionDecl, closure: Environment):
        self.decl = decl
        self.closure = closure

    def call(self, interpreter: Any, args: List[Value], line: int, column: int) -> Value:
        if len(args) != len(self.decl.params):
            raise TypeError(
                f"함수 '{self.decl.name}' 호출에 {len(self.decl.params)}개의 인자가 필요하지만 {len(args)}개가 전달되었습니다.",
                line=line,
                column=column,
                source_code=interpreter.source_code,
            )

        frame = CallFrame(function_name=self.decl.name, line=line, column=column)
        interpreter.call_stack.append(frame)

        local_env = Environment(parent=self.closure, is_function_boundary=True)
        for param, arg in zip(self.decl.params, args):
            local_env.define(
                name=param.name,
                value=arg,
                type_name=param.type_name or "",
                is_const=False,
                line=line,
                column=column,
                source_code=interpreter.source_code,
            )

        try:
            interpreter.execute_block(self.decl.body, local_env)
        except ReturnSignal as sig:
            # 반환 타입 검사 (명시된 경우)
            if self.decl.return_type:
                return local_env._check_and_coerce_type(
                    self.decl.return_type, sig.value, line, column, interpreter.source_code
                )
            return sig.value
        finally:
            interpreter.call_stack.pop()

        return NULL_VALUE

    def display(self) -> str:
        return f"<function {self.decl.name}>"

    def __repr__(self) -> str:
        return f"FunctionValue({self.decl.name})"


class BuiltinFunctionValue(CallableValue):
    """내장 함수"""

    def __init__(self, name: str, fn: Callable[..., Value]):
        self.name = name
        self.fn = fn

    def call(self, interpreter: Any, args: List[Value], line: int, column: int) -> Value:
        return self.fn(interpreter, args, line, column)

    def display(self) -> str:
        return f"<builtin-function {self.name}>"

    def __repr__(self) -> str:
        return f"BuiltinFunctionValue({self.name})"
