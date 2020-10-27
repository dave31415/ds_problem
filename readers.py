import csv
import numpy as np
import params
from collections import Counter
from math import exp
data_dir = 'data'


def read_first_names(gender='male'):
    """
    Read first name file, split by gender into two files
    :param gender: gender of names
    :return: list of first names
    """
    file_name = "%s/first_names_boys.csv" % data_dir
    if gender == "female":
        file_name = "%s/first_names_girls.csv" % data_dir
    return list(csv.DictReader(open(file_name, 'rU')))


def read_last_names():
    """
    :return: list of last names and counts
    """
    file_name = "%s/last_names.csv" % data_dir
    return list(csv.DictReader(open(file_name, 'rU')))


def read_street_names():
    """
    :return: list of street names and counts
    """
    file_name = "%s/street_names.csv" % data_dir
    return list(csv.DictReader(open(file_name, 'rU')))


def read_street_numbers():
    """
    :return: list of street numbers and counts
    """
    file_name = "%s/street_numbers.csv" % data_dir
    street_nums = list(csv.DictReader(open(file_name, 'rU')))
    # give more weight to smaller house numbers
    for item in street_nums:
        house_num = int(item['House Number'])
        if house_num > 10000:
            house_num = 1
        count = int(item['count'])
        item['count'] = count * exp(-house_num/params.street_exp_length)
    return street_nums


def read_cities():
    """
    :return: list of cities and counts
    """
    file_name = "%s/cities.csv" % data_dir
    data = list(csv.DictReader(open(file_name, 'rU')))
    for d in data:
        d['city_state'] = d['city']+','+d['state']
    return data


def read_addresses():
    """
    :return:list of address
    """
    file_name = "%s/addresses.csv" % data_dir
    return [a for a in csv.DictReader(open(file_name, 'rU'))
            if a['House Number'].isdigit() and len(a['Street Name']) > 2]


def read_first_names_male():
    """
    :return: list of male names and counts
    """
    return read_first_names(gender='male')


def read_first_names_female():
    """
    :return: list of female names and counts
    """
    return read_first_names(gender='female')


def read_states():
    """
    :return: read states and counts
    """
    file_name = "%s/states.csv" % data_dir
    return list(csv.DictReader(open(file_name, 'rU')))


def make_picker(reader, freq_tag, name_tag):
    """
    Make a closure that can randomly pick from a reader
    with the right frequency
    :param reader: a reader list or stream
    :param freq_tag: 'count' 'freq' etc whatever indicates
                     relative frequency
    :param name_tag: name of the thing to be picked (e.g. "House Number")
    :return: a randomly chosen object
    """
    name_list = sorted(reader(),
                       key=lambda x: x[freq_tag], reverse=True)
    cum_freq = np.cumsum(np.array([float(f[freq_tag]) for f in name_list]))
    freq_tot = float(cum_freq[-1])
    cum_freq /= freq_tot

    def this_picker():
        rand = np.random.random()
        index = np.argmax(cum_freq > rand)
        return name_list[index][name_tag]

    return this_picker


def make_person_picker():
    """
    Pick out a random person using all the files
    :return: a chosen Person object (well dictionary)
    """
    boy_picker = make_picker(read_first_names_male, 'freq', 'first_name')
    girl_picker = make_picker(read_first_names_female, 'freq', 'first_name')
    last_name_picker = make_picker(read_last_names, 'count', 'Name')
    street_picker = make_picker(read_street_names, 'count', 'Street Name')
    street_number_picker = make_picker(
        read_street_numbers, 'count', 'House Number')
    city_picker = make_picker(read_cities, 'count', 'city_state')

    def pick():
        if np.random.random() < 0.5:
            first_name = boy_picker()
            gender = "male"
        else:
            first_name = girl_picker()
            gender = "female"
        last_name = last_name_picker()

        age_sigma = params.age_sigma
        if gender == 'female':
            # make female distribution younger just to
            # allow for that to lead to slighly better results
            # should someone look into that
            age_sigma *= params.women_younger_by
        age = params.age_min + age_sigma*abs(np.random.randn())
        age = int(round(age))

        city, state = city_picker().split(',')

        amount = 0.0
        if np.random.random() > params.amount_percent_zero:
            random_normal = params.amount_lognormal_mu \
                + np.random.randn()*params.amount_lognormal_sigma
            amount = np.exp(random_normal)

        if params.amount_round:
            amount = round(amount)

        street_num = street_picker()
        if street_num == 0:
            street_num = 1

        return {'first_name': first_name.capitalize(),
                'last_name': last_name.capitalize(),
                # keep gender a latent variable
                # 'gender': gender,
                'age': age,
                'address_num': street_number_picker(),
                'street': street_num,
                'city': city,
                'state': state,
                'amount': int(amount)}

    return pick


def write_people_file(num=params.num_lines):
    """
    Writes a file of People, the main input file before corruption
    :param num: number of lines to write
    :return: None
    """
    np.random.seed(params.random_seed)
    person_picker = make_person_picker()
    people = [person_picker() for i in xrange(num)]
    total_amount = sum([float(p['amount']) for p in people])
    print "Total amount: %0.2f million" % (total_amount/1e6)
    print "Average amount: %0.2f" % (total_amount/float(len(people)))
    field_names = people[0].keys()
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
    return list(csv.DictReader(open(file_name, 'rU')))


def write_street_address_file(x_tag):
    """
    :param x_tag:
    :return:
    """
    count = Counter()
    for address in read_addresses():
        street_num = address[x_tag]
        count[street_num] += 1
    out_file = "%s/%s.csv" % (data_dir, x_tag)
    out_data = [{x_tag: key, "count": val}
                for key, val in count.iteritems()]
    out_data = sorted(out_data, key=lambda x: x['count'], reverse=True)
    fieldnames = [x_tag, "count"]
    dw = csv.DictWriter(open(out_file, 'w'), fieldnames=fieldnames)
    dw.writeheader()
    dw.writerows(out_data)


def write_street_number_file():
    """
    Write the street number file
    :return:
    """
    write_street_address_file("House Number")


def write_street_name_file():
    """
    Write the street name file
    :return:
    """
    write_street_address_file("Street Name")


def read_corrupted_people_file():
    """
    Returns a generator to the corrupted data file
    :return:
    """
    file_name = "%s/%s" % (params.data_dir, 'ledger_corrupted.csv')
    return csv.DictReader(open(file_name, 'rU'))


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
