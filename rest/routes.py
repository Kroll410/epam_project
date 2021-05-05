from datetime import datetime
from flask import request, render_template, make_response
from flask_restful import Resource
from sqlalchemy import Table, MetaData
from config import Config
from helpers.validation import validate_user_inputs

from init import api, db
from service.crud_operations import insert_into_table, delete_table_from_db

con = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
meta = MetaData(bind=con)


class TableApi(Resource):

    def get(self, table_name):
        table = Table(table_name, meta, autoload_with=con)
        columns = [str(x).split('.')[1] for x in table.columns]
        table_types = [c.type for c in meta.tables[table_name].columns]
        table_info = [list(x) for x in db.session.query(table).all()]

        return make_response(render_template('show-table.html', data={
            'fields': columns,
            'table_types': str(table_types),
            'table_data': table_info,
            'name': table_name,
            'amount_of_fields': len(columns),
        }), 200)

    def post(self, table_name):
        table = Table(table_name, meta, autoload_with=con)

        is_success_validation = True if validate_user_inputs(table, request.form) else False

        if is_success_validation:
            insert_into_table(request.form, table_name)

        columns = [str(x).split('.')[1] for x in table.columns]
        table_types = [c.type for c in meta.tables[table_name].columns]
        table_info = [list(x) for x in db.session.query(table).all()]

        return make_response(render_template('show-table.html', data={
            'fields': columns,
            'table_types': table_types,
            'table_data': table_info,
            'name': table_name,
            'amount_of_fields': len(columns),
            'delete_table': delete_table_from_db,
        }), 200)



def activate_api():
    api.add_resource(TableApi, '/tables/<string:table_name>', )
    print('Api activated')


activate_api()
