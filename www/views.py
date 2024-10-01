from flask import render_template, Blueprint, request, jsonify
from json import loads
from create_db import db
import db_models
import hashlib
import hmac
from operator import itemgetter
from urllib.parse import parse_qsl
from os import getenv
import datetime
from time import time
import jwt
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

BOT_TOKEN = getenv('BOT_TOKEN')
SECRET_KEY = getenv('SECRET_KEY')

bp = Blueprint('main', __name__)

house_prices = {
    1: 1000,
    2: 5000,
    3: 10000,
    4: 100000,
    5: 1000000,
}

house_residential_places = {
    1: 10,
    2: 50,
    3: 100,
    4: 1000,
    5: 10000,
}

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'message': 'Token is missing or invalid!'}), 403

        try:
            token = token.split('Bearer ')[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 403

        return f(current_user_id, *args, **kwargs)
    return decorated

def check_webapp_signature(token: str, init_data: str):
    try:
        parsed_data = dict(parse_qsl(init_data))
    except ValueError:
        return False
    if "hash" not in parsed_data:
        return False

    hash_ = parsed_data.pop('hash')
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    if calculated_hash == hash_:
        pairs = data_check_string.split('\n')
        data_dict = dict(pair.split('=') for pair in pairs)
        user_data = loads(data_dict['user'])

        return user_data

@bp.route('/', methods=['GET', 'POST'])
def init():
    if request.method == 'GET':
        return render_template('init.html')
    elif request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization header missing or invalid'}), 400

        init_data = auth_header.split('Bearer ')[1]
        if not init_data:
            return jsonify({'error': 'No initData provided'}), 400

        res = check_webapp_signature(BOT_TOKEN, init_data)
        if res is not False:
            user = db_models.Users.query.filter_by(tg_id=int(res['id'])).first()
            referals = user.referrals
            if user:
                token = generate_token(res['id'])
                html = render_template('index.html', user=user, referals=referals)
                return jsonify({'html': html, 'token': token})
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': 'Invalid init data'}), 400

@bp.route('/town', methods=['GET', 'POST'])
@token_required
def show_town(current_user_id):
    user = db_models.Users.query.filter_by(tg_id=current_user_id).first()
    if user.town_name is None:
        return render_template('creatingTown.html', user=user)
    return render_template('town.html', user=user)

@bp.route('/api/create', methods=['POST'])
@token_required
def create_town(current_user_id):
    user = db_models.Users.query.filter_by(tg_id=current_user_id).first()
    if user.town_name is None:
        body = request.get_json()
        user.town_name = body['townName']
        db.session.commit()
        return render_template('town.html', user=user)

@bp.route('/api/withdraw_town_balance', methods=['POST'])
@token_required
def withdraw_town_balance(current_user_id):
    user = db_models.Users.query.filter_by(tg_id=current_user_id).first()
    if user.town_balance > 0:
        user.balance += user.town_balance
        user.town_balance = 0
        user.town_last_money_take_time = time()
        db.session.commit()
        return '', 200
    else:
        return jsonify({'error': 'Town balance is empty'}), 400

@bp.route('/api/buy_house', methods=['POST'])
@token_required
def town_buy_house(current_user_id):
    houseID = request.get_json()['houseID']
    if houseID > 0 and houseID and houseID <= len(house_prices):
        user = db_models.Users.query.filter_by(tg_id=current_user_id).first()
        if user.balance >= house_prices[houseID]:
            user.balance -= house_prices[houseID]
            user.town_residential_places += house_residential_places[houseID]
            db.session.commit()
            return jsonify({'user': user.to_dict()}), 200
        return '', 400
    return '', 400

@bp.route('/api/tap', methods=['POST'])
@token_required
def api_tap(current_user_id):
    if request.method == 'POST':
        taps = request.get_json()['taps']
        user = db_models.Users.query.filter_by(tg_id=current_user_id).first()
        user.balance += taps
        db.session.commit()
        return jsonify({'message': 'Success'})
