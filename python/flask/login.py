# -*- coding: utf-8 -*-
import flask
from flask.ext import login as lm


def get_users():
    users = []
    with open('users.txt') as f:
        for line in f:
            id, username, password = line.strip().split('\t')
            users.append((int(id), username, password, ))
    return users


def make_user(id, username, password):
    rv = User()
    rv.id = id
    rv.username = username
    rv.password = password
    return rv


def get_user(user_id):
    for u in get_users():
        id, username, password = u
        if user_id == id:
            return make_user(id, username, password)


class User(lm.UserMixin):

    id = None
    username = None
    password = None

    def __init__(self):
        pass


    def get_auth_token(self):
        rv = lm.make_secure_token(
            self.username + self.password)

        app.logger.debug(rv)

        return rv


app = flask.Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hello'

app.logger.debug(get_users())

login_manager = lm.LoginManager()
login_manager.init_app(app)


@login_manager.token_loader
def load_token(*args, **kwargs):
    app.logger.debug(args)
    app.logger.debug(kwargs)


@login_manager.user_loader
def load_user(s_user_id):
    user_id = int(s_user_id)
    rv = get_user(user_id)
    if rv:
        return rv


@app.route('/', endpoint='root')
def root():
    return flask.redirect(flask.url_for('login'))


@app.route('/login', methods=['GET', 'POST'], endpoint='login')

def login():
    if flask.request.method == 'GET':
        return flask.render_template('login/login.html')

    for u in get_users():
        id, username, password = u
        if flask.request.form['username'].strip() == username and \
           flask.request.form['password'].strip() == password:
            user = make_user(id, username, password)
            lm.login_user(user)

            return flask.redirect(flask.url_for('home'))

@app.route('/logout', endpoint='logout')
def logout():
    lm.logout_user()
    return flask.redirect(flask.url_for('login'))


@app.route('/home', endpoint='home')
@lm.login_required
def home():
    user = lm.current_user
    return flask.render_template('login/home.html', user=user)


app.run('0.0.0.0', port=5000, threaded=True)
