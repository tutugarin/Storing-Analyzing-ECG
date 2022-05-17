import json
import flask
import requests
from flask import Blueprint, render_template, make_response
from flask_restful import Resource
import time
from datetime import datetime
from . import dbms

SCOPE = 'https://www.googleapis.com/auth/fitness.heart_rate.read'

CLIENT_ID = '433488219494-pskhdk5jvej4f11kt8a6svtqb5qnts05.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'

DATA_SOURCE = 'raw:com.google.heart_rate.bpm:com.google.android.apps.fitness:user_input'
NOW = datetime.today()
START = 0
END = int(time.mktime(NOW.timetuple()) * 1000000000)
DATA_SET = "%s-%s" % (START, END)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    prom = dbms.DataBaseManagemantSystem()
    email = flask.session.get('email', False)
    if not email:
        auth = 0
        name = 'Please login first'
    else:
        auth = prom.get_info_by_email(email)['is_login']
        name = prom.get_info_by_email(email)['name']
    return render_template('index.html', auth=auth, name=name)


class Profile(Resource):
    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if not email:
            auth = 0
            status = 0
        else:
            status = prom.get_info_by_email(email).get('status', 0)
            auth = prom.get_info_by_email(email)['is_login']
        return make_response(render_template('profile.html', auth=auth, status=status), 200)


class StartProgram(Resource):
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
            prom = dbms.DataBaseManagemantSystem()
            email = flask.session.get('email', False)
            if email:
                prom.insert_json_into_postgres(email, r.json())
                print(r.json())
                auth = prom.get_info_by_email(email)['is_login']
                status = prom.get_info_by_email(email).get('status', 0)
            else:
                auth = 0
                status = 0
            return make_response(render_template('profile.html', auth=auth, status=status), 200)


class GoogleLogin(Resource):
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
            prom = dbms.DataBaseManagemantSystem()
            email = flask.session.get('email', False)
            if email:
                prom.update_flag(2, email)
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
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if email:
            prom.update_flag(1, email)
        if status_code == 200:
            return flask.redirect(flask.url_for('main.profile'))
        else:
            return 'An error occurred.'


class CheckStatus(Resource):
    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if email:
            auth = prom.get_info_by_email(email)['is_login']
            status = prom.get_info_by_email(email).get('status', 0)
        else:
            auth = 0
            status = 0
        return make_response(render_template('profile.html', auth=auth, status=status), 200)


class StopProgram(Resource):
    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if email:
            auth = prom.get_info_by_email(email)['is_login']
            prom.update_status_by_email(email, 3)
            status = 3
        else:
            auth = 0
            status = 0
        return make_response(render_template('profile.html', auth=auth, status=status), 200)


class GetResult(Resource):
    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if email:
            auth = prom.get_info_by_email(email)['is_login']
            prom.update_status_by_email(3, email)
            info = prom.get_info_by_email(email)['info']
            status = 3
        else:
            auth = 0
            status = 0
            info = 'None'
        return make_response(render_template('profile.html', auth=auth, status=status, info=info), 200)


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def add_main_method(api):
    api.add_resource(Profile, '/profile', endpoint="main.profile")
    api.add_resource(StartProgram, '/test', endpoint="main.test")
    api.add_resource(GoogleLogin, '/oauth2callback', endpoint="main.oauth2callback")
    api.add_resource(Revoke, '/revoke', endpoint="main.revoke")
    api.add_resource(CheckStatus, '/check', endpoint="main.check")
    api.add_resource(StopProgram, '/stop', endpoint="main.stop")
    api.add_resource(GetResult, '/result', endpoint="main.result")
