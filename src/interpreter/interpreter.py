import sys
from typing import List, Optional, Any
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
    TRUE_VALUE,
    FALSE_VALUE,
)
from src.runtime.environment import Environment
from src.runtime.function import CallableValue, FunctionValue, CallFrame
from src.runtime.collections import BoundMethodValue
from src.runtime.klass import ClassValue, InstanceValue
from src.stdlib.builtins import register_builtins
from src.interpreter.control_flow import BreakSignal, ContinueSignal, ReturnSignal
from src.errors import (
    TypeError,
    RuntimeError,
    IndexError,
    NameError,
    ConstAssignmentError,
)


class Interpreter:
    """서윤랭 인터프리터 (Interpreter)"""

    def __init__(
        self,
        source_code: Optional[str] = None,
        stdin: Any = sys.stdin,
        stdout: Any = sys.stdout,
    ):
        self.source_code: Optional[str] = source_code
        self.stdin = stdin
        self.stdout = stdout
        self.global_env = Environment()
        self.current_env = self.global_env
        self.call_stack: List[CallFrame] = []

        # 내장 함수 및 입출력 함수 등록
        register_builtins(self.global_env)

    def interpret(self, program: Program) -> None:
        for stmt in program.statements:
            self.execute(stmt)

    def execute(self, stmt: ASTNode) -> None:
        if isinstance(stmt, BlockStmt):
            self.execute_block(stmt, Environment(parent=self.current_env))

        elif isinstance(stmt, VariableDecl):
            init_val = self.evaluate(stmt.init) if stmt.init is not None else None
            self.current_env.define(
                name=stmt.name,
                value=init_val,
                type_name=stmt.type_name,
                is_const=stmt.is_const,
                line=stmt.line,
                column=stmt.column,
                source_code=self.source_code,
            )

        elif isinstance(stmt, ExpressionStmt):
            self.evaluate(stmt.expr)

        elif isinstance(stmt, IfStmt):
            cond_val = self.evaluate(stmt.condition)
            if cond_val.is_truthy():
                self.execute(stmt.then_branch)
            elif stmt.else_branch is not None:
                self.execute(stmt.else_branch)

        elif isinstance(stmt, WhileStmt):
            while self.evaluate(stmt.condition).is_truthy():
                try:
                    self.execute(stmt.body)
                except BreakSignal:
                    break
                except ContinueSignal:
                    continue

        elif isinstance(stmt, ForStmt):
            loop_env = Environment(parent=self.current_env)
            prev_env = self.current_env
            self.current_env = loop_env
            try:
                if stmt.init is not None:
                    self.execute(stmt.init)

                while True:
                    if stmt.condition is not None:
                        if not self.evaluate(stmt.condition).is_truthy():
                            break

                    try:
                        self.execute(stmt.body)
                    except BreakSignal:
                        break
                    except ContinueSignal:
                        pass

                    if stmt.update is not None:
                        self.evaluate(stmt.update)
            finally:
                self.current_env = prev_env

        elif isinstance(stmt, BreakStmt):
            raise BreakSignal()

        elif isinstance(stmt, ContinueStmt):
            raise ContinueSignal()

        elif isinstance(stmt, ReturnStmt):
            val = self.evaluate(stmt.value) if stmt.value is not None else NULL_VALUE
            raise ReturnSignal(val)

        elif isinstance(stmt, FunctionDecl):
            fn_val = FunctionValue(stmt, self.current_env)
            self.current_env.define(
                name=stmt.name,
                value=fn_val,
                type_name="",
                is_const=False,
                line=stmt.line,
                column=stmt.column,
                source_code=self.source_code,
            )

        elif isinstance(stmt, ClassDecl):
            cls_val = ClassValue(stmt, self.current_env)
            self.current_env.define(
                name=stmt.name,
                value=cls_val,
                type_name="",
                is_const=False,
                line=stmt.line,
                column=stmt.column,
                source_code=self.source_code,
            )

        else:
            raise RuntimeError(
                f"알 수 없는 구문 노드입니다: {type(stmt).__name__}",
                line=stmt.line,
                column=stmt.column,
                source_code=self.source_code,
            )

    def execute_block(self, block: BlockStmt, env: Environment) -> None:
        prev_env = self.current_env
        self.current_env = env
        try:
            for stmt in block.statements:
                self.execute(stmt)
        finally:
            self.current_env = prev_env

    def evaluate(self, expr: ASTNode) -> Value:
        if isinstance(expr, Literal):
            if expr.type_hint == "int":
                return IntValue(int(expr.value))
            elif expr.type_hint == "float":
                return FloatValue(float(expr.value))
            elif expr.type_hint == "string":
                return StringValue(str(expr.value))
            elif expr.type_hint == "char":
                return CharValue(str(expr.value))
            elif expr.type_hint == "bool":
                return TRUE_VALUE if expr.value else FALSE_VALUE
            elif expr.type_hint == "null":
                return NULL_VALUE
            return NULL_VALUE

        elif isinstance(expr, Identifier):
            return self.current_env.get(
                expr.name, line=expr.line, column=expr.column, source_code=self.source_code
            )

        elif isinstance(expr, ArrayLiteral):
            elements = [self.evaluate(elem) for elem in expr.elements]
            return ArrayValue(elements)

        elif isinstance(expr, IndexExpr):
            coll = self.evaluate(expr.target)
            idx_val = self.evaluate(expr.index)

            if not isinstance(idx_val, (IntValue, LongValue)):
                raise TypeError("인덱스는 정수여야 합니다.", line=expr.line, column=expr.column, source_code=self.source_code)

            idx = idx_val.val
            if isinstance(coll, (ArrayValue, ListValue)):
                if idx < 0 or idx >= len(coll.elements):
                    raise IndexError(
                        f"인덱스 범위를 벗어났습니다: {idx} (크기: {len(coll.elements)})",
                        line=expr.line,
                        column=expr.column,
                        source_code=self.source_code,
                    )
                return coll.elements[idx]

            elif isinstance(coll, StringValue):
                if idx < 0 or idx >= len(coll.val):
                    raise IndexError(
                        f"문자열 인덱스 범위를 벗어났습니다: {idx} (길이: {len(coll.val)})",
                        line=expr.line,
                        column=expr.column,
                        source_code=self.source_code,
                    )
                return CharValue(coll.val[idx])

            raise TypeError(
                f"'{type(coll).__name__}' 타입은 인덱스 접근을 지원하지 않습니다.",
                line=expr.line,
                column=expr.column,
                source_code=self.source_code,
            )

        elif isinstance(expr, MemberExpr):
            obj = self.evaluate(expr.target)
            if isinstance(obj, (ListValue, StackValue, StringValue, ArrayValue)):
                return BoundMethodValue(obj, expr.member)
            elif isinstance(obj, InstanceValue):
                return obj.get_member(expr.member, expr.line, expr.column, self.source_code)
            raise RuntimeError(
                f"'{type(obj).__name__}' 타입은 멤버 접근을 지원하지 않습니다: '{expr.member}'",
                line=expr.line,
                column=expr.column,
                source_code=self.source_code,
            )

        elif isinstance(expr, Assignment):
            val = self.evaluate(expr.value)
            if isinstance(expr.target, Identifier):
                self.current_env.assign(
                    expr.target.name,
                    val,
                    line=expr.line,
                    column=expr.column,
                    source_code=self.source_code,
                )
                return val

            elif isinstance(expr.target, IndexExpr):
                coll = self.evaluate(expr.target.target)
                idx_val = self.evaluate(expr.target.index)
                if not isinstance(idx_val, (IntValue, LongValue)):
                    raise TypeError("인덱스는 정수여야 합니다.", line=expr.line, column=expr.column, source_code=self.source_code)
                idx = idx_val.val

                if isinstance(coll, (ArrayValue, ListValue)):
                    if idx < 0 or idx >= len(coll.elements):
                        raise IndexError(
                            f"인덱스 범위를 벗어났습니다: {idx} (크기: {len(coll.elements)})",
                            line=expr.line,
                            column=expr.column,
                            source_code=self.source_code,
                        )
                    coll.elements[idx] = val
                    return val

                raise TypeError(
                    f"'{type(coll).__name__}' 타입은 인덱스 할당을 지원하지 않습니다.",
                    line=expr.line,
                    column=expr.column,
                    source_code=self.source_code,
                )

            elif isinstance(expr.target, MemberExpr):
                obj = self.evaluate(expr.target.target)
                if isinstance(obj, InstanceValue):
                    obj.set_member(expr.target.member, val)
                    return val
                raise TypeError(
                    f"'{type(obj).__name__}' 타입은 멤버 할당을 지원하지 않습니다.",
                    line=expr.line,
                    column=expr.column,
                    source_code=self.source_code,
                )

            raise RuntimeError("잘못된 할당 대상입니다.", line=expr.line, column=expr.column, source_code=self.source_code)

        elif isinstance(expr, UpdateExpr):
            delta = 1 if expr.op == "++" else -1
            if isinstance(expr.target, Identifier):
                old_val = self.current_env.get(
                    expr.target.name, line=expr.line, column=expr.column, source_code=self.source_code
                )
                if not isinstance(old_val, (IntValue, LongValue, FloatValue)):
                    raise TypeError("증감 연산자는 숫자 타입에만 적용할 수 있습니다.", line=expr.line, column=expr.column, source_code=self.source_code)
                new_num = old_val.val + delta
                new_val = IntValue(new_num) if isinstance(old_val, IntValue) else (
                    LongValue(new_num) if isinstance(old_val, LongValue) else FloatValue(float(new_num))
                )
                self.current_env.assign(
                    expr.target.name,
                    new_val,
                    line=expr.line,
                    column=expr.column,
                    source_code=self.source_code,
                )
                return new_val if expr.is_prefix else old_val

            elif isinstance(expr.target, IndexExpr):
                coll = self.evaluate(expr.target.target)
                idx_val = self.evaluate(expr.target.index)
                if not isinstance(idx_val, (IntValue, LongValue)):
                    raise TypeError("인덱스는 정수여야 합니다.", line=expr.line, column=expr.column, source_code=self.source_code)
                idx = idx_val.val

                if isinstance(coll, (ArrayValue, ListValue)):
                    if idx < 0 or idx >= len(coll.elements):
                        raise IndexError(f"인덱스 범위를 벗어났습니다: {idx}", line=expr.line, column=expr.column, source_code=self.source_code)
                    old_item = coll.elements[idx]
                    if not isinstance(old_item, (IntValue, LongValue, FloatValue)):
                        raise TypeError("증감 연산자는 숫자 타입에만 적용할 수 있습니다.", line=expr.line, column=expr.column, source_code=self.source_code)
                    new_num = old_item.val + delta
                    new_item = IntValue(new_num) if isinstance(old_item, IntValue) else (
                        LongValue(new_num) if isinstance(old_item, LongValue) else FloatValue(float(new_num))
                    )
                    coll.elements[idx] = new_item
                    return new_item if expr.is_prefix else old_item

            raise RuntimeError("잘못된 증감 대상입니다.", line=expr.line, column=expr.column, source_code=self.source_code)

        elif isinstance(expr, BinaryOp):
            # 논리 연산자 단락 평가 (Short-circuit)
            if expr.op == "&&":
                left_val = self.evaluate(expr.left)
                if not left_val.is_truthy():
                    return FALSE_VALUE
                right_val = self.evaluate(expr.right)
                return TRUE_VALUE if right_val.is_truthy() else FALSE_VALUE

            if expr.op == "||":
                left_val = self.evaluate(expr.left)
                if left_val.is_truthy():
                    return TRUE_VALUE
                right_val = self.evaluate(expr.right)
                return TRUE_VALUE if right_val.is_truthy() else FALSE_VALUE

            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)

            # 덧셈 (+): 문자열 연결 또는 산술 덧셈
            if expr.op == "+":
                if isinstance(left, (StringValue, CharValue)) or isinstance(right, (StringValue, CharValue)):
                    return StringValue(left.display() + right.display())
                if isinstance(left, ArrayValue) and isinstance(right, ArrayValue):
                    return ArrayValue(left.elements + right.elements)

            # 산술 / 비트 / 비교 연산
            return self._evaluate_binary_op(expr.op, left, right, expr.line, expr.column)

        elif isinstance(expr, UnaryOp):
            operand = self.evaluate(expr.operand)
            if expr.op == "!":
                return FALSE_VALUE if operand.is_truthy() else TRUE_VALUE
            if expr.op == "-":
                if isinstance(operand, IntValue):
                    return IntValue(-operand.val)
                if isinstance(operand, LongValue):
                    return LongValue(-operand.val)
                if isinstance(operand, FloatValue):
                    return FloatValue(-operand.val)
                raise TypeError("'-' 단항 연산자는 숫자 타입에만 사용할 수 있습니다.", line=expr.line, column=expr.column, source_code=self.source_code)
            if expr.op == "+":
                if isinstance(operand, (IntValue, LongValue, FloatValue)):
                    return operand
                raise TypeError("'+' 단항 연산자는 숫자 타입에만 사용할 수 있습니다.", line=expr.line, column=expr.column, source_code=self.source_code)

            raise RuntimeError(f"알 수 없는 단항 연산자입니다: '{expr.op}'", line=expr.line, column=expr.column, source_code=self.source_code)

        elif isinstance(expr, CallExpr):
            callee = self.evaluate(expr.callee)
            args = [self.evaluate(a) for a in expr.args]

            if isinstance(callee, CallableValue):
                return callee.call(self, args, expr.line, expr.column)

            raise TypeError(
                f"'{type(callee).__name__}'은(는) 호출 가능한 객체가 아닙니다.",
                line=expr.line,
                column=expr.column,
                source_code=self.source_code,
            )

        raise RuntimeError(
            f"알 수 없는 표현식 노드입니다: {type(expr).__name__}",
            line=expr.line,
            column=expr.column,
            source_code=self.source_code,
        )

    def _evaluate_binary_op(
        self, op: str, left: Value, right: Value, line: int, column: int
    ) -> Value:
        src = self.source_code

        # 1. 동등성 검사 (==, !=)
        if op == "==":
            return TRUE_VALUE if self._is_equal(left, right) else FALSE_VALUE
        if op == "!=":
            return FALSE_VALUE if self._is_equal(left, right) else TRUE_VALUE

        # 2. 숫자 기반 연산자 검사
        is_num_left = isinstance(left, (IntValue, LongValue, FloatValue))
        is_num_right = isinstance(right, (IntValue, LongValue, FloatValue))

        if not (is_num_left and is_num_right):
            # 문자열 간 비교 지원
            if isinstance(left, (StringValue, CharValue)) and isinstance(right, (StringValue, CharValue)):
                s_l = left.val
                s_r = right.val
                if op == "<":
                    return TRUE_VALUE if s_l < s_r else FALSE_VALUE
                if op == "<=":
                    return TRUE_VALUE if s_l <= s_r else FALSE_VALUE
                if op == ">":
                    return TRUE_VALUE if s_l > s_r else FALSE_VALUE
                if op == ">=":
                    return TRUE_VALUE if s_l >= s_r else FALSE_VALUE

            raise TypeError(
                f"'{op}' 연산자는 '{type(left).__name__}'과(와) '{type(right).__name__}' 사이에 지원되지 않습니다.",
                line=line,
                column=column,
                source_code=src,
            )

        v_l = left.val
        v_r = right.val
        has_float = isinstance(left, FloatValue) or isinstance(right, FloatValue)

        # 비교 연산자
        if op == "<":
            return TRUE_VALUE if v_l < v_r else FALSE_VALUE
        if op == "<=":
            return TRUE_VALUE if v_l <= v_r else FALSE_VALUE
        if op == ">":
            return TRUE_VALUE if v_l > v_r else FALSE_VALUE
        if op == ">=":
            return TRUE_VALUE if v_l >= v_r else FALSE_VALUE

        # 산술 연산자
        if op == "+":
            res = v_l + v_r
            return FloatValue(res) if has_float else IntValue(res)
        if op == "-":
            res = v_l - v_r
            return FloatValue(res) if has_float else IntValue(res)
        if op == "*":
            res = v_l * v_r
            return FloatValue(res) if has_float else IntValue(res)
        if op == "/":
            if v_r == 0:
                raise RuntimeError("0으로 나눌 수 없습니다.", line=line, column=column, source_code=src)
            if has_float:
                return FloatValue(v_l / v_r)
            # 정수 나눗셈 (C/Java 계열 기본)
            return IntValue(v_l // v_r)
        if op == "%":
            if v_r == 0:
                raise RuntimeError("0으로 나눌 수 없습니다.", line=line, column=column, source_code=src)
            return FloatValue(v_l % v_r) if has_float else IntValue(v_l % v_r)
        if op == "**":
            res = v_l ** v_r
            return FloatValue(float(res)) if has_float else IntValue(int(res))

        # 비트 연산자 (정수 전용)
        if isinstance(left, (IntValue, LongValue)) and isinstance(right, (IntValue, LongValue)):
            i_l = int(v_l)
            i_r = int(v_r)
            if op == "&":
                return IntValue(i_l & i_r)
            if op == "|":
                return IntValue(i_l | i_r)
            if op == "^":
                return IntValue(i_l ^ i_r)
            if op == "<<":
                return IntValue(i_l << i_r)
            if op == ">>":
                return IntValue(i_l >> i_r)

        raise RuntimeError(
            f"알 수 없는 연산자입니다: '{op}'", line=line, column=column, source_code=src
        )

    def _is_equal(self, a: Value, b: Value) -> bool:
        if isinstance(a, NullValue) and isinstance(b, NullValue):
            return True
        if isinstance(a, NullValue) or isinstance(b, NullValue):
            return False

        if isinstance(a, (IntValue, LongValue, FloatValue)) and isinstance(b, (IntValue, LongValue, FloatValue)):
            return a.val == b.val

        if isinstance(a, (StringValue, CharValue)) and isinstance(b, (StringValue, CharValue)):
            return a.val == b.val

        if isinstance(a, BoolValue) and isinstance(b, BoolValue):
            return a.val == b.val

        return a is b
