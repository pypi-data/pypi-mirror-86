import bcrypt
import base64
import json
from datetime import datetime, timedelta
from os import environ
from flask import current_app as app, request, url_for

class URLSigning(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not app.config.get('SECRET_KEY'):
            raise RuntimeError('SECRET_KEY must be set.')

def signed_url_for(path, hours=0, minutes=15, _external=False, **kwargs):
    validity = timedelta(hours=hours, minutes=minutes)
    expires = str((datetime.utcnow() + validity).timestamp())
    return url_for(path, **_sign_params(expires, url_for(path), **kwargs), _external=_external)

def _sign_params(expires, *args, **kwargs):
    _kwargs = {**kwargs, 'expires': expires}
    cat = str.encode(''.join(args) + json.dumps(_kwargs) + app.secret_key)
    token = bcrypt.hashpw(cat, bcrypt.gensalt())
    return {**_kwargs, 'token': base64.b64encode(token).decode('ascii')}

def verify_signed_url():
    token = request.args.get('token')
    expires = request.args.get('expires')
    if not token or not expires:
        return False
    path = request.path
    args = {
        k: v for k, v
        in request.args.items()
        if k not in ['token', 'expires']
    }
    return _verify_signed_params(token, expires, path, **args)

def _verify_signed_params(token, expires, *args, **kwargs):
    _kwargs = {**kwargs, 'expires': expires}
    cat = str.encode(''.join(args) + json.dumps(_kwargs) + app.secret_key)
    _expires = datetime.fromtimestamp(float(expires))
    _token = base64.b64decode(token)
    try:
        return _expires > datetime.utcnow() and bcrypt.checkpw(cat, _token)
    except:
        return False
