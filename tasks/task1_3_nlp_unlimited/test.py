from sympy import Rational, Matrix
from tasks.task1_3_nlp_unlimited.model.methods import RapidAscentMethod

from tasks.task1_3_nlp_unlimited.model import NLPObjective
from tasks.task1_3_nlp_unlimited.model.univariate_step_size_finder import UnivariateStepSizeFinder

objective = NLPObjective(coeffs=[
    Rational(-14), Rational(-26), Rational(16), Rational(84), Rational(252)
])
start_point = Matrix([6, 5])

# methods = [BroydenMethod(objective), ConjugateGradientMethod(objective), RelaxationMethod(objective),
#            RapidAscentMethod(objective), NewtonMethod(objective), DFPMethod(objective),
# ]
#
# for abstract in methods:
#     print(f"abstract: {abstract.__class__.__name__}")
#     solution = abstract.solve(start_point)
#     for s in solution:
#         print(f'\t{s}')
method = RapidAscentMethod(objective)
k = method.step_direction(start_point, prev_point=None, step_num=0)
finder = UnivariateStepSizeFinder(objective, start_point, k)
interval_steps = finder.start_interval_steps
print(interval_steps)
print(finder.golden_section_method_steps(interval_steps[-1]))

