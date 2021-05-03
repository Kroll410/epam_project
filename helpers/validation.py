import re
from service.crud_operations import get_all_tables_info


def _validate_table_field_name(table_name):
    return True if re.fullmatch(r'^[A-Z|_][^-. ]*$', table_name) else False


def _is_already_exists(table_name):
    return True if table_name in get_all_tables_info().values() else False


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


def validate_file_type(filetype):
    return False if filetype not in ('csv', 'tsv') else True