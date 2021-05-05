import re
from service.crud_operations import get_all_tables_info
import datetime


def _validate_table_field_name(name):
    return True if re.fullmatch(r'^[A-Z|_][^-.]*$', name) else False


def _is_already_exists(table_name):
    return True if table_name in get_all_tables_info().values() else False


def _str_validation(value, _type):
    return False if len(value) > _type.length else True


def _tint_validation(value, _type):
    return True if value in range(0, 255 + 1) else False


def _date_validation(value, _type):
    # mm-dd-yyyy standard
    print(value)
    try:
        datetime.datetime.strptime(value, '%m-%d-%Y')
    except ValueError:
        print('Wrong date format')
        return False
    return True


def validate_table(table_data):
    is_valid = True
    for name in list(table_data.items()):
        if not _validate_table_field_name(name[1]) and not name[0].startswith('field-type'):
            is_valid = False
            break
    else:
        if len(table_data) < 3:
            is_valid = ''

    if _is_already_exists(table_data['table-name']):
        is_valid = False

    return is_valid


def validate_file_type(file):
    types = {
        'csv': ',',
        'tsv': '\t',
    }
    is_valid = False
    f_type = None
    if (f_type := file.filename.split('.')[1]) in ('csv', 'tsv'):
        file_data = file.read().decode('utf-8')
        fields, rows = file_data.split("\n")[0], file_data.split("\n")[1:]

        for el in [x.strip(" \"\'") for x in fields.split('{}'.format(types[f_type]))]:
            is_valid = _validate_table_field_name(el)
    file.seek(0)
    return is_valid, f_type


def validate_user_inputs(table, data):
    types = {
        str: _str_validation,
        datetime.date: _date_validation,
        int: _tint_validation,
    }

    data_types = [x.type for i, x in enumerate(table.columns) if i not in (0, len(table.columns) - 1)]

    for _type, pair in zip(data_types, dict(data).items()):
        curr_col, curr_value = pair
        func = types[_type.python_type]
        if not func(curr_value, _type) or str(curr_value) == '':
            return False
    return True
