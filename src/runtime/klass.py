from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from src.runtime.values import Value, NULL_VALUE
from src.runtime.function import CallableValue, FunctionValue, CallFrame
from src.ast.nodes import ClassDecl
from src.runtime.environment import Environment
from src.errors import NameError, RuntimeError, TypeError


class InstanceEnvironment(Environment):
    """인스턴스의 필드 및 메서드를 직접 참조할 수 있는 스코프 환경"""

    def __init__(self, instance: "InstanceValue", parent: Environment):
        super().__init__(parent=parent)
        self.instance = instance

    def get(
        self,
        name: str,
        line: int = 1,
        column: int = 1,
        source_code: Optional[str] = None,
    ) -> Value:
        if name in self.bindings:
            return self.bindings[name].value
        if name in self.instance.fields:
            return self.instance.fields[name]
        if name in self.instance.methods:
            return self.instance.methods[name]
        if name in ("this", "self"):
            return self.instance
        if self.parent is not None:
            return self.parent.get(name, line, column, source_code)
        raise NameError(
            f"선언되지 않은 식별자입니다: '{name}'",
            line=line,
            column=column,
            source_code=source_code,
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
            super().assign(name, value, line, column, source_code)
            return
        if name in self.instance.fields:
            self.instance.fields[name] = value
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


class BoundInstanceMethodValue(CallableValue):
    """인스턴스에 바인딩된 메서드"""

    def __init__(self, instance: "InstanceValue", method: FunctionValue):
        self.instance = instance
        self.method = method

    def call(self, interpreter: Any, args: List[Value], line: int, column: int) -> Value:
        decl = self.method.decl
        if len(args) != len(decl.params):
            raise TypeError(
                f"메서드 '{decl.name}' 호출에 {len(decl.params)}개의 인자가 필요하지만 {len(args)}개가 전달되었습니다.",
                line=line,
                column=column,
                source_code=interpreter.source_code,
            )

        frame = CallFrame(function_name=f"{self.instance.klass.decl.name}.{decl.name}", line=line, column=column)
        interpreter.call_stack.append(frame)

        # 인스턴스 환경을 부모로 하여 로컬 환경 생성
        instance_env = InstanceEnvironment(self.instance, parent=self.method.closure)
        local_env = Environment(parent=instance_env, is_function_boundary=True)

        for param, arg in zip(decl.params, args):
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
            from src.interpreter.control_flow import ReturnSignal
            interpreter.execute_block(decl.body, local_env)
        except ReturnSignal as sig:
            if decl.return_type:
                return local_env._check_and_coerce_type(
                    decl.return_type, sig.value, line, column, interpreter.source_code
                )
            return sig.value
        finally:
            interpreter.call_stack.pop()

        return NULL_VALUE

    def display(self) -> str:
        return f"<bound method {self.instance.klass.decl.name}.{self.method.decl.name}>"


class ClassValue(CallableValue):
    """클래스 정의 런타임 객체"""

    def __init__(self, decl: ClassDecl, closure: Environment):
        self.decl = decl
        self.closure = closure

    def call(self, interpreter: Any, args: List[Value], line: int, column: int) -> Value:
        instance = InstanceValue(self)

        # 기본 필드 초기화
        for f in self.decl.fields:
            init_val = None
            if f.init is not None:
                init_val = interpreter.evaluate(f.init)
            else:
                init_val = self.closure._get_default_value(f.type_name)
            instance.fields[f.name] = init_val

        # init 메서드가 있다면 호출
        if "init" in instance.methods:
            bound_init = BoundInstanceMethodValue(instance, instance.methods["init"])
            bound_init.call(interpreter, args, line, column)

        return instance

    def display(self) -> str:
        return f"<class {self.decl.name}>"

    def __repr__(self) -> str:
        return f"ClassValue({self.decl.name})"


class InstanceValue(Value):
    """클래스 인스턴스 런타임 객체"""

    def __init__(self, klass: ClassValue):
        self.klass = klass
        self.fields: Dict[str, Value] = {}
        self.methods: Dict[str, FunctionValue] = {}

        # 클래스에 정의된 메서드 준비
        for m in klass.decl.methods:
            self.methods[m.name] = FunctionValue(m, klass.closure)

    def get_member(self, member: str, line: int, column: int, src: Optional[str]) -> Value:
        if member in self.fields:
            return self.fields[member]
        if member in self.methods:
            return BoundInstanceMethodValue(self, self.methods[member])

        raise NameError(
            f"'{self.klass.decl.name}' 객체에 멤버 '{member}'이(가) 존재하지 않습니다.",
            line=line,
            column=column,
            source_code=src,
        )

    def set_member(self, member: str, value: Value) -> None:
        self.fields[member] = value

    def display(self) -> str:
        return f"<instance of {self.klass.decl.name}>"

    def __repr__(self) -> str:
        return f"InstanceValue({self.klass.decl.name})"
