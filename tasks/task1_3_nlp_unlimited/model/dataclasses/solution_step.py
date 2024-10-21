from dataclasses import dataclass

from sympy import Rational


@dataclass
class SolutionStep:
    x1: Rational
    x2: Rational
    value: Rational
