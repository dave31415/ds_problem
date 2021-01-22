from solutions.file_io import read_corrupted_ledger_file
from solutions.file_io import write_file
from solutions.max_like import find_best_perm

# 9:06 10:01
# 59.22006446068493 %


def run_solution_2():
    corrupted = read_corrupted_ledger_file()
    data_fixed = []
    for line in corrupted:
        values = list(line.values())
        rows_fixed, probability, _ = find_best_perm([values])
        data_fixed.extend(rows_fixed)

    write_file(data_fixed, 'data/ledger_fixed_2.csv')
