import warnings

from docx import Document

from my_docx import docx_output
import sympy as sp
from sympy import Matrix, symbols

from my_docx.fillers.barrier_function_filler import BarrierFunctionDocxFiller
from my_docx.fillers.bill_filler import BillDocxFiller
from my_docx.fillers.frank_wolfe_filler import FrankWolfeDocxFiller
from my_docx.fillers.gradient_projection_filler import GradientProjectionDocxFiller
from my_docx.fillers.penalty_function_filler import PenaltyFunctionDocxFiller
from my_docx.fillers.possible_directions_filler import PossibleDirectionsDocxFiller
from my_docx.optimum_condition_filler import OptimumConditionDocxFiller
from my_io.io import folder
from task import Task
from methods.gradient_projection import GradientProjection
from methods.lagrange import Lagrange
from methods.penalty_funcition_method import PenaltyFunctionMethod
from methods.barrier_funcition_method import BarrierFunctionMethod
from methods.bill.bill import Bill
from methods.frank_wolfe.frank_wolfe import FrankWolfe
from methods.possible_directions import PossibleDirections

from my_docx.fillers.main_filler import main_data_producers
from my_docx.fillers.lagrange_filler import LagrangeDocxFiller

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    x1, x2 = symbols('x1 x2')

    lagrange = Lagrange()
    bill = Bill()
    gradient_projection = GradientProjection()
    possible_directions = PossibleDirections()
    barrier_function = BarrierFunctionMethod()
    penalty_function = PenaltyFunctionMethod()
    frank_wolfe = FrankWolfe()

    lagrange.solve(f=Task.f, limitation=Task.lim5)
    bill.solve(f=Task.f, limitations=Task.lim1234)
    gradient_projection.solve(f=Task.f, limitations=Task.lim1234)
    possible_directions.solve(f=Task.f, limits_le=Task.lim67)
    barrier_function.solve(f=Task.f, limitations=Task.lim1234, start=sp.Matrix([1, 2]))
    penalty_function.solve(f=Task.f, limitations=Task.lim1234, start=Matrix([14, 7]))
    frank_wolfe.solve(f=Task.f, limitations=Task.lim1234)

    lagrange.show_plot()
    bill.save_plot('./report_data/bill.png')
    gradient_projection.save_plot('./report_data/gradient_projection.png')
    possible_directions.save_plot('./report_data/possible_directions.png')
    penalty_function.save_plot('./report_data/penalty_function.png')
    barrier_function.save_plot('report_data/barrier_function.png')
    frank_wolfe.save_plot('report_data/frank_wolfe.png')

    template = Document('open_system_template.docx')
    optimum_condition_filler = OptimumConditionDocxFiller().get_data_producers()
    lagrange_data_producers = LagrangeDocxFiller(lagrange).get_data_producers()
    bill_data_producers = BillDocxFiller(bill).get_data_producers()
    gradient_projection_data_producers = GradientProjectionDocxFiller(gradient_projection).get_data_producers()
    possible_directions_data_producers = PossibleDirectionsDocxFiller(possible_directions).get_data_producers()
    penalty_function_data_producers = PenaltyFunctionDocxFiller(penalty_function).get_data_producers()
    barrier_function_data_producers = BarrierFunctionDocxFiller(barrier_function).get_data_producers()
    frank_wolfe_data_producers = FrankWolfeDocxFiller(frank_wolfe).get_data_producers()
    result_data_producers = {
        **optimum_condition_filler,
        **main_data_producers,
        **lagrange_data_producers,
        **bill_data_producers,
        **gradient_projection_data_producers,
        **possible_directions_data_producers,
        **penalty_function_data_producers,
        **barrier_function_data_producers,
        **frank_wolfe_data_producers}
    docx_output.fill_template(template=template, data_producers=result_data_producers)
    template.save(f'{folder}/output.docx')

    print()
    print(f'Метод Билла = {round(float(bill.solution["f"]), 4)}')
    print(f'Метод проекции градиента = {round(float(gradient_projection.solution["f"]), 4)}')
    print(f'Метод Франка-Вульфа = {round(float(frank_wolfe.solution["f"]), 4)}')
    print()
    print(f'Метод возможных направлений = {round(float(possible_directions.solution["f"]), 4)}')
    print(f'Метод штрафных функций = {round(float(penalty_function.solution["f"]), 4)}')
    print(f'Метод барьерных функций = {round(float(barrier_function.solution["f"]), 4)}')
