import functools
import json
import os
import flask
import requests

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from . import db
import time
from datetime import datetime

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "/home/andrcontrol/PycharmProjects/flusk_auth_out/project/client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/fitness.heart_rate.read']
API_SERVICE_NAME = 'fitness'
API_VERSION = 'v1'

DATA_SOURCE = 'raw:com.google.heart_rate.bpm:com.google.android.apps.fitness:user_input'
NOW = datetime.today()
START = 0
END = int(time.mktime(NOW.timetuple()) * 1000000000)
DATA_SET = "%s-%s" % (START, END)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/test')
def test_api_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    oauth2_client = googleapiclient.discovery.build(
        'fitness', 'v1',
        credentials=credentials)

    return oauth2_client.users().dataSources().datasets().get(
        userId='me', dataSourceId=DATA_SOURCE, datasetId=DATA_SET).execute()


@main.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = "http://localhost:5000/oauth2callback"

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    flask.session['state'] = state
    flask.session.permanent = True
    return flask.redirect(authorization_url)


@main.route('/oauth2callback')
def oauth2callback():
    state = flask.request.args.get('state', default=None, type=None)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = "http://localhost:5000/oauth2callback"
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('main.test_api_request'))

@main.route('/revoke')
def revoke():
  if 'credentials' not in flask.session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **flask.session['credentials'])

  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.')
  else:
    return('An error occurred.')


@main.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return ('Credentials have been cleared.<br><br>')


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
