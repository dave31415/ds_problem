import csv

data_dir = 'data'
field_names = ['customer_id', 'age', 'amount']


def read_corrupted_ledger_file():
    """
    Returns a generator to the corrupted data file
    :return:
    """
    file_name = "%s/%s" % (data_dir, 'ledger_corrupted.csv')
    return list(csv.DictReader(open(file_name, 'r')))


def write_file(data, file_name):
    writer = csv.DictWriter(open(file_name, 'w'), fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data)
    print('wrote: %s' % file_name)


def batch_stream(stream, batch_size):
    """
    Take a stream and return another which yields batches
    of some specified size
    :param stream: any stream
    :param batch_size: size of each batch
    :return: batched stream
    """
    batch = []
    for obj in stream:
        batch.append(obj)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if len(batch) > 0:
        yield batch
