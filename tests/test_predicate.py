from src import Predicate
import pytest

def test_invalid_json():
    with pytest.raises(ValueError):
        Predicate.from_json("invalid json")

def test_valid_dict():
    with pytest.raises(ValueError):
        Predicate.from_json("[]")

def test_valid_dict_keys():
    with pytest.raises(ValueError):
        Predicate.from_json('''{"feature": ".x.y" }''')

def test_feature_path():
    with pytest.raises(ValueError):
        Predicate.from_json('''{"feature": "x.y", "operation": {"operator": "isNotNone"}}''')

def test_invalid_operation():
    with pytest.raises(ValueError):
        Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "xor"}}''')