

from src.operators.base import Operator
from typing import Any, List

class GroupOperator(Operator):
    def __init__(self, operator: str, operations: List[Operator]) -> None:
        self.operations = operations
        super().__init__(operator)

class AndOperator(GroupOperator):
    def evaluate(self, value: Any) -> bool:
        try:
            return all(op.evaluate(value) for op in self.operations)
        except Exception as e:
            print(f"Error in AndOperator: {e}")
            return False
        
class OrOperator(GroupOperator):
    def evaluate(self, value: Any) -> bool:
        try:
            return any(op.evaluate(value) for op in self.operations)
        except Exception as e:
            print(f"Error in OrOperator: {e}")
            return False