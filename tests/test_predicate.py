from src import Predicate
import pytest

def test_invalid_json():
    with pytest.raises(ValueError):
        Predicate.from_json("invalid json")


def test_valid_dict():
    with pytest.raises(ValueError):
        Predicate.from_json("[]")
