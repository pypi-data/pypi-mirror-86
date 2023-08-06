from . import bp
from polzybackend import messenger
from polzybackend.models import User
from flask import jsonify


# toast debugging route
@bp.route('/ping')
def ping():
    #msg = messenger.format_sse(data='ping', event='fasifu')
    msg = "data: fasifu message\n\n"
    messenger.announce(msg=msg)
    return {}, 200


# returns all available users
@bp.route('/users')
def get_users():
	users = User.query.all()
	return jsonify([u.email for u in users]), 200
