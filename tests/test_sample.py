# tests/test_sample.py
import sys

def test_environment():
    """Test that our basic environment is set up correctly"""
    assert True

def test_python_version():
    """Test that we're using the correct Python version"""
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 10
    print(f"Python version: {sys.version}")

def test_basic_math():
    """A simple test to verify basic functionality"""
    assert 5 + 5== 10