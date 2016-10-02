import csv
import os
import sys


def clean_file(file_name):
    new_file_data = []
    with open(file_name) as f:
        reader = csv.reader(f)
        for line in reader:
            try:
                col_1 = int(line[1])
            except ValueError:
                col_1 = line[1]
            new_file_data.append([line[0], col_1])

    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        for line in new_file_data:
            writer.writerow(line)


def main(argv):
    rev_files = os.listdir('revenue')
    exp_files = os.listdir('expenses')

    for fil in rev_files:
        if fil[0] != '.':
            fil_path = 'revenue/' + fil
            clean_file(fil_path)

    for fil in exp_files:
        if fil[0] != '.':
            fil_path = 'expenses/' + fil
            clean_file(fil_path)


if __name__ == '__main__':
    main(sys.argv)
