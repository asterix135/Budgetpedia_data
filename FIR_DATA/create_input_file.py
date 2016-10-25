"""
Creates input files for budgetpedia from FIR data:
    Either for all cities/year or one city only
Run from command line - Python 3.5 or later
cd to folder containing this file
python3 create_input_file.py city_id data_set_id
:param city_id (optional): ID of city to pull data for; 'A' or None selects all
:param data_set_id (optional): 'old' uses 2000-2008 data;
                                anything else uses 2009+ data
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


def build_category_tree(link_file, cat_description_dict):
    """
    Builds a tree with 3 parent nodes (REV, EXP, STF) showing
        hierarchy of budget categories
    :param link_file: string with location of csv showing relationships
    :param cat_description_dict: dict with human-friendly descriptions
    :returns Tree: Tree object representing hierarchy
    """
    # 1. build tree from adjacency list
    cat_tree = Tree()
    with open(link_file) as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            if line[1] not in cat_description_dict:
                raise KeyError('%s desription not defined' % str(line[1]))
            cat_tree.add_node(line[1], line[0],
                              node_desc=cat_description_dict[line[1]])
    # check to make sure that root nodes are only ['REV', 'EXP', 'STF']
    if not set(cat_tree.root_nodes()).issubset({'REV', 'EXP', 'STF'}):
        raise ValueError('Tree root nodes are incorrect.  Should be only '
                         'REV, EXP and STF.\n'
                         'Root values are %s' % str(set(cat_tree.root_nodes())))
    return cat_tree


def populate_tree(tree, city_year_data):
    """
    Takes existing tree and adds values for specific city in specific year
    :param tree: Tree object, fully fleshed out
    :param city_year_data: dict with city data values for specific city & year
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


def append_child_data(node, path_list, curr_path=None):
    """
    Recursive function to build csv file for Budgetpedia input
    :param node: a Node object.  First call should be to a root node.
                 Recursive calls will run on child nodes
    :param path_list: A list.  Empty unless there are columns that need to be
                      inserted before root node's code, desc for root node
    :param curr_path: DO NOT supply on original call - only for recursion
    :returns nothing this is modified by the function so does not need to
                        be specified
    """
    if node.is_leaf():
        path_extension = [node.node_key(),
                          node.node_description(),
                          node.node_val()]
        if curr_path is not None:
            curr_path.extend(path_extension)
        else:
            curr_path = path_extension
        path_list.append(curr_path)
    else:
        path_extension = [node.node_key(),
                          node.node_description()]
        if curr_path is not None:
            curr_path.extend(path_extension)
        else:
            curr_path = path_extension
        for child_node in node.get_children():
            append_child_data(child_node, path_list, curr_path[:])


def build_csv_data(list_of_paths):
    pass


def add_metadata():
    """
    _META_START_,
    SOURCE_DOCUMENT_LINK_ORIGINAL,
    SOURCE_DOCUMENT_LINK_COPY,https://drive.google.com/open?id=0B208oCU9D8OuVmZIU0tFRkhTcU0
    SOURCE_DOCUMENT_LINK_WORKING_DIRECTORY,https://drive.google.com/open?id=0B208oCU9D8OuZW9OVU5sUVZtVDg
    SOURCE_DOCUMENT_TITLE,"CITY OF TORONTO CONSOLIDATED FINANCIAL STATEMENTS FOR THE YEAR ENDED DECEMBER 31, 1998"
    SOURCE_DOCUMENT_TABLE_LOCATION,p.17
    SOURCE_DOCUMENT_TABLE_TITLE,"CONSOLIDATED STATEMENT OF OPERATIONS FOR THE YEAR ENDED DECEMBER 31, 1998"
    SOURCE_CSV_PRECURSOR_LINK,https://drive.google.com/open?id=0B0nzg-ld6eh_LXBTX0dmMWQtNlU
    SOURCE_CSV_PRECURSOR_AUTHOR_ID,Chris
    YEAR,1998
    VERSION,Actual
    ASPECT,Revenues
    NOTES_CONTENT,
    NOTES_SEVERITY,
    UNITS_NAME,Dollar
    UNITS_CODE,DOLLAR
    UNITS_MULTIPLIER,1000
    TOTAL_AMOUNT,
    INTAKE_DATETIME,
    INTAKE_OPERATOR_ID,Chris
    COLUMNS_CATEGORIES,Program:NAME
    COLUMNS_ATTRIBUTES,"Amount:VALUE, Notes:DESCRIPTION, Severity: CODE"
    _META_END_,
    """
    pass


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

    # TODO: REMOVE AFTER TESTING
    # data_file = 'test_data/data_file.csv'
    # map_file = 'test_data/map_file.csv'
    # cat_file = 'test_data/cat_file.csv'
    # link_file = 'test_data/link_file.csv'

    if len(argv) > 1 and argv[1] != 'A':
        city_id = argv[1]  # argvs are imported as strings
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
                cols_to_import[col_name] = col_desc + ': ' + line_desc
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
    # merge hand-crafted categories and column descriptions into one dict
    all_cats = {**cols_to_import, **my_cats}

    # build tree
    budget_tree = build_category_tree(link_file, all_cats)
    # populate tree for each city/year
    # TODO: make this general - right now it's only test for 1 yr of toronto
    data_to_populate = city_data['20002']['2014']
    tree_for_year = populate_tree(budget_tree, data_to_populate)

    # build csv
    roots = tree_for_year.root_nodes()
    all_paths = []
    test_path = append_child_data(tree_for_year.get_node(roots[0]), all_paths)
    for path in all_paths:
        print(path)

if __name__ == '__main__':
    main(sys.argv)
