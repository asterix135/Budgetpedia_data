# Data work for Budgetpedia

Working data files to feed into Toronto Budgetpedia process

## Key files

### FIR Data Processing

- All relevant files & work contained in FIR_DATA folder
- To process raw FIR data into Budgetpedia-ready csv files (assuming you've cloned the repo)
    1. cd to FIR_DATA folder
    2. ensure python 3.5 or higher is installed (there is a command included
        that was introduced in python 3.5)
    3. from command line, run

    python3 create_input_file.py city_id data_set_id
