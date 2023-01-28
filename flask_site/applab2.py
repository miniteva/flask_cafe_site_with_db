import json

from flask import Flask, render_template, session
from auth.auth import blueprint_auth
from report.reportroutes import blueprint_report
from basket.route import blueprint_order
from access import login_required


app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_order, url_prefix='/order')


app.config['db_config'] = json.load(open('configs/database.json'))
app.config['access_config'] = json.load(open('configs/access.json'))


with open('configs/cache.json', 'r') as f:
    app.config['cache_config'] = json.load(f)


@app.route('/')
@login_required
def menu_choice():
    if 'user_id' in session:
        if session.get('user_group', None):
            return render_template('internal_user_menu.html')  # internal_user_menu
        else:
            return render_template('external_user_menu.html')  # external_user_menu
    else:
        return render_template('auth.html')


@app.route('/exit')
@login_required
def exit_func():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5010, debug=True)
