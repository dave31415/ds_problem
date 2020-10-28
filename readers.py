import csv
import numpy as np
import params
from collections import Counter
from math import exp
from random import Random
import os
data_dir = 'data'


def make_id_picker():
    rand = Random()
    rand.seed(37464)
    num_lines = params.num_lines
    n = int(2.8 * num_lines)
    ids = list(range(n))
    rand.shuffle(ids)
    ids = ids[0:num_lines]
    stream = (i for i in ids)

    def picker():
        return next(stream)

    return picker


def make_person_picker():
    """
    Pick out a random person using all the files
    :return: a chosen Person object (well dictionary)
    """

    id_picker = make_id_picker()

    print(params)

    def pick():
        age_sigma = params.age_sigma
        age = params.age_min + age_sigma*abs(np.random.randn())
        age = int(round(age))

        amount = 0.0
        if np.random.random() > params.amount_percent_zero:
            random_normal = params.amount_lognormal_mu \
                + np.random.randn()*params.amount_lognormal_sigma
            amount = np.exp(random_normal)

        amount = round(amount)

        return {'age': age,
                'amount': int(amount),
                'customer_id': id_picker()}

    return pick


def write_people_file(num=params.num_lines):
    """
    Writes a file of People, the main input file before corruption
    :param num: number of lines to write
    :return: None
    """
    np.random.seed(params.random_seed)
    person_picker = make_person_picker()
    people = [person_picker() for _ in range(num)]
    total_amount = sum([float(p['amount']) for p in people])
    print("Total amount: %0.2f million" % (total_amount/1e6))
    print("Average amount: %0.2f" % (total_amount/float(len(people))))
    field_names = ['customer_id', 'age', 'amount']
    outfile = "%s/%s" % (params.data_dir, params.ledger_file)
    dw = csv.DictWriter(open(outfile, 'w'), delimiter=',',
                        fieldnames=field_names)
    dw.writeheader()
    dw.writerows(people)


def read_ledger_file():
    """
    Read the uncorrupted ledger.csv file
    :return: list of Person dicts
    """
    file_name = "%s/%s" % (params.data_dir, params.ledger_file)
    if not os.path.exists(file_name):
        print('File: %s not found' % file_name)
        return []

    return list(csv.DictReader(open(file_name, 'r')))


def read_corrupted_ledger_file():
    """
    Returns a generator to the corrupted data file
    :return:
    """
    file_name = "%s/%s" % (params.data_dir, 'ledger_corrupted.csv')
    return list(csv.DictReader(open(file_name, 'r')))


def stream_buffers():
    """
    :param buffer_size:
    :return:
    """
    reader = read_corrupted_people_file()
    buffer = []
    for line_num, line in enumerate(reader):
        buffer.append(line)
        if (line_num+1) % params.buffer_length == 0 and line_num > 0:
            output = [b for b in buffer]
            buffer = []
            yield output
    if len(buffer) > 0:
        yield buffer


if __name__ == "__main__":
    write_people_file()
