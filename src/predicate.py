from __future__ import annotations
import json
import re
from typing import Any


class Predicate():
    def __init__(self, feature: str, operation: Any) -> None:
        self.feature = feature
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

        cls._validate_feature_path(data["feature"])


    @classmethod
    def _validate_feature_path(cls, path: str) -> None:
        if path == '': return # Test against root

        pattern = r'^(\.[a-zA-Z][a-zA-Z0-9_]*)*$'
        if not re.match(pattern, path):
            raise ValueError(
                f"Invalid feature path: {path}. Must be empty or start with '.' "
                "followed by valid attribute names"
            )

        
