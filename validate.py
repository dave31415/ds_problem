import csv
import sys
from readers import read_ledger_file


def make_person_name(person):
    """
    :param person: person object
    :return: full name
    """
    return person['first_name']+' ' + person['last_name']


def make_person_address(person):
    """
    :param person: person object
    :return: address string of person
    """
    return "{address_num} {street}, {city}, {state}".format(**person)


def make_person_id(person):
    id = make_person_name(person) + ', ' + make_person_address(person)
    return id.lower().strip()


def validate_file(file_name):
    ledger_corrected = list(csv.DictReader(open(file_name, 'rU')))
    return validate_ledger(ledger_corrected)


def validate_ledger(ledger_corrected):
    ledger = read_ledger_file()
    num_lines = len(ledger)
    total = sum([int(l['amount']) for l in ledger])
    num_corrected = len(ledger_corrected)
    if num_corrected != num_lines:
        print 'Warning, files are not the same size'
        print 'Ledger: %s, Ledger_corrected: %s' % (num_lines, num_corrected)
    person_dict = {}
    for line in ledger:
        id = make_person_id(line)
        person_dict[id] = line

    num_correct = 0
    total_collection = 0.0
    for person in ledger_corrected:
        id = make_person_id(person)
        if id not in person_dict:
            continue
        match_person = person_dict[id]
        amount_true = match_person['amount']
        amount = person['amount']
        if amount == amount_true:
            num_correct += 1
            total_collection += int(amount)

    results = {'num_lines_correct': num_correct,
               'num_lines_wrong': num_lines - num_correct,
               'percent_lines_correct': 100.0*num_correct/float(num_lines),
               'amount_recovered': total_collection,
               'percent_recovered': 100.0*total_collection/total}

    explain_results(results)
    return results


def compare_files(corrected_file):
    people = read_ledger_file()
    people_corrected = list(csv.DictReader(open(corrected_file, 'rU')))

    i = 0
    for person, person_corrected in zip(people, people_corrected):
        del person['age'], person['height'], person['weight']
        del person_corrected['age']
        del person_corrected['height']
        del person_corrected['weight']

        if person == person_corrected:
            pass
        else:
            print 'Not correct, line: %s' % i
            print person
            print person_corrected
        i += 1


def explain_results(results):
    for k, v in sorted(results.items()):
        print "%s  : %s" % (k, v)


if __name__ == "__main__":
    file_name = sys.argv[1]
    result = validate_file(file_name)
