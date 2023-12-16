import sympy as sp

rational = sp.Rational("-11/3")

print(divmod(rational, 1))

print(int(rational), abs(rational - int(rational)), sep="$")