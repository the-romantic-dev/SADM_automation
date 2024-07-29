from dataclasses import dataclass
from pathlib import Path

from sympy import Rational


@dataclass
class Node:
    channels_count: int
    mu: float | int


working_directory = Path(r"D:\Убежище\Университет\6 семестр\САПР\4\Сабонис\test")
variant = 4
nodes = [
    Node(channels_count=2, mu=8),
    Node(channels_count=2, mu=9),
    Node(channels_count=2, mu=8),
    Node(channels_count=3, mu=1)
]

requests_number = 4
transmission_matrix = [
    [Rational(125, 1000), Rational(625, 1000), Rational(625, 10000), Rational(1875, 10000)],
    [Rational(4, 10), Rational(0), Rational(6, 10), Rational(0)],
    [Rational(7692, 10000), Rational(1538, 10000), Rational(0), Rational(769, 10000)],
    [Rational(0), Rational(5833, 10000), Rational(4167, 10000), Rational(0)]
]
