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
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "eqTo", "operand": 5}}''')
    result = predicate.evaluate({ "x": { "y": 5} })
    assert result is True

def test_binary_eqTo_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "eqTo", "operand": 5}}''')
    result = predicate.evaluate({ "x": { "y": 2} })
    assert result is False

def test_binary_notEqualTo_True():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "notEqualTo", "operand": 5}}''')
    result = predicate.evaluate({ "x": { "y": 1} })
    assert result is True

def test_binary_notEqualTo_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "notEqualTo", "operand": 5}}''')
    result = predicate.evaluate({ "x": { "y": 5} })
    assert result is False

def test_binary_isLessThan_True():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "isLessThan", "operand": 5}}''')
    result = predicate.evaluate({ "x": { "y": 1} })
    assert result is True

def test_binary_isLessThan_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "isLessThan", "operand": 5}}''')
    result = predicate.evaluate({ "x": { "y": 6} })
    assert result is False

def test_binary_isGreaterThan_True():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "isGreaterThan", "operand": 5}}''')
    result = predicate.evaluate({ "x": { "y": 6} })
    assert result is True

def test_binary_isGreaterThan_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "isGreaterThan", "operand": 5}}''')
    result = predicate.evaluate({ "x": { "y": 1} })
    assert result is False

def test_group_and_True():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "and", "operations": [ {"operator": "isNotNone"}, {"operator": "isLessThan", "operand": 9 } ]}}''')
    result = predicate.evaluate({ "x": { "y": 6} })
    assert result is True

def test_group_and_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "and", "operations": [ {"operator": "isNotNone"}, {"operator": "isGreaterThan", "operand": 9 } ]}}''')
    result = predicate.evaluate({ "x": { "y": 6} })
    assert result is False

def test_group_or_True():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "or", "operations": [ {"operator": "notEqualTo", "operand": 1}, {"operator": "isLessThan", "operand": 1 } ]}}''')
    result = predicate.evaluate({ "x": { "y": 6} })
    assert result is True

def test_group_or_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "or", "operations": [ {"operator": "eqTo", "operand": 9}, {"operator": "isGreaterThan", "operand": 9 } ]}}''')
    result = predicate.evaluate({ "x": { "y": 6} })
    assert result is False