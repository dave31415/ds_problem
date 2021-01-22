from solutions.file_io import read_corrupted_ledger_file
from solutions.file_io import write_file

# 8:35 to 8:43 about 10 minutes
# 73.77279061625134

field_names = ['customer_id', 'age', 'amount']


def run_solution_1():
    corrupted = read_corrupted_ledger_file()
    data_fixed = []
    for line in corrupted:
        values = [int(i) for i in list(line.values())]
        values_sorted = sorted(values)
        cust_id = values_sorted[2]
        age = values_sorted[0]
        amount = values_sorted[1]

        if age < 18:
            # swap age and amount, helps very little
            age, amount = amount, age

        values_fixed = [cust_id, age, amount]
        row_fixed = {k: v for k, v in zip(field_names, values_fixed)}
        data_fixed.append(row_fixed)

    write_file(data_fixed, 'data/ledger_fixed_1.csv')
