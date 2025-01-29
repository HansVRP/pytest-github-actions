import pytest

def test_pass():
    """A dummy test that always passes"""
    assert True

def test_fail():
    """A dummy test that always fails"""
    assert False

def test_random():
    """A test that sometimes fails"""
    import random
    assert random.choice([True, False])