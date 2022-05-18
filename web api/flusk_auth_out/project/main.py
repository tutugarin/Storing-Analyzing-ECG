import json
import flask
import requests
from flask import Blueprint
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


class Index(Resource):
    def get(self):
        prom = dbms.DataBaseManagemantSystem()
        email = flask.session.get('email', False)
        if not email:
            auth = 0
            name = 'Please login first'
        else:
            auth = prom.get_info_by_email(email)['is_login']
            name = prom.get_info_by_email(email)['name']
        data = {'auth': auth, 'name': name}
        return data


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
        data = {'auth': auth, 'status': status}
        return data


class StartProgram(Resource):
    def get(self):
        if 'credentials' not in flask.session:
            data = {'message': 'First of all you need to login in Gooogle account'}
            return data
        credentials = json.loads(flask.session['credentials'])
        if credentials['expires_in'] <= 0:
            data = {'message': 'First of all you need to login in Gooogle account'}
            return data
        else:
            headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
            req_uri = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/raw:com.google.heart_rate.bpm:com.google.android.apps.fitness:user_input/datasets/' + str(
                DATA_SET)
            r = requests.get(req_uri, headers=headers)
            prom = dbms.DataBaseManagemantSystem()
            email = flask.session.get('email', False)
            if email:
                prom.insert_json_into_postgres(email, r.json())
                auth = prom.get_info_by_email(email)['is_login']
                status = prom.get_info_by_email(email).get('status', 0)
            else:
                auth = 0
                status = 0
            data = {'auth': auth, 'status': status}
            return data


class GoogleLogin(Resource):
    def get(self):
        if 'code' not in flask.request.args:
            auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                        '&client_id={}&redirect_uri={}&scope={}').format(CLIENT_ID, REDIRECT_URI, SCOPE)
            data = {'auth_uri': auth_uri}
            return data
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
            data = {'message': 'You successfully logged in Google account'}
            return data


class Revoke(Resource):
    def get(self):
        if 'credentials' not in flask.session:
            data = {'message': 'You need to authorize!'}
            return data

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
            data = {'message': 'You successully logged out from Google account'}
            return data
        else:
            data = {'message': 'An error occurred.'}
            return data


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
        data = {'auth': auth, 'status': status}
        return data


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
        data = {'auth': auth, 'status': status}
        return data


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
        data = {'auth': auth, 'status': status, 'info': info}
        return data


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def add_main_method(api):
    api.add_resource(Index, '/', endpoint="main.index")
    api.add_resource(Profile, '/profile', endpoint="main.profile")
    api.add_resource(StartProgram, '/test', endpoint="main.test")
    api.add_resource(GoogleLogin, '/oauth2callback', endpoint="main.oauth2callback")
    api.add_resource(Revoke, '/revoke', endpoint="main.revoke")
    api.add_resource(CheckStatus, '/check', endpoint="main.check")
    api.add_resource(StopProgram, '/stop', endpoint="main.stop")
    api.add_resource(GetResult, '/result', endpoint="main.result")
