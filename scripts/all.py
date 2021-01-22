from scripts.simulate import main as main_sim
from scripts.plots import main as main_plots
from scripts.solution_1 import main as main_sol_1
from scripts.solution_2 import main as main_sol_2
from scripts.solution_3 import main as main_sol_3
from scripts.solution_4 import main as main_sol_4
from scripts.validate import main as main_validate


def main(*args):
    main_sim()
    main_plots()
    main_sol_1()
    main_sol_2()
    main_sol_3()
    main_sol_4()
    main_validate('data/ledger_fixed_1.csv', 'score')
    main_validate('data/ledger_fixed_2.csv', 'score')
    main_validate('data/ledger_fixed_3.csv', 'score')
    main_validate('data/ledger_fixed_4.csv', 'score')
