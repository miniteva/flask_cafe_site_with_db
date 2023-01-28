import os
from typing import Optional, Dict
from flask import Blueprint, request, render_template, current_app, session, redirect, url_for
from sem4.database.db_work import select_dict
from sem4.database.sql_provider import SQLProvider
from sem4.database.db_context_manager import DBConnection
from sem4.cache.wrapper import fetch_from_cache
import datetime

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
blueprint_order = Blueprint('blueprint_order', __name__, template_folder='templates')


@blueprint_order.route('/', methods=['GET', 'POST'])
def order_index():
    db_config = current_app.config['db_config']
    cache_config = current_app.config['cache_config']
    # print(cache_config)
    cached_select = fetch_from_cache('all_items_cached', cache_config)(select_dict)
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)
        basket_items = session.get('basket', {})
        return render_template('basket_order_list.html', items=items, basket=basket_items)
    else:
        prod_id = request.form['prod_id']
        sql = provider.get('select_item.sql', prod_id=prod_id)
        item = select_dict(db_config, sql)[0]

        add_to_basket(prod_id, item)

        return redirect(url_for('blueprint_order.order_index'))


def add_to_basket(prod_id: str, item:dict):
    curr_basket = session.get('basket', {})
    kolvo=request.form.get('kolvo')
    if prod_id in curr_basket:
        curr_basket[prod_id]['amount'] = curr_basket[prod_id]['amount'] + int(kolvo)
    else:
        curr_basket[prod_id] = {
            'nazvanie': item['nazvanie'],
            'valuee': item['valuee'],
            'amount': int(kolvo)
        }
        session['basket'] = curr_basket
        session.permanent = True
    return True


@blueprint_order.route('/save_order', methods=['GET', 'POST'])
def save_order():
    user_id = session.get('user_id')
    current_basket = session.get('basket', {})
    hall_id = session.get('select')
    stol_nom = session.get('stol_nom')
    print(session)
    order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket, hall_id, stol_nom)
    print(order_id)
    if order_id:
        session.pop('basket')
        return render_template('order_created.html', order_id=order_id)
    else:
        return render_template('have_error.html')


def save_order_with_list(dbconfig: dict, user_id, current_basket: dict, hall_id, stol_nom):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не найден')
        cur_date = datetime.date.today()
        #print(stol_nom)
        _sql1 = provider.get('insert_order.sql', user_id=user_id, order_date=cur_date, hall_id=hall_id, stol_nom=stol_nom) #результатом запроса insert является кол-во строк на котрове этот запрос воздействовал в бд
        result1 = cursor.execute(_sql1)
        #print(result1)
        if result1 == 1:
            _sql2 = provider.get('select_order_id.sql', user_id=user_id)
            print(user_id)
            cursor.execute(_sql2)
            order_id = cursor.fetchall()[0][0]
            print(order_id)
            if order_id:
                for key in current_basket:
                    prod_amount = current_basket[key]['amount']
                    _sql3 = provider.get('insert_order_list.sql', order_id=order_id, prod_id=key, prod_amount=prod_amount )
                    cursor.execute(_sql3)
                print(order_id)
                return order_id


@blueprint_order.route('/order_details', methods=['GET', 'POST'])
def order_details():
    if request.method == 'GET':
        return render_template('details_form.html')
    else:  # получить из формы параметры, выполнить   sql запрос
        hall_id = request.form.get('select')
        stol_nom = request.form.get('stol_nom')
        session['select'] = hall_id
        session['stol_nom'] = stol_nom
        #print(hall_id)
        #print(stol_nom)
        return redirect(url_for('blueprint_order.order_index'))


@blueprint_order.route('/clear-basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('blueprint_order.order_index'))