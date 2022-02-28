import csv
import json
import os
import re
import sys
from collections import defaultdict

columns = defaultdict(list)  # each value in each column is appended to a list

with open(os.path.abspath(sys.argv[1])) as f:
    reader = csv.DictReader(f)  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)  # append the value into the appropriate list


def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z


def parse_column(parsed_data, enum, column0, column1, column2, column3, column4, column5, column6, column7, column8):
    ship = {}
    import_name = defaultdict(list)
    direct = defaultdict(list)
    type = defaultdict(list)
    count = defaultdict(list)
    line = defaultdict(list)

    ship['ship_name'] = columns[column1][enum]
    import_name['import'].append(columns[column1][enum + 1])
    import_name['export'].append(columns[column5][enum + 1])
    direct['loaded'].append(columns[column1][enum + 2])
    direct['empty'].append(columns[column3][enum + 2])

    direct['loaded'].append(columns[column5][enum + 2])
    direct['empty'].append(columns[column7][enum + 2])

    type['container_type'].append(columns[column1][enum + 3])
    type['container_type'].append(columns[column2][enum + 3])
    type['container_type'].append(columns[column3][enum + 3])
    type['container_type'].append(columns[column4][enum + 3])

    type['container_type'].append(columns[column5][enum + 3])
    type['container_type'].append(columns[column6][enum + 3])
    type['container_type'].append(columns[column7][enum + 3])
    type['container_type'].append(columns[column8][enum + 3])

    list_index = [i + 5 for i, item in enumerate(columns[column1][enum + 5:enum + 19]) if re.search('\d', item)]
    # print(list_index)

    for enum_for_value in list_index:
        count['count'].append(columns[column1][enum + enum_for_value])
        count['count'].append(columns[column2][enum + enum_for_value])
        count['count'].append(columns[column3][enum + enum_for_value])
        count['count'].append(columns[column4][enum + enum_for_value])
        count['count'].append(columns[column5][enum + enum_for_value])
        count['count'].append(columns[column6][enum + enum_for_value])
        count['count'].append(columns[column7][enum + enum_for_value])
        count['count'].append(columns[column8][enum + enum_for_value])

        line['line'].append(columns[column0][enum + enum_for_value])

    x = {**ship, **import_name, **direct, **line, **type, **count}
    record = merge_two_dicts(context, x)
    parsed_data.append(record)


parsed_data = []
context = dict()


def process(input_file_path):
    columns = defaultdict(list)  # each value in each column is appended to a list

    with open(input_file_path) as file:
        reader = csv.DictReader(file)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1:Линия/Агент value1, column2: value2,...}
            for (key, value) in row.items():  # go over each column name and value
                columns[key].append(value)
    zip_list = list(columns)
    print(zip_list)
    context['month'] = zip_list[0]
    for enum, (ship_name, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y) in \
            enumerate(zip(columns[zip_list[0]], columns[zip_list[1]], columns[zip_list[2]], columns[zip_list[3]],
            columns[zip_list[4]], columns[zip_list[5]], columns[zip_list[6]], columns[zip_list[7]], columns[zip_list[8]],
            columns[zip_list[9]], columns[zip_list[10]], columns[zip_list[11]], columns[zip_list[12]], columns[zip_list[13]],
            columns[zip_list[14]], columns[zip_list[15]], columns[zip_list[16]],
            columns[zip_list[17]], columns[zip_list[18]], columns[zip_list[19]], columns[zip_list[20]],
            columns[zip_list[21]], columns[zip_list[22]], columns[zip_list[23]], columns[zip_list[24]])):
        if ship_name == 'Название судна':
            parse_column(parsed_data, enum, zip_list[0], zip_list[1], zip_list[2], zip_list[3], zip_list[4],
                         zip_list[5], zip_list[6], zip_list[7], zip_list[8])
            parse_column(parsed_data, enum, zip_list[0], zip_list[9], zip_list[10], zip_list[11], zip_list[12],
                         zip_list[13], zip_list[14], zip_list[15], zip_list[16])
            parse_column(parsed_data, enum, zip_list[0], zip_list[17], zip_list[18], zip_list[19], zip_list[20],
                         zip_list[21], zip_list[22], zip_list[23], zip_list[24])

    return parsed_data


# input_file_path = "/home/timur/PycharmWork/containers/17.02/csv/СТАТИСТИКА_2021.xls.csv"
# output_folder = "/home/timur/PycharmWork/containers/17.02/json/"
input_file_path = os.path.abspath(sys.argv[1])
output_folder = sys.argv[2]
basename = os.path.basename(input_file_path)
output_file_path = os.path.join(output_folder, basename + '.json')
print("output_file_path is {}".format(output_file_path))

parsed_data = process(input_file_path)
print(parsed_data)
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(parsed_data, file, ensure_ascii=False, indent=4)