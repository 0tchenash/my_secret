from flask import Flask, redirect, flash, session
from flask_login import LoginManager, login_required
from flask_babel import Babel
from flask_babel import gettext
from dao.models.models import User
from files.utils import *
from files.config import Config




login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    app.app_context().push()
    login_manager.init_app(app)


    return app

app = create_app(Config())
babel = Babel(app)



@babel.localeselector
def get_locale():
    return 'en'

@login_manager.unauthorized_handler     
def unauthorized_callback():
    flash(gettext(f"Access denied, login first"), "warning")                 
    return redirect('/user/login/')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/user/<query>/", methods=("GET", "POST"), strict_slashes=False)
def auth(query):
    if query == 'login':
        return login()
    elif query == 'register':
        return register()
    elif query == 'logout':
        return logout()
    else:
        return redirect(url_for('page_not_found'))


@app.route("/users/<query>/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def users_list(query):
    if query == 'list':
        return users()
    elif query.isdigit():
        return user_delete(int(query))
    else:
        return redirect(url_for('page_not_found'))


@app.route('/contact/', methods=("GET", "POST"), strict_slashes=False)
def contacts():
    
    return contact()

@app.route('/meow/')
def page_not_found():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=80)
    

