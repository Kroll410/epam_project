from sqlalchemy import MetaData, Table
from models.meta_models import class_factory
from init import db
from config import Config
import uuid

con = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
meta = MetaData(bind=con)


def create_table(table_data) -> None:
    MetaTableClass = class_factory(table_data)
    MetaTableClass.__table__.create(bind=con)
    print(f'Table `{MetaTableClass.__tablename__}` was created')


def create_table_by(file, f_type):
    types = {
        'csv': ',',
        'tsv': '\t',
    }

    def column_type(column):
        for val in column:
            try:
                float(val)
                if '.' in val:
                    return 'Float'
                else:
                    return 'Integer'
            except ValueError:
                return 'Text'
        return 'Text'

    table_name = file.filename.split('.')[0]

    file = file.read().decode('utf-8').split('\n')
    table_fields_raw, rows = file[0], [[y.strip(' \'\"') for y in x.split(f'{types[f_type]}')] for x in file[1:-1]]
    fields = [str(x.strip(' \t\n\'\"')) for x in table_fields_raw.split(f'{types[f_type]}')]

    table_meta = [
        ('table-name', table_name)
    ]
    for idx, col in enumerate(zip(*rows)):
        table_meta.extend([
            (f'field-name-{idx + 1}', fields[idx]),
            (f'field-type-{idx + 1}', column_type(col))
        ])

    create_table(table_meta)
    try:

        for i in range(len(rows)):
            data = []
            for j in range(len(fields)):
                data.append((fields[j], rows[i][j]))
            insert_into_table(data, table_name)
    except:
        delete_table_from_db(table_name)


def get_all_tables_info() -> dict:
    inspector = db.inspect(con)
    tables = inspector.get_table_names()

    data = {}
    for table in tables:
        data.update({table: []})
        for column in inspector.get_columns(table):
            data[table].append(column['name'])

    return data


def insert_into_table(data, table_name):
    table = Table(table_name, meta, autoload_with=con)
    data = dict(data)
    data.update({
        'uuid': str(uuid.uuid4())
    })
    ins = table.insert()
    con.execute(ins, data)


def delete_table_from_db(table_name):
    print(table_name)
    table = Table(table_name, meta, autoload_with=con)
    table.drop(con)
    db.metadata.clear()
