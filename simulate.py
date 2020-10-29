import csv
import numpy as np
import params
import readers
from utils import write_file


debug = False
field_names = ['customer_id', 'age', 'amount']


def pick_two(n):
    all_nums = list(range(n))
    np.random.shuffle(all_nums)
    first = all_nums.pop()
    np.random.shuffle(all_nums)
    second = all_nums.pop()
    return first, second


def corrupt_file(file_name=None):
    if file_name is None:
        file_name = "%s/%s" % (params.data_dir, params.ledger_file)

    np.random.seed(params.random_seed)

    data = list(csv.DictReader(open(file_name, 'r')))

    fnc = [f for f in field_names]
    n_fields = len(field_names)
    col_index = list(range(n_fields))

    corrupted_data = []
    for line_num, data_dict in enumerate(data):
        # every time a new buffer block is written,
        # there is a chance of a mutation which swaps columns
        if np.random.random() < params.mutation_rate \
                and (line_num % params.buffer_length) == 0 \
                and line_num > 0:

            first, second = pick_two(n_fields)
            col_index[first], col_index[second] \
                = col_index[second], col_index[first]
            fnc[first], fnc[second] = fnc[second], fnc[first]

        data_line = [data_dict[i] for i in field_names]
        data_line_corr = [data_line[c] for c in col_index]

        row_corrupted = {k: v for k, v in zip(field_names, data_line_corr)}
        corrupted_data.append(row_corrupted)

    assert file_name.endswith('.csv')
    outfile = file_name.replace('.csv', '_corrupted.csv')
    write_file(corrupted_data, outfile)


if __name__ == "__main__":
    readers.write_people_file()
    corrupt_file()
