import pytest
import json
from dataclasses import dataclass
from types import SimpleNamespace
from src import Predicate

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

def test_binary_notEqTo_True():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "notEqTo", "operand": 5}}''')
    result = predicate.evaluate({ "x": { "y": 1} })
    assert result is True

def test_binary_notEqTo_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "notEqTo", "operand": 5}}''')
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
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "or", "operations": [ {"operator": "notEqTo", "operand": 1}, {"operator": "isLessThan", "operand": 1 } ]}}''')
    result = predicate.evaluate({ "x": { "y": 6} })
    assert result is True

def test_group_or_False():
    predicate = Predicate.from_json('''{"feature": ".x.y", "operation": {"operator": "or", "operations": [ {"operator": "eqTo", "operand": 9}, {"operator": "isGreaterThan", "operand": 9 } ]}}''')
    result = predicate.evaluate({ "x": { "y": 6} })
    assert result is False

def test_dataclass_objects():
    @dataclass
    class User:
        name: str
        level: int

    @dataclass
    class Game:
        user: User

    g = Game(user=User(name="bob", level=6))
    
    pred_str = '{"feature": ".user.name", "operation": {"operator": "eqTo", "operand": "bob"}}'
    pred = Predicate.from_json(pred_str)
    assert pred.evaluate(g) is True

    pred_str2 = '''{"feature": ".user.level", "operation": {"operator": "isLessThan", "operand": 3.6}}'''
    pred = Predicate.from_json(pred_str2)
    assert pred.evaluate(g) is False

def test_complex_examples():
    # Check if a number is:
    # Level 1 (AND):
    #   - not null AND
    #   - Level 2 (OR):
    #       - exactly 100 OR
    #       - Level 3 (AND):
    #           - greater than 0 AND
    #           - less than 50 AND
    #           - not equal to 25
    #       - Level 3 (AND):
    #           - greater than 75 AND
    #           - less than 90
    deep_nested = {
        "feature": ".value",
        "operation": {
            "operator": "and",
            "operations": [
                {"operator": "isNotNone"},
                {
                    "operator": "or",
                    "operations": [
                        {"operator": "eqTo", "operand": 100},
                        {
                            "operator": "and",
                            "operations": [
                                {"operator": "isGreaterThan", "operand": 0},
                                {"operator": "isLessThan", "operand": 50},
                                {"operator": "notEqTo", "operand": 25}
                            ]
                        },
                        {
                            "operator": "and",
                            "operations": [
                                {"operator": "isGreaterThan", "operand": 75},
                                {"operator": "isLessThan", "operand": 90}
                            ]
                        }
                    ]
                }
            ]
        }
    }

    pred = Predicate.from_json(json.dumps(deep_nested))
    
    # Test cases
    # Should pass (exactly 100)
    assert pred.evaluate(SimpleNamespace(value=100)) is True
    
    # Should pass (between 0 and 50, not 25)
    assert pred.evaluate(SimpleNamespace(value=30)) is True
    
    # Should pass (between 75 and 90)
    assert pred.evaluate(SimpleNamespace(value=80)) is True
    
    # Should fail (equals 25)
    assert pred.evaluate(SimpleNamespace(value=25)) is False
    
    # Should fail (None value)
    assert pred.evaluate(SimpleNamespace(value=None)) is False
    
    # Should fail (outside all ranges)
    assert pred.evaluate(SimpleNamespace(value=60)) is False
    
    # Should fail (outside all ranges)
    assert pred.evaluate(SimpleNamespace(value=95)) is False