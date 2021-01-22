import csv
from simulate.readers import read_ledger_file, read_corrupted_ledger_file

debug = False


def validate_file(file_name, use_corrupted=False):
    ledger_corrected = list(csv.DictReader(open(file_name, 'r')))
    return validate_ledger(ledger_corrected, use_corrupted=use_corrupted)


def validate_ledger(ledger_corrected, use_corrupted=True):
    if use_corrupted:
        print('Using corrupted file as original file just '
              'in order to validate file structure')

        ledger = read_corrupted_ledger_file()
    else:
        print('Validating and calculating score against actual original')
        ledger = read_ledger_file()

    actual_due_lookup = {row['customer_id']: int(row['amount']) for row in ledger}

    num_lines = len(ledger)
    num_corrected = len(ledger_corrected)

    if num_corrected != num_lines:
        raise ValueError('Error, files are not the same size: Ledger: %s, '
                         'Ledger_corrected: %s' % (num_lines, num_corrected))

    line_num = 0
    num_correct = 0
    total_collected = 0

    # This is only correct when using the real ledger
    actual_amount_total = 0.0

    for line, line_corr in zip(ledger, ledger_corrected):
        sum_line = sum([int(i) for i in line.values()])
        sum_line_corr = sum([int(i) for i in line_corr.values()])
        if sum_line != sum_line_corr:
            raise ValueError('Line %s does not have the right sum'
                             'file might be out of order' % line_num)

        if line_num == 0 and set(line.keys()) != set(line_corr.keys()):
            keys_expected = sorted(list(line.keys())).__repr__()
            keys_got = sorted(list(line.keys())).__repr__()
            raise ValueError('Does not have the expected keys. '
                             'Expected: %s, Got: %s' % (keys_expected, keys_got))

        if line == line_corr:
            # correct
            num_correct += 1
            total_collected += int(line_corr['amount'])
        else:
            cust_id_guessed = line_corr['customer_id']
            amount_guessed = int(line_corr['amount'])
            actually_due = actual_due_lookup.get(cust_id_guessed, 0)
            if amount_guessed <= actually_due:
                # customer still pays what you say they owe
                # when it is less than what they actually owe
                total_collected += int(line_corr['amount'])
            else:
                # customer does not pay, no net amount collected
                pass

            # line is wrong
            if debug and not use_corrupted:
                if line_corr != line:
                    sep = '---------------------'
                    print(sep)
                    print('original, line: %s' % line_num)
                    print(line)
                    print('corrected')
                    print(line_corr)

        actual_amount_total += int(line['amount'])
        line_num += 1

    print('Input file is valid')

    percent_correct = (100.0 * num_correct)/num_lines
    percent_recovered = (100.0 * total_collected) / actual_amount_total

    results = {'num_lines_correct': num_correct,
               'num_lines_wrong': num_lines - num_correct,
               'percent_lines_correct': percent_correct,
               'amount_recovered': total_collected,
               'percent_recovered': percent_recovered}

    if not use_corrupted:
        for k, v in results.items():
            print("\t%s: %s" % (k, v))

    return percent_recovered
