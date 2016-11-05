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

```bash
python3 create_input_file.py city_id data_set_id
```

- (city_id is optional - numeric value of city in FIR data file, absence or 'A' selects all cities)
- (data_set_id is optional - 'old' uses pre-2009 data; anything else uses 2009 and later; city_id must be specified for this to be included)


### Audited Financial Statements

Relevant data contained in Fin_statements folder.  Most of this data was copy/pasted from financial statement pdfs and then processed manually


### Web site contributions

HTML file contains a couple of web page skeletons
