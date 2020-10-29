from readers import read_corrupted_ledger_file
from utils import write_file
from max_like import find_best_perm

# 9:06 10:01
# 59.22006446068493 %

field_names = ['customer_id', 'age', 'amount']
debug = False


def run_solution_2():
    corrupted = read_corrupted_ledger_file()
    data_fixed = []
    for line in corrupted:
        values = list(line.values())
        rows_fixed = find_best_perm([values])
        if debug:
            print('best', rows_fixed.__repr__())
        data_fixed.extend(rows_fixed)

    write_file(data_fixed, 'data/ledger_fixed_2.csv')


if __name__ == "__main__":
    run_solution_2()
