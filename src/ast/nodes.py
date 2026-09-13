from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class ASTNode:
    line: int = 1
    column: int = 1


@dataclass
class Program(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)


@dataclass
class BlockStmt(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)


@dataclass
class VariableDecl(ASTNode):
    type_name: str = ""
    name: str = ""
    init: Optional[ASTNode] = None
    is_const: bool = False


@dataclass
class Assignment(ASTNode):
    target: ASTNode = None  # Identifier, IndexExpr, or MemberExpr
    value: ASTNode = None


@dataclass
class ExpressionStmt(ASTNode):
    expr: ASTNode = None


@dataclass
class IfStmt(ASTNode):
    condition: ASTNode = None
    then_branch: ASTNode = None
    else_branch: Optional[ASTNode] = None


@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode = None
    body: ASTNode = None


@dataclass
class ForStmt(ASTNode):
    init: Optional[ASTNode] = None
    condition: Optional[ASTNode] = None
    update: Optional[ASTNode] = None
    body: ASTNode = None


@dataclass
class BreakStmt(ASTNode):
    pass


@dataclass
class ContinueStmt(ASTNode):
    pass


@dataclass
class ReturnStmt(ASTNode):
    value: Optional[ASTNode] = None


@dataclass
class Param:
    name: str
    type_name: Optional[str] = None


@dataclass
class FunctionDecl(ASTNode):
    name: str = ""
    params: List[Param] = field(default_factory=list)
    body: BlockStmt = None
    return_type: Optional[str] = None


@dataclass
class ClassDecl(ASTNode):
    name: str = ""
    fields: List[VariableDecl] = field(default_factory=list)
    methods: List[FunctionDecl] = field(default_factory=list)


# Expressions
@dataclass
class Literal(ASTNode):
    value: Any = None
    raw: str = ""
    type_hint: str = ""  # 'int', 'float', 'string', 'char', 'bool', 'null'


@dataclass
class Identifier(ASTNode):
    name: str = ""


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode = None
    op: str = ""
    right: ASTNode = None


@dataclass
class UnaryOp(ASTNode):
    op: str = ""
    operand: ASTNode = None
    is_prefix: bool = True


@dataclass
class UpdateExpr(ASTNode):
    target: ASTNode = None
    op: str = ""  # '++' or '--'
    is_prefix: bool = False


@dataclass
class CallExpr(ASTNode):
    callee: ASTNode = None
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class ArrayLiteral(ASTNode):
    elements: List[ASTNode] = field(default_factory=list)


@dataclass
class IndexExpr(ASTNode):
    target: ASTNode = None
    index: ASTNode = None


@dataclass
class MemberExpr(ASTNode):
    target: ASTNode = None
    member: str = ""
