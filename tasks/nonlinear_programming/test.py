if __name__ == '__main__':
    import plotter
    from sympy import symbols

    x1, x2 = symbols("x1 x2")
    plotter.add_linear_eq_limitation(4 * x2 - 8).show()