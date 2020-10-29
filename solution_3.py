from readers import read_corrupted_ledger_file
from utils import write_file, batch_stream
from max_like import find_best_perm

# Over an hour
# 97.78753713962284 %

field_names = ['customer_id', 'age', 'amount']
debug = False


def run_solution_2():
    corrupted = read_corrupted_ledger_file()
    corrupted_batches = list(batch_stream(corrupted, 3))

    data_fixed = []
    for batch_number, rows_list in enumerate(corrupted_batches):
        values_list = [list(line.values()) for line in rows_list]
        row_fixed_list = find_best_perm(values_list)
        data_fixed.extend(row_fixed_list)

    write_file(data_fixed, 'data/ledger_fixed_3.csv')


if __name__ == "__main__":
    run_solution_2()
