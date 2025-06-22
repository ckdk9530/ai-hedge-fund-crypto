import pytest
from ..utils.util_func import deep_merge_dicts


def test_deep_merge_dicts_basic():
    a = {"a": 1, "b": 2, "c": 3, "config": {"a": 1, "b": 2, "c": 3}}
    b = {"a": 2, "config": {"a": 2, "d": 3, "data": {"key": "value"}}}
    expected = {
        "a": 2,
        "b": 2,
        "c": 3,
        "config": {"a": 2, "b": 2, "c": 3, "d": 3, "data": {"key": "value"}},
    }
    assert deep_merge_dicts(a, b) == expected


def test_deep_merge_dicts_nested():
    a = {"x": {"y": {"z": 1}}, "common": {"a": 1}}
    b = {"x": {"y": {"w": 2}}, "common": {"b": 2}}
    expected = {"x": {"y": {"z": 1, "w": 2}}, "common": {"a": 1, "b": 2}}
    assert deep_merge_dicts(a, b) == expected
