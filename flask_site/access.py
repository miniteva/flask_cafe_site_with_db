from functools import wraps

from flask import session, render_template, current_app, request, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('blueprint_auth.start_auth'))
    return wrapper


def group_validation(config: dict)-> bool:
    endpont_func =request.endpoint # достаёт имя обработчика
    endpont_app = request.endpoint.split('.')[0] #имя блюпринта без имени функции
    print(endpont_app)
    print(endpont_func)
    if 'user_group' in session:
        user_group = session['user_group']
        if user_group in config and endpont_app in config[user_group]: #если user
            return True
        elif user_group in config and endpont_func in config[user_group]: #проверка для конкретных имён
            return True
    return False


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return f(*args, **kwargs)
        return render_template('exceptions/internal_only.html')
    return wrapper


