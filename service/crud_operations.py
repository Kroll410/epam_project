from sqlalchemy import MetaData, Table
from models.meta_models import class_factory
from werkzeug.datastructures import ImmutableDict
from init import db
from config import Config
import uuid

con = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
meta = MetaData(bind=con)


def create_table(table_data: ImmutableDict) -> None:
    MetaTableClass = class_factory(table_data)
    MetaTableClass.__table__.create(bind=con)
    print(f'Table `{MetaTableClass.__tablename__}` was created')


def create_table_by(file, f_type):
    if f_type == 'csv':
        f_type = ','
    elif f_type == 'tsv':
        f_type = '\t'
    else:
        raise ValueError

    file_data = file.read().decode('utf-8')
    table_name = file.filename.split('.')[0]

    fields = [x.strip('\'\" ') for x in file_data.split('\n')[0].split('{}'.format(f_type))]
    rows = [[y.strip('\'\" ') for y in x.split('{}'.format(f_type))] for x in file_data.split('\n')[1:]]

    table_field_types = {
        k: None for k in fields
    }

    # for f_idx in range(len(fields)):
    #     for row in rows:



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
    print(data)
    con.execute(ins, data)


def delete_table_from_db(table_name):
    print(table_name)
    table = Table(table_name, meta, autoload_with=con)
    table.drop(con)
