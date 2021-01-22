from solutions.file_io import read_corrupted_ledger_file
from solutions.file_io import write_file
from solutions.max_like import find_best_perm

# 9:06 10:01
# 59.22006446068493 %


def run_solution_2():
    """
    This technique has been refactored since it is now a simple case of
    solution_3 where we use a 1-row buffer and do it line by line,
    rather than buffer by buffer. It is a maximum likelihood
    technique. This method was in fact designed only a stop on the way
    to solution_3.
    See solution_3 documentation.
    :return:
    """
    corrupted = read_corrupted_ledger_file()
    data_fixed = []
    for line in corrupted:
        values = list(line.values())
        rows_fixed, probability, _ = find_best_perm([values])
        data_fixed.extend(rows_fixed)

    write_file(data_fixed, 'data/ledger_fixed_2.csv')
