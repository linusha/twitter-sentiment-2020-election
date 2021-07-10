import sys
import csv
import logging

input_file = sys.argv[1]
output_file = sys.argv[2]

# https://stackoverflow.com/questions/26050968/line-contains-null-byte-error-in-python-csv-reader
def nullbyte_resistent_reader(csv_dict_reader):
    while True:
        try:
            yield next(csv_dict_reader)
        except csv.Error:
            logging.critical('Row discarded due to NULL Byte.')
            print('Row discarded due to NULL Byte.')
            pass
        continue
    return

input_fieldnames = ['Positive', 
    'Negative',
    'Text',
    'date',]

output_fieldnames = ['positive', 
    'negative',
    'polarity',
    'sentiment',
    'is_negative',
    'interaction_term',]

with open(input_file, 'r', newline = '') as i:
    input_reader = nullbyte_resistent_reader(csv.DictReader(i, fieldnames = input_fieldnames, delimiter = '\t'))
    with open(output_file, 'w', newline = '' ) as o:
        output_writer = csv.DictWriter(o, fieldnames = output_fieldnames, delimiter = ',')
        for row in input_reader:
            # skip header line with column names
            if (row['Positive'] == 'Positive'):
                continue

            output_writer.writerow({'positive': row['Positive'], 
                                    'negative': row['Negative'],
                                    'polarity': int(row['Positive']) + int(row['Negative']),
                                    'sentiment': (int(row['Positive']) - int(row['Negative'])) - 2,
                                    'is_negative': int(int(row['Positive']) + int(row['Negative']) < 0),
                                    'interaction_term': ((int(row['Positive']) - int(row['Negative'])) - 2) * int(int(row['Positive']) + int(row['Negative']) < 0), 
                                    })

i.close()
o.close()        
