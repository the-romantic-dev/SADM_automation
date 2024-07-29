import pytest

# from tasks.task1_2_lp.solvers.bruteforce_solver.bruteforce_solver import \


@pytest.mark.parametrize(
    "total_vars, basis_size, expected",
    [
        (4, 2, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
        (5, 2, [
            (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 2), (1, 3), (1, 4),
            (2, 3), (2, 4), (3, 4)]
         ),
        (0, 0, [()]),
        (1, 1, [(0,)]),
        (2, 3, []),
        (15, -1, [])
    ]
)
def test_get_basis_list(total_vars, basis_size, expected):
    assert _get_basis_list(total_vars, basis_size) == expected


@pytest.mark.parametrize(
    "basis, all_vars, expected",
    [
        ((2, 3), [0, 1, 2, 3], (0, 1)),
        ((1, 3), [0, 1, 2, 3], (0, 2)),
     ]
)
def test_get_free(basis, all_vars, expected):
    assert _get_free(basis, all_vars) == expected

