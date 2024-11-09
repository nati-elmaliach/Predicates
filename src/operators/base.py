from abc import ABC, abstractmethod
from typing import Any


class Operator(ABC):
    def __init__(self, operator: str) -> None:
        self.operator = operator

    @abstractmethod
    def evaluate(self, value: Any) -> bool:
        pass
