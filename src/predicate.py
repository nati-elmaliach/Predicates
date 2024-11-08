from __future__ import annotations
import json


class Predicate():
    @classmethod
    def from_json(cls, json_string: str) -> Predicate:
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")
        
        if not isinstance(data, dict):
            raise ValueError('JSON must decode to a dictionary')
        
