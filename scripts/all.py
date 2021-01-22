from scripts.simulate import main as main_sim
from scripts.plots import main as main_plots
from scripts.solution_1 import main as main_sol_1
from scripts.solution_2 import main as main_sol_2
from scripts.solution_3 import main as main_sol_3
from scripts.solution_4 import main as main_sol_4
from scripts.validate import main as main_validate


def hash_it(v):
    hash_val = str(v % 1)[2:]
    return ''.join(list(reversed(hash_val)))


def main(*args):
    main_sim()
    main_plots()
    main_sol_1()
    main_sol_2()
    main_sol_3()
    main_sol_4()
    v1 = main_validate('data/ledger_fixed_1.csv', 'score')
    v2 = main_validate('data/ledger_fixed_2.csv', 'score')
    v3 = main_validate('data/ledger_fixed_3.csv', 'score')
    v4 = main_validate('data/ledger_fixed_4.csv', 'score')

    # print a hash val to indicate any change to performance metrics
    # should print 2950076768751078
    # if not, a change occurred that effected the metrics
    # (or someone forgot to update the above)
    # This aids in refactoring

    hash_val = hash_it(v1*v2*v3*v4)
    print('hash_val: %s' % hash_val)
