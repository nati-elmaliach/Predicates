from typing import Any
from .base import Operator

class UnaryOperator(Operator):
    def __init__(self, operator: str) -> None:
        super().__init__(operator)

class IsNoneOperator(UnaryOperator):
    def evaluate(self, value: Any) -> bool:
        return value is None
    
class IsNotNoneOperator(UnaryOperator):
    def evaluate(self, value: Any) -> bool:
        return value is not None