from readers import read_corrupted_ledger_file
from utils import write_file
from max_like import find_best_perm

# 9:06 10:01
# 84.95871033578258 %

field_names = ['customer_id', 'age', 'amount']
debug = False


def run_solution_2():
    corrupted = read_corrupted_ledger_file()
    data_fixed = []
    for line in corrupted:
        values = list(line.values())
        row_fixed = find_best_perm([values])
        if debug:
            print('best', row_fixed.__repr__())
        data_fixed.append(row_fixed)

    write_file(data_fixed, 'data/ledger_fixed_2.csv')


if __name__ == "__main__":
    run_solution_2()
