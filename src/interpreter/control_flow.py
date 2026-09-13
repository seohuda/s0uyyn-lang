from typing import Optional
from src.runtime.values import Value, NULL_VALUE


class ControlFlowSignal(Exception):
    """제어 흐름 시그널 기본 클래스"""
    pass


class BreakSignal(ControlFlowSignal):
    """'말걸지마세요' (break) 시그널"""
    pass


class ContinueSignal(ControlFlowSignal):
    """'꺼져ㅗ' (continue) 시그널"""
    pass


class ReturnSignal(ControlFlowSignal):
    """'울산행KTX' (return) 시그널"""

    def __init__(self, value: Optional[Value] = None):
        self.value: Value = value if value is not None else NULL_VALUE
        super().__init__()
