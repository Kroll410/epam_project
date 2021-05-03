from sqlalchemy import MetaData, Table
from models.meta_models import class_factory
from werkzeug.datastructures import ImmutableDict
from init import db
from config import Config
from init import pd
import uuid


con = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
meta = MetaData(bind=con)


def create_table(table_data: ImmutableDict) -> None:
    MetaTableClass = class_factory(table_data)
    MetaTableClass.__table__.create(bind=con)
    print(f'Table `{MetaTableClass.__tablename__}` was created')


def create_table_by(file):
    table_name = file.filename.split('.')[0]
    df = pd.read_csv(file)


def get_all_tables_info() -> dict:
    inspector = db.inspect(con)
    tables = inspector.get_table_names()

    data = {}
    for table in tables:
        data.update({table: []})
        for column in inspector.get_columns(table):
            data[table].append(column['name'])

    return data


def insert_into_table(table_name):
    table = Table(table_name, meta, autoload_with=con)
    # ins = table.insert().values(A='Example', uuid=uuid.uuid4())
    print(db.session.query(table).all())
    # con.execute(ins)

insert_into_table('A')
