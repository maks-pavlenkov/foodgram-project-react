import sys
from csv import reader
from errno import EACCES, ENOENT


def data_validation(path):

    try:
        with open(path, 'r') as csv_file:
            data = list(reader(csv_file, delimiter=','))
            if not data:
                raise ValueError('No data available')
    except IOError as e:
        if e.errno == ENOENT:
            print('File is missing or wrong path!')
            sys.exit()
        elif e.errno == EACCES:
            print('Permission denied')
            sys.exit()
        else:
            print('Could not open file')
            sys.exit()
    return data
