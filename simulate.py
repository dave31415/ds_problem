import csv
import numpy as np
import params
import readers

debug = False


def pick_two(n):
    all_nums = range(n)
    np.random.shuffle(all_nums)
    first = all_nums.pop()
    np.random.shuffle(all_nums)
    second = all_nums.pop()
    return first, second


def corrupt_file(file_name=None):
    if file_name is None:
        file_name = "%s/%s" % (params.data_dir, params.ledger_file)
    np.random.seed(params.random_seed)
    assert file_name.endswith('.csv')
    outfile = file_name.replace('.csv', '_corrupted.csv')
    data = csv.DictReader(open(file_name, 'rU'))
    field_names = data.fieldnames
    fnc = [f for f in data.fieldnames]
    n_fields = len(field_names)
    col_index = range(n_fields)
    out = open(outfile, 'w')
    line = ','.join(field_names)
    out.write(line+'\n')

    for line_num, data_dict in enumerate(data):
        # every time a new buffer block is written,
        # there is a chance of a mutation which swaps columns
        if np.random.random() < params.mutation_rate \
                and (line_num % params.buffer_length) == 0 \
                and line_num > 0:
            first, second = pick_two(n_fields)
            if debug:
                print 'line: %s swapping %s, %s: %s, %s' \
                      % (line_num, first, second, fnc[first], fnc[second])
            col_index[first], col_index[second] \
                = col_index[second], col_index[first]
            fnc[first], fnc[second] = fnc[second], fnc[first]

        data_line = [data_dict[i] for i in field_names]
        data_line_corrupted = [data_line[c] for c in col_index]
        line = ','.join(data_line_corrupted)
        out.write(line+'\n')


if __name__ == "__main__":
    readers.write_people_file()
    corrupt_file()
