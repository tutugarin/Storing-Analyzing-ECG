import flask
from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_restful import Resource, Api
from flask_restful import reqparse
from .models import User
from . import db
from .main import flag_false

auth = Blueprint('auth', __name__)


class Logout(Resource):
    def get(self):
        logout_user()
        flask.session.clear()
        flag_false()
        return redirect(url_for('main.index'))


class Signup(Resource):
    def post(self):
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(
            email=email).first()  # if this returns a user, then the email already exists in database

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    def get(self):
        return make_response(render_template('signup.html'), 200)


class Login(Resource):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    def get(self):
        return make_response(render_template('login.html'), 200)


def add_auth_method(api):
    api.add_resource(Login, '/login', endpoint="auth.login")
    api.add_resource(Signup, '/signup', endpoint="auth.signup")
    api.add_resource(Logout, '/logout', endpoint="auth.logout")
