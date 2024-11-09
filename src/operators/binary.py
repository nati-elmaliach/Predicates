from typing import Any

from src.operators.base import Operator


class BinaryOperator(Operator):
    def __init__(self, operator: str, operand: Any) -> None:
        self.operand = operand
        super().__init__(operator)


class EqualTo(BinaryOperator):
    def evaluate(self, value: Any) -> bool:
        return value == self.operand


class notEqTo(BinaryOperator):
    def evaluate(self, value: Any) -> bool:
        return value != self.operand


class IsLessThan(BinaryOperator):
    def evaluate(self, value: Any) -> bool:
        return value < self.operand


class IsGreaterThan(BinaryOperator):
    def evaluate(self, value: Any) -> bool:
        return value > self.operand
