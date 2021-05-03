from init import app
from flask import render_template, request, url_for, redirect
from helpers.validation import validate_table, validate_file_type
from service.crud_operations import create_table, get_all_tables_info, create_table_by


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


@app.route('/show_all_tables')
def show_all_tables():
    tables_info = get_all_tables_info()
    return render_template(f'show-all-tables.html',
                           data={'info': enumerate(tables_info.items()), 'amount_of_tables': len(tables_info)})


@app.route('/uploader', methods=["GET", "POST"])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        filetype = f.filename.split('.')[1]
        is_success_validation = True if validate_file_type(filetype) else False
        if is_success_validation:
            create_table_by(file=f)

        return render_template(f'add-new-table.html', data={'success-span': is_success_validation})
