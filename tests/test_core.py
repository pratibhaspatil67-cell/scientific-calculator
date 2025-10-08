# tests/test_core.py
import math
import pytest
from calculator.core import sqrt, factorial, ln, power

def test_sqrt():
    assert sqrt(4) == pytest.approx(2.0)
    assert sqrt(0) == 0.0
    with pytest.raises(ValueError):
        sqrt(-1)

def test_factorial():
    assert factorial(5) == 120
    with pytest.raises(ValueError):
        factorial(-1)
    with pytest.raises(ValueError):
        factorial(3.5)

def test_ln():
    assert ln(math.e) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        ln(0)

def test_power():
    assert power(2, 3) == pytest.approx(8.0)
    assert power(9, 0.5) == pytest.approx(3.0)

