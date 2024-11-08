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

# Also test for dict as input
def test_unary_isNone():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "isNone"}}''')
    result = predicate.evaluate({ "x": { "y": None} })
    assert result is True

def test_unary_isNone_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "isNone"}}''')
    result = predicate.evaluate({ "x": { "y": 1} })
    assert result is False

def test_unary_isNotNone_True():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "isNotNone"}}''')
    result = predicate.evaluate({ "x": { "y": 1} })
    assert result is True

def test_unary_isNotNone_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "isNotNone"}}''')
    result = predicate.evaluate({ "x": { "y": None} })
    assert result is False

def test_binary_eqTo_True():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "eqTo", operand: 5}}''')
    result = predicate.evaluate({ "x": { "y": 5} })
    assert result is True