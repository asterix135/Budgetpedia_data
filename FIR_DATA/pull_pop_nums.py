import csv

TORONTO_ID = 20002

tor_demographics = {}

with open('pre_2009/fir2000-2008.csv') as f:
    reader = csv.DictReader(f)
    for line in reader:
        mun_num = line['MUNID']
        if int(line['MUNID']) == TORONTO_ID:
            year = line['MARSYEAR']
            households = line['slc.02.40.01']
            population = line['slc.02.41.01']
            tor_demographics[year] = {'households': households,
                                      'population': population}

with open('to_demographics_pre_2009.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['year', 'households, population'])
    for year in tor_demographics:
        writer.writerow([year, tor_demographics[year]['households'],
                         tor_demographics[year]['population']])