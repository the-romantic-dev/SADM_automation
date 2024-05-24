from dataclasses import dataclass
from pathlib import Path

from sympy import Rational


@dataclass
class Node:
    channels_count: int
    mu: float | int


working_directory = Path(r"D:\Убежище\Университет\6 семестр\САПР\4\Сабонис\Удалов (48)")
variant = 48
nodes = [
    Node(channels_count=3, mu=8),
    Node(channels_count=3, mu=1),
    Node(channels_count=3, mu=8),
    Node(channels_count=3, mu=8)
]

requests_number = 5
transmission_matrix = [
    [Rational(4, 15), Rational(0), Rational(2, 3), Rational(1, 15)],
    [Rational(0), Rational(0), Rational(1), Rational(0)],
    [Rational(1), Rational(0), Rational(0), Rational(0)],
    [Rational(0), Rational(1), Rational(0), Rational(0)]
]
