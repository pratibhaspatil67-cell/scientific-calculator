# calculator/core.py
import math

def sqrt(x: float) -> float:
    if x < 0:
        raise ValueError("sqrt requires a non-negative number")
    return math.sqrt(x)

def factorial(n: int) -> int:
    if not isinstance(n, int) or n < 0:
        raise ValueError("factorial requires a non-negative integer")
    return math.factorial(n)

def ln(x: float) -> float:
    if x <= 0:
        raise ValueError("ln requires a positive number")
    return math.log(x)

def power(x: float, b: float) -> float:
    return math.pow(x, b)

