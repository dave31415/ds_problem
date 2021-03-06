import csv
from tempfile import NamedTemporaryFile
import os

field_names = ['customer_id', 'age', 'amount']


def ensure_dir_exists(directory):
    """
    If a directory doesn't exists, create it
    :param directory:
    :return:
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_temp_html():
    return NamedTemporaryFile().name+'.html'


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
