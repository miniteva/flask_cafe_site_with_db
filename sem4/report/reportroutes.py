
import os
from flask import Blueprint, request, render_template, current_app
from sem4.database.db_work import select,call_proc
from sem4.database.sql_provider import SQLProvider
from sem4.access import group_required

blueprint_report = Blueprint('blueprint_report', __name__,template_folder='templates')  # Папка с шаблонами template_folder
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))  # создается экземпляр класса sqlprovider выделенное кавычками путь к sql файлу


report_list = [
    {'rep_name': 'Отчет 1 ', 'rep_id': '1'},
]

report_url = {
    '1': {'create_rep': 'blueprint_report.create_rep1', 'view_rep': 'blueprint_report.view_rep1'},
}



@blueprint_report.route('/')
@group_required
def start_report():
    return render_template('report_result.html')


@blueprint_report.route('/worker')
@group_required
def perehod():
    return render_template('report_result.html')


@blueprint_report.route('/zaprosi')
@group_required
def zaprosi():
    return render_template('report_result4.html')



@blueprint_report.route('/el_menu')
def menu():
    _sql = provider.get('menu.sql')
    product_result, schema = select(current_app.config['db_config'], _sql)
    schema = ('номер блюда','цена','вес','название')
    return render_template('menuu.html', schema=schema, result=product_result)


@blueprint_report.route('/queries', methods=['GET', 'POST'])      #отчет
def queries():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
             _sql = provider.get('product.sql', input_product=input_product)
             product_result, schema = select(current_app.config['db_config'], _sql)
             schema = ('номер заказа', 'стол', 'оффициант', 'дата заказа', 'полная стоимост заказа')
             return render_template('db_result.html', schema=schema, result=product_result)
        else:
             return "Repeat input"



@blueprint_report.route('/sozdanie')      #еще не доделал
@group_required
def sozdanie():
    if request.method == 'GET':
        return render_template('product_form_zakaz.html')
    else:
        input_product = request.form.get('stol','officiant','stoimostm')
        if input_product:
            _sql = provider.get('sozdanie.sql')
            product_result, schema = select(current_app.config['db_config'], _sql)
            schema = ('номер заказа', 'стол', 'оффициант', 'дата заказа', 'полная стоимост заказа')
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"



@blueprint_report.route('/ofzakaz', methods=['GET', 'POST'])     #получение информации о заказах оффицианта
def ofzakaz():
    if request.method == 'GET':
        return render_template('product_form_ofzakaz.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
             _sql = provider.get('ofzakaz.sql', input_product=input_product)
             product_result, schema = select(current_app.config['db_config'], _sql)
             schema = ('номер заказа', 'стол',  'дата заказа', 'полная стоимость заказа')
             return render_template('db_result_ofzakaz.html', schema=schema, result=product_result)
        else:
             return "Repeat input"




@blueprint_report.route('/ofzakaz', methods=['GET', 'POST'])     #получение информации о выбранном заказе
def stroki_zakaza():
    if request.method == 'GET':
        return render_template('stroki_zakaza.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
             _sql = provider.get('ofzakaz.sql', input_product=input_product)
             product_result, schema = select(current_app.config['db_config'], _sql)
             schema = ('позиция', 'количество',  'стоимость')
             return render_template('db_result_stroki_zakaza.html', schema=schema, result=product_result)
        else:
             return "Repeat input"






@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        print("GET_create")
        return render_template('report_create.html')
    else:
        print(current_app.config['db_config'])
        print("POST_create")
        r_year = request.form.get('input_year')
        r_month = request.form.get('input_month')
        print("Loading...")
        if r_year and r_month:
            res = call_proc(current_app.config['db_config'], 'pop', r_year, r_month)
            print('res=', res)
            return render_template('report_created.html')
        else:
            return "Repeat input"




@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    if request.method == 'GET':
        return render_template('view_rep.html')
    else:
        rep_year = request.form.get('input_year')
        rep_month = request.form.get('input_month')
        print(rep_year)
        if rep_year and rep_month:
            _sql = provider.get('rep1.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            schema = ('номер отчета', 'id продукта', 'выбранный месяц', 'выбранный год','количество','сумма')
            return render_template('result_rep1.html', schema=schema, result=product_result)
        else:
            return "Repeat input"
