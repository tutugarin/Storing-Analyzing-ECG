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
        data = {'message': 'You successfully logged out!'}
        return data


class Signup(Resource):
    def post(self):
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        prom = dbms.DataBaseManagemantSystem()
        check = prom.check_user(email)
        if check:
            data = {'message': 'Email address already exists'}
            return data
        prom.add_user(name, generate_password_hash(password, method='sha256'), email)
        data = {'message': 'You successfully sign up!'}
        return data

    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if not email:
            auth = 0
        else:
            auth = prom.get_info_by_email(email)['is_login']
        data = {'auth': auth}
        return data


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
            data = {'message': 'Please check your login details and try again.'}
            return data

        flask.session['email'] = email
        prom.update_flag(1, email)
        data = {'message': 'You successfully logged in!'}
        return data

    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if not email:
            auth = 0
        else:
            auth = prom.get_info_by_email(email)['is_login']
        data = {'auth': auth}
        return data


def add_auth_method(api):
    api.add_resource(Login, '/login', endpoint="auth.login")
    api.add_resource(Signup, '/signup', endpoint="auth.signup")
    api.add_resource(Logout, '/logout', endpoint="auth.logout")
