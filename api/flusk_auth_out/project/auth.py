import flask
from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from . import dbms

auth = Blueprint('auth', __name__)


class Logout(Resource):
    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if email:
            prom.update_flag(0, email)
        flask.session.clear()
        return redirect(url_for('main.index'))


class Signup(Resource):
    def post(self):
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        prom = dbms.DataBaseManagemantSystem()
        check = prom.check_user(email)
        if check:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        prom.add_user(name, generate_password_hash(password, method='sha256'), email)
        return redirect(url_for('auth.login'))

    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if not email:
            auth = 0
        else:
            auth = prom.get_info_by_email(email)['is_login']
        return make_response(render_template('signup.html', auth=auth), 200)


class Login(Resource):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        prom = dbms.DataBaseManagemantSystem()
        check = prom.check_user(email)
        if check:
            info = prom.get_info_by_email(email)
        if not check or not check_password_hash(info['password'], password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

        flask.session['email'] = email
        prom.update_flag(1, email)
        return redirect(url_for('main.profile'))

    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if not email:
            auth = 0
        else:
            auth = prom.get_info_by_email(email)['is_login']
        return make_response(render_template('login.html', auth=auth), 200)


def add_auth_method(api):
    api.add_resource(Login, '/login', endpoint="auth.login")
    api.add_resource(Signup, '/signup', endpoint="auth.signup")
    api.add_resource(Logout, '/logout', endpoint="auth.logout")
