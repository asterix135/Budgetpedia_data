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
    # TODO: Rather than copy, perhaps wipe current tree and start over
    new_tree = tree.copy_tree()
    for data_point in city_year_data:
        if new_tree.has_node(data_point):
            new_tree.update_node_val(data_point, city_year_data[data_point])
        else:
            raise KeyError('%s not in Tree' % str(data_point))
    return new_tree


def append_child_data(node, path_list, curr_path=None):
    """
    Recursive function to build list of lists than can be turned into a csv
        for Budgetpedia input
    :param node: a Node object.  First call should be to a root node.
                 Recursive calls will run on child nodes
    :param path_list: A list.  Empty unless there are columns that need to be
                      inserted before root node's code, desc for root node
    :param curr_path: DO NOT supply on original call - only for recursion
    :returns nothing: path_list param is modified by the function and changed
                      version can be used in parent function
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


def set_path_lengths_equal(list_of_paths):
    """
    Appends empty commas to each row so that each row is identical length
    :param list_of_paths: list of lists, where each sublist is path to cost
    :returns nothing: list_of_paths is modified by function
    """
    max_length = 0
    for sub_path in list_of_paths:
        if len(sub_path) > max_length:
            max_length = len(sub_path)
    for sub_path in list_of_paths:
        sub_path.extend([''] * (max_length (len(sub_path))))


def find_source_url(file_path, muni_id, year_val):
    """
    looks up url for source file for a municipality and year from relevant year
    table
    :param file_path: string indicating where lookup table is found
    :param muni_id: string indicating municipal id number in table
    :param year_val: string indicating year to lookup
    :returns string: absolute url of source file
    """
    url_prefix = 'https://efis.fma.csc.gov.on.ca/fir/'
    with open(file_path) as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if row[0] == muni_id:
                return url_prefix + row[2]


def add_metadata(list_of_paths, max_path_length, muni_id, year_val):
    """
    Prepend metadata needed for Budgetpedia intake process
    :param list_of_paths: list of list containing path info on data_set
    :param max_path_length: integer with length of longest path_list
    :param muni_id: integer identifying municipality
    :param year_val: integer identifying year
    :returns list of lists: combining metadata with list_of_paths
    """
    file_prefix = '2009_and_later/html_tables/'
    lookup_file = file_prefix + str(year_val) + '.txt'
    source_url = find_source_url(lookup_file, muni_id, year_val)
    meta_vals = [['_META_START_'],
                 ['SOURCE_DOCUMENT_LINK_ORIGINAL', source_url],
                 ['SOURCE_DOCUMENT_LINK_COPY',
                    'https://efis.fma.csc.gov.on.ca/fir/fir.csv'],
                 ['SOURCE_DOCUMENT_LINK_WORKING_DIRECTORY'],
                 ['SOURCE_DOCUMENT_LINK_WORKING_DIRECTORY'],
                 ['SOURCE_DOCUMENT_TITLE'],
                 ['SOURCE_DOCUMENT_TABLE_LOCATION'],
                 ['SOURCE_DOCUMENT_TABLE_TITLE'],
                 ['SOURCE_CSV_PRECURSOR_LINK'],
                 ['SOURCE_CSV_PRECURSOR_AUTHOR_ID', 'Chris'],
                 ['YEAR', year_val],
                 ['VERSION'],
                 ['ASPECT'],
                 ['NOTES_CONTENT'],
                 ['NOTES_SEVERITY'],
                 ['UNITS_NAME', 'Dollar'],
                 ['UNITS_MULTIPLIER', 1],
                 ['TOTAL_AMOUNT'],
                 ['INTAKE_DATETIME'],
                 ['INTAKE_OPERATOR_ID', 'Chris'],
                 ['COLUMNS_CATEGORIES', 'Program:NAME'],
                 ['COLUMNS_ATTRIBUTES'],
                 ['_META_END_']]
    for val in meta_vals:
        val.extend([''] * (max_path_length - len(val)))
    return meta_vals.extend(list_of_paths)


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
    muni_id = '20002'
    year_val = '2014'
    data_to_populate = city_data[muni_id][year_val]
    tree_for_year = populate_tree(budget_tree, data_to_populate)

    # build csv
    roots = tree_for_year.root_nodes()
    for node in roots:
        all_paths = []
        append_child_data(tree_for_year.get_node(node), all_paths)
        data_to_write = add_metadata(all_paths, 1, muni_id, year_val)

        # TODO: Need function to write csv to drive

    # append_child_data(tree_for_year.get_node(roots[0]), all_paths)
    for path in all_paths:
        print(path)

if __name__ == '__main__':
    main(sys.argv)
