from solutions.file_io import read_corrupted_ledger_file, write_file
from solutions.file_io import batch_stream
from solutions.max_like import find_best_perm

# Over an hour
# 97.78753713962284 %


def run_solution_3():
    corrupted = read_corrupted_ledger_file()
    corrupted_batches = list(batch_stream(corrupted, 3))

    data_fixed = []
    for batch_number, rows_list in enumerate(corrupted_batches):
        values_list = [list(line.values()) for line in rows_list]
        row_fixed_list = find_best_perm(values_list)
        data_fixed.extend(row_fixed_list)

    write_file(data_fixed, 'data/ledger_fixed_3.csv')
