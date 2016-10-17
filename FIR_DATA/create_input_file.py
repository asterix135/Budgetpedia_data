"""
Run from command line - Python 3.5 or later
cd to folder containing this file
python3 create_input_file.py city_id data_set_id
:param city_id: ID of city to pull data for; 'A' selects all
:param data_set_id: 'old' uses 2000-2008 data; anything else uses 2009+ data
"""

import sys
import csv
# import pandas

NEW_CAT_FILE = 'budget_categories.csv'
OLD_CAT_FILE = 'budget_categories.csv'
NEW_LINK_FILE = 'budget_expense_links.csv'
OLD_LINK_FILE = 'budget_expense_links.csv'
NEW_DATA = '2009_and_later/fir.csv'
OLD_DATA = 'pre_2009/fir2000-2008.csv'
NEW_MAP = '2009_and_later/FIR - CSV and RDA file Documentation - ' \
          'Data Dictionary.csv'
OLD_MAP = 'pre_2009/FIR - CSV and RDA file Documentation - 2000 to 2008 - ' \
        'Data Dictionary.csv'


def build_category_graph(exp_dict, cat_dict, city_data, link_file):
    """
    Builds a graph with 3 parent nodes (REV, EXP, STF) showing
        hierarchy of budget categories
    :param exp_dict: dictionary of budget category codes to be imported
    :param cat_dict: dictionary of hand-crafted categories for hierarchy
    :param city_data: dictionary with city data values
    :param link_file: string with location of csv showing relationships
    :returns ??: ?? Have to figure out ??
    """
    # 1. build tree from adjacency list
    cat_tree = Tree()
    with open(link_file) as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            cat_tree.add_node(line[1], line[0])
    # 2. add data points to leaves of tree
    for data_point in city_data:
        if cat_tree.has_node(data_point):
            
    # 3. build csv file required for input



def main(argv):
    # Set parameters for what gets selected for output
    if len(argv) > 2 and argv[2] == 'old':
        data_file = OLD_DATA
        map_file = OLD_MAP
        cat_file = OLD_CAT_FILE
        link_file = OLD_LINK_FILE
    else:
        data_file = NEW_DATA
        map_file = NEW_MAP
        cat_file = NEW_CAT_FILE
        link_file = NEW_LINK_FILE
    if len(argv) > 1 and argv[1] != 'A':
        # TODO: check datatype of city_id
        city_id = str(argv[1])
    else:
        city_id = 'all'

    # get list of what columns to import
    cols_to_import = {}
    with open(map_file) as f:
        reader = csv.DictReader(f)
        for line in reader:
            if str(line['Include']) == '1':
                col_name = line['Variable Name']
                col_desc = line['Column Description']
                line_desc = line['Variable / Line Description']
                cols_to_import[col_name] = [col_desc + ': ' + line_desc]
        if len(cols_to_import) == 0:
            print('\n=========================================')
            print('No Columns Selected for Import.  Aborting')
            print('=========================================\n')
            quit()

    # Import actual dollar values
    city_data = {}
    with open(data_file) as f:
        reader = csv.DictReader(f)
        for line in reader:
            mun_id = str(line['MUNID'])
            year = str(line['MARSYEAR'])
            if city_id == 'all' or mun_id == city_id:
                keepers = list(cols_to_import.keys())
                include_vals = {
                    key: value for key, value in line.items() if key in keepers
                }
                if mun_id in city_data:
                    city_data[mun_id][year] = include_vals
                else:
                    city_data[mun_id] = {year: include_vals}
    if len(city_data) == 0:
        print('\n================================')
        print('No city data imported.  Aborting')
        print('================================\n')
        quit()

    # import hand-crafted categories
    my_cats = {}
    with open(cat_file) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            my_cats[row[0]] = row[1]
        if len(my_cats) == 0:
            print('\n=================================')
            print('No categories imported.  Aborting')
            print('=================================\n')
            quit()

    # build graph hierarchy
    graph = None

if __name__ == '__main__':
    main(sys.argv)
