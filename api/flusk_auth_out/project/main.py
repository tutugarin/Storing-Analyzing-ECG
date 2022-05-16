import functools
import json
import os
import flask
import requests

from flask import Blueprint, render_template, make_response
from flask_login import login_required, current_user
from flask_restful import Resource, Api
from flask_restful import reqparse

from . import db
import time
from datetime import datetime

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPE = 'https://www.googleapis.com/auth/fitness.heart_rate.read'
API_SERVICE_NAME = 'fitness'
API_VERSION = 'v1'

CLIENT_ID = '433488219494-pskhdk5jvej4f11kt8a6svtqb5qnts05.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'

DATA_SOURCE = 'raw:com.google.heart_rate.bpm:com.google.android.apps.fitness:user_input'
NOW = datetime.today()
START = 0
END = int(time.mktime(NOW.timetuple()) * 1000000000)
DATA_SET = "%s-%s" % (START, END)

main = Blueprint('main', __name__)

flag = False


@main.route('/')
def index():
    return render_template('index.html')


class Profile(Resource):
    def get(self):
        return make_response(render_template('profile.html', name=current_user.name, flag=flag), 200)


class GetProgramResult(Resource):
    def get(self):
        if 'credentials' not in flask.session:
            return flask.redirect(flask.url_for('main.oauth2callback'))
        credentials = json.loads(flask.session['credentials'])
        if credentials['expires_in'] <= 0:
            return flask.redirect(flask.url_for('main.oauth2callback'))
        else:
            headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
            req_uri = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/raw:com.google.heart_rate.bpm:com.google.android.apps.fitness:user_input/datasets/' + str(
                DATA_SET)
            r = requests.get(req_uri, headers=headers)
            return r.json()


class StartProgram(Resource):
    def get(self):
        if 'code' not in flask.request.args:
            auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                        '&client_id={}&redirect_uri={}&scope={}').format(CLIENT_ID, REDIRECT_URI, SCOPE)
            return flask.redirect(auth_uri)
        else:
            auth_code = flask.request.args.get('code')
            data = {'code': auth_code,
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'redirect_uri': REDIRECT_URI,
                    'grant_type': 'authorization_code'}
            r = requests.post('https://oauth2.googleapis.com/token', data=data)
            flask.session['credentials'] = r.text
            global flag
            flag = True
            return flask.redirect(flask.url_for('main.profile'))


class Revoke(Resource):
    def get(self):
        if 'credentials' not in flask.session:
            return make_response('You need to <a href="/oauth2callback">authorize</a> before ' +
                                 'testing the code to revoke credentials.', 200)

        credentials = json.loads(flask.session['credentials'])

        revoke = requests.post('https://oauth2.googleapis.com/revoke',
                               params={'token': credentials['access_token']},
                               headers={'content-type': 'application/x-www-form-urlencoded'})

        status_code = getattr(revoke, 'status_code')
        del flask.session['credentials']
        flag_false()
        if status_code == 200:
            return flask.redirect(flask.url_for('main.profile'))
        else:
            return 'An error occurred.'


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def add_main_method(api):
    api.add_resource(Profile, '/profile', endpoint="main.profile")
    api.add_resource(GetProgramResult, '/test', endpoint="main.test")
    api.add_resource(StartProgram, '/oauth2callback', endpoint="main.oauth2callback")
    api.add_resource(Revoke, '/revoke', endpoint="main.revoke")


def flag_false():
    global flag
    flag = False
