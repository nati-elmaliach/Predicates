from __future__ import annotations

import json
import re
from typing import Any, Dict, Type, TypedDict, cast

from .operators import *


class PredicateData(TypedDict):
    feature: str
    operation: Dict[str, Any]


class Predicate:
    OPERATOR_MAP: Dict[str, Type[Operator]] = {
        "isNone": IsNoneOperator,
        "isNotNone": IsNotNoneOperator,
        "eqTo": EqualTo,
        "notEqTo": notEqTo,
        "isLessThan": IsLessThan,
        "isGreaterThan": IsGreaterThan,
        "and": AndOperator,
        "or": OrOperator,
    }

    def __init__(self, feature_path: str, operation: Operator) -> None:
        self.feature_path = feature_path
        self.operation = operation

    @classmethod
    def from_json(cls, json_string: str) -> Predicate:
        data = cls.parse_json(json_string)
        feature, operation_dict = data["feature"], data["operation"]

        cls._validate_feature_path(feature)
        operation = cls._parse_operation(operation_dict)

        return cls(feature, operation)

    @classmethod
    def parse_json(cls, json_string: str) -> PredicateData:
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

        if not isinstance(data, dict):
            raise ValueError("JSON must decode to a dictionary")

        if "feature" not in data or "operation" not in data:
            raise ValueError("JSON must contain 'feature' and 'operation' fields")

        if not isinstance(data["feature"], str) or not isinstance(
            data["operation"], dict
        ):
            raise ValueError(
                "'feature' must be a string and 'operation' must be a dict"
            )

        return cast(PredicateData, data)

    @classmethod
    def _validate_feature_path(cls, path: str) -> None:
        if path == "":
            return  # Test against root

        pattern = r"^(\.[a-zA-Z][a-zA-Z0-9_]*)*$"
        if not re.match(pattern, path):
            raise ValueError(
                f"Invalid feature path: {path}. Must be empty or start with '.' "
                "followed by valid attribute names"
            )

    @classmethod
    def _parse_operation(cls, operation_dict: Dict[str, Any]) -> Operator:
        operator = operation_dict["operator"]

        if operator not in cls.OPERATOR_MAP:
            raise ValueError(f"Unsupported operator: {operator}")

        operator_class = cls.OPERATOR_MAP[operator]

        if issubclass(operator_class, UnaryOperator):
            return operator_class(operator)

        if issubclass(operator_class, BinaryOperator):
            if "operand" not in operation_dict:
                raise ValueError(f"Binary operator {operator} requires an operand")
            return operator_class(operator, operation_dict["operand"])

        if issubclass(operator_class, GroupOperator):
            if "operations" not in operation_dict:
                raise ValueError(f"Group operator {operator} requires operations list")
            operations = [
                cls._parse_operation(op) for op in operation_dict["operations"]
            ]
            return operator_class(operator, operations)

        raise ValueError(f"Unknown operator type: {operator}")

    def _get_feature_value(self, root: object) -> Any:
        if not self.feature_path:
            return root  # Test against root

        current = root
        for attr in self.feature_path.split(".")[1:]:
            try:
                if isinstance(current, dict):
                    current = current[attr]
                else:
                    current = getattr(current, attr)
            except AttributeError:
                raise AttributeError(f"Path does not exists {self.feature_path}")

        return current

    def evaluate(self, root: object) -> bool:
        try:
            feature_value = self._get_feature_value(root)
        except AttributeError:
            # If a feature does not exist, return False as the predicate fails.
            return False

        try:
            return self.operation.evaluate(feature_value)
        except Exception as e:
            raise ValueError(e)
