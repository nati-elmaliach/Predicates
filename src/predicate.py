from __future__ import annotations
from typing import Any, Dict, Type
import json
import re
from .operators import *
from types import SimpleNamespace

class Predicate():
    OPERATOR_MAP: Dict[str, Type[Operator]] = {
        "isNone": IsNoneOperator,
        "isNotNone": IsNotNoneOperator
    }

    def __init__(self, feature_path: str, operation: Operator) -> None:
        self.feature_path = feature_path
        self.operation = operation

    @classmethod
    def from_json(cls, json_string: str) -> Predicate:
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

        if not isinstance(data, dict):
            raise ValueError('JSON must decode to a dictionary')
        
        if "feature" not in data or "operation" not in data:
            raise ValueError("JSON must contain 'feature' and 'operation' fields")

        # TODO: more input validations
        feature = data["feature"]
        cls._validate_feature_path(feature)
        operation = cls._parse_operation(data["operation"])

        return cls(feature, operation)

    @classmethod
    def _validate_feature_path(cls, path: str) -> None:
        if path == '': return # Test against root

        pattern = r'^(\.[a-zA-Z][a-zA-Z0-9_]*)*$'
        if not re.match(pattern, path):
            raise ValueError(
                f"Invalid feature path: {path}. Must be empty or start with '.' "
                "followed by valid attribute names"
            )

    @classmethod
    def _parse_operation(cls, operation_dict: Dict[str, Any]) -> Any:
        operator = operation_dict["operator"]

        if operator not in cls.OPERATOR_MAP:
            raise ValueError(f"Unsupported operator: {operator}")
        
        operator_class = cls.OPERATOR_MAP[operator]

        if issubclass(operator_class, UnaryOperator):
            return operator_class(operator)
        
    def _get_feature_value(self, root: object) -> Any:
        if self.feature_path == '':
            return root

        # Instead of using a library, this also give us a bit optimization
        isDict = False
        if isinstance(root, dict):
            isDict = True

        try:
            current = root
            for attr in self.feature_path.split('.')[1:]:
                if isDict:
                    current = current[attr]
                else:
                    current = getattr(current, attr)
            return current
        except AttributeError:
            raise ValueError(f"Path does not exists {self.feature_path}")


    def evaluate(self, root: object) -> bool:
        # make sure the feature_path exists
        feature_value = self._get_feature_value(root)
        try:
            return self.operation.evaluate(feature_value)
        except Exception as e:
            raise ValueError(e)


        


