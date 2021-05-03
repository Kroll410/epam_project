from datetime import datetime
from flask import request, render_template, make_response
from flask_restful import Resource
from sqlalchemy import Table, MetaData
from config import Config

from init import api, db

con = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
meta = MetaData(bind=con)


class TableApi(Resource):

    def get(self, table_name):
        table = Table(table_name, meta, autoload_with=con)
        columns = [str(x).split('.')[1] for x in table.columns]
        table_info = [list(x) for x in db.session.query(table).all()]

        return make_response(render_template('show-table.html', data={
            'fields': columns,
            'table_data': table_info,
            'name': table_name,
            'amount_of_fields': len(columns),
        }), 200)


def activate_api():
    api.add_resource(TableApi, '/<string:table_name>')
    print('Api activated')


activate_api()
