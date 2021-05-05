from werkzeug.utils import redirect

from init import app
from flask import render_template, request
from helpers.validation import validate_table, validate_file_type
from service.crud_operations import create_table, get_all_tables_info, create_table_by, delete_table_from_db


@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_new_table', methods=["GET", "POST"])
def add_new_table():
    if request.method == "GET":
        return render_template('add-new-table.html', data={'success-span': None})

    elif request.method == "POST":
        is_success_validation = True if validate_table(request.form) else False

        if is_success_validation:
            create_table(request.form)
        return render_template(f'add-new-table.html', data={'success-span': is_success_validation})


@app.route('/tables')
def show_all_tables():
    tables_info = get_all_tables_info()
    return render_template(f'show-all-tables.html',
                           data={'info': enumerate(tables_info.items()), 'amount_of_tables': len(tables_info)})


@app.route('/uploader', methods=["GET", "POST"])
def uploader():
    if request.method == 'GET':
        return redirect('/tables')

    if request.method == 'POST':
        f = request.files['file']
        is_success_validation, f_type = validate_file_type(f)
        if is_success_validation:
            create_table_by(file=f, f_type=f_type)

        return redirect('/add_new_table')
        # return render_template(f'add-new-table.html', data={'success-span': is_success_validation})


@app.route('/tables/<table_name>/delete', methods=["POST"])
def delete_table(table_name):
    delete_table_from_db(table_name)
    return redirect('/tables')
