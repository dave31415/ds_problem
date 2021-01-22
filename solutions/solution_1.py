from solutions.file_io import read_corrupted_ledger_file
from solutions.file_io import write_file

# 8:35 to 8:43 about 10 minutes to write this (without documentation)
# 73.77279061625134 % lines correct

field_names = ['customer_id', 'age', 'amount']


def run_solution_1():
    """
    Very simple, very approximate, solution based on the idea that the age, amount and
    customer_id should typically be sorted in that order. There are
    10,000 lines. The sum of the amounts should be between 7 and 8 million.
    So amounts should average around 750
    Ages must be in range [18, 100]
    Customer ids should be a mostly-uniform distribution at least
    spread over the range 0 - 10,000.
    So sorting them and assigning them to age, amount, customer_id
    should be right most of the time.
    Also added a swap of age and amounts if age, determined
    in the above way is < 18.
    This ignores the issue of buffers and treats every line independently.
    It turns out that this manages to get 91% of the lines correct and
    recover 74% of the total.
    Combining information about 3-line buffers would ne a natural way to
    improve on this, i.e. choose the most common ordering if there is one.
    :return:
    """
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
