from dataclasses import dataclass
from pathlib import Path

from sympy import Rational


@dataclass
class Node:
    channels_count: int
    mu: float | int


working_directory = Path(r"D:\Убежище\Университет\6 семестр\САПР\4\Сабонис\_Я_ (4)")
variant = 4
lambda_0 = Rational(7, 2)
nodes = [
    Node(channels_count=1, mu=7),
    Node(channels_count=1, mu=10),
    Node(channels_count=1, mu=6),
    Node(channels_count=3, mu=7)
]

transmission_matrix = [
    [Rational(0), Rational(1), Rational(0), Rational(0), Rational(0)],
    [Rational(7, 9), Rational(0), Rational(0), Rational(0), Rational(2, 9)],
    [Rational(0), Rational(8, 13), Rational(0), Rational(5, 13), Rational(0)],
    [Rational(0), Rational(0), Rational(4, 11), Rational(0), Rational(7, 11)],
    [Rational(0), Rational(0), Rational(3, 13), Rational(10, 13), Rational(0)],
]
