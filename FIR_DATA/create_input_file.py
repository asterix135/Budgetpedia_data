"""
Run from command line - Python 3.5 or later
cd to folder containing this file
python3 create_input_file.py city_id data_set_id
:param city_id: ID of city to pull data for; 'A' selects all
:param data_set_id: 'old' uses 2000-2008 data; anything else uses 2009+ data
"""

import sys
import csv
from tree import Tree
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


def populate_tree(tree, city_year_data):
    """
    Takes existing tree and adds values for specific city in specific year
    :param tree: Tree object, fully fleshed out
    :param city_data: dict with city data values for specific city & year
                      (already subset from all data)
    :returns Tree: copy of tree with values populated into leaves
    """
    new_tree = tree.copy_tree()
    for data_point in city_year_data:
        if new_tree.has_node(data_point):
            new_tree.update_node_val(data_point, city_year_data[data_point])
        else:
            raise KeyError('%s not in Tree' % str(data_point))
    return new_tree


def build_category_tree(city_data, link_file):
    """
    Builds a tree with 3 parent nodes (REV, EXP, STF) showing
        hierarchy of budget categories
    :param city_data: dictionary with city data values
    :param link_file: string with location of csv showing relationships
    :returns Tree: Tree object representing hierarchy
    """
    # 1. build tree from adjacency list
    cat_tree = Tree()
    with open(link_file) as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            cat_tree.add_node(line[1], line[0])
    # check to make sure that root nodes are only ['REV', 'EXP', 'STF']
    if not set(cat_tree.root_nodes()).issubset({'REV', 'EXP', 'STF'}):
        raise ValueError('Tree root nodes are incorrect.  Should be only ' \
                         'REV, EXP and STF.\n' \
                         'Root values are %s' % str(set(cat_tree.root_nodes())))
    return cat_tree


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

    # build tree
    budget_tree = build_category_tree(city_data, link_file)


if __name__ == '__main__':
    main(sys.argv)
