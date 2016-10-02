"""
Parses text copied from Toronto City Financial Statements (pdfs)
into csv file with only current year actual saved

run from command line
$python3 parse_copied_text.py inputfile outputfile index_of_correct_value
(default index is 1)
"""

import csv
import sys
import re


def parse_line(line, idx):
    desc_regex = r'(\D+\(Note\s\d+\))|\D+'
    num_regex = r'(\d+(,\d\d\d)+)|(\-)'
    description = re.match(desc_regex, line).group().strip()
    numbers = re.findall(num_regex, line)
    try:
        if numbers[idx][2] == '-':
            budget_num = '0'
        else:
            budget_num = numbers[idx][0].replace(',', '')
    except IndexError:
        budget_num = 0
        print("double-check value for %s" % description)

    return [description, budget_num]


def main(argv):
    output_data = []
    in_file = argv[1]
    out_file = argv[2]
    idx = int(argv[3]) if len(argv) > 3 else 1

    with open(in_file) as f:
        for line in f:
            if len(line) > 1:
                output_data.append(parse_line(line, idx))

    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(output_data)


if __name__ == '__main__':
    main(sys.argv)
