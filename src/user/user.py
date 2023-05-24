from __main__ import app
from flask import request, abort, jsonify
from src.db.db_user import *
from src.encryption import Crypt

otp = '1234'
STR_KEY = 'klausadvertising'


def verify_user(user_id, email):
    crypt = Crypt()
    decrypt_user = crypt.decrypt(user_id, STR_KEY)
    return True if (decrypt_user == email) else False


@app.route('/user/login', methods=['POST'])
def login():
    if not request.json or not 'password' in request.json or (
            'email' not in request.json and 'phone' not in request.json):
        return jsonify(
            {'error': 'Request Error: should include email/phone and password in your request', 'status': 400})
    query = {"email": request.json['email']} if "email" in request.json else {'phone': request.json['phone']}
    login_user = find_one_user(query=query)
    if login_user:
        if request.json['password'] == login_user['password']:
            return jsonify({'status': 200})
        else:
            return jsonify({'error': 'Incorrect Password', 'status': 400})
    else:
        return jsonify({'error': 'User Not Found', 'status': 404})


@app.route('/user/check', methods=['Get'])
def check():
    if not request.args.get('email') and not request.args.get('phone'):
        return abort(400)
    check_type = 'email' if request.args.get('email') else 'phone'
    is_user = check_user_exists(email=request.args.get('email'), phone=request.args.get('phone'))
    if is_user:
        return jsonify({'error': f'This {check_type} is registered', 'status': 200})
    return jsonify({'status': 404})


def check_user_exists(email=None, phone=None):
    check_type = 'email' if email else 'phone'
    check_data = email if email else phone
    query = {
        check_type: check_data
    }
    is_user = find_one_user(query=query)
    if is_user:
        return True
    else:
        return False


@app.route('/user/get_key', methods=['Get'])
def get_key():
    email = request.args.get('email')
    if not request.args.get('email'):
        return abort(400)
    crypt = Crypt()
    user_id = str(crypt.encrypt(str_to_enc=email, str_key=STR_KEY))
    print(user_id)
    return jsonify({'user_id': user_id, "status": 200})


@app.route('/user/get', methods=['Get'])
def get_user():
    if not request.args.get('email') and not request.args.get('phone'):
        return abort(400)
    check_type = 'email' if request.args.get('email') else 'phone'
    check_data = request.args.get(check_type)

    query = {
        check_type: check_data
    }
    user = find_one_user(query=query)
    if user:
        return jsonify({'user': user, "status": 200})
    return jsonify({'Error': 'User not found', 'status': 404})


@app.route('/user/get_all', methods=['Get'])
def get_all_user():
    query = {}
    users = find_users(query=query)
    print(users)
    if users:
        return jsonify({'users': users, "status": 200})
    return jsonify({'Error': 'User not found', 'status': 400})


@app.route('/user/otp', methods=['POST'])
def send_otp():
    if not request.json or 'phone' not in request.json:
        return jsonify(
            {'error': 'Request Error: should include phone in your request', 'status': 400})
    phone = request.json['phone']
    otp = '1234'
    query = {
        'phone': phone
    }
    data = {
        'otp': otp
    }
    update_one_user(query=query, data=data)
    return jsonify({'status': 200})


@app.route('/user/update_favor_ad', methods=['POST'])
def update_favor_ad():
    if not request.json or 'ad_id' not in request.json or 'email' not in request.json:
        return jsonify(
            {'error': 'Request Error: should include phone in your request', 'status': 400})
    query = {
        'email': request.json['email']
    }
    update_user_list_property(data_key='favor_ads', query=query, data=request.json['ad_id'], remove_when_duplicate=True)
    return jsonify({'status': 200})


@app.route('/user/get_all_favor_Ad', methods=['Get'])
def get_all_favor_Ad():
    query = {}
    users = find_users(query=query)
    print(users)
    if users:
        return jsonify({'users': users, "status": 200})
    return jsonify({'Error': 'User not found', 'status': 400})


@app.route('/user/signup', methods=['POST'])
def signup():
    if not request.json or not 'password' in request.json or \
            'email' not in request.json or 'phone' not in request.json \
            or 'name' not in request.json or 'otp' not in request.json:
        return jsonify(
            {'error': 'Request Error: should include email, phone and password in your request', 'status': 400})
    if request.json['otp'] != otp:
        return jsonify(
            {'error': 'One time password is incorrect.', 'status': 400})
    if check_user_exists(request.json['email']):
        return jsonify(
            {'error': 'User exists', 'status': 400})
    crypt = Crypt()
    user_id = str(crypt.encrypt(str_to_enc=request.json['email'], str_key=STR_KEY))
    signup_user = {
        'name': request.json['name'],
        'email': request.json['email'],
        'phone': request.json['phone'],
        'password': request.json['password'],
        'user_id': user_id,
        'type': request.json['type'],
        'tags': [],
        'favor_ads': [],
        'apply_ads': [],
        'post_ads': []
    }
    add_one_user(data=signup_user)
    return jsonify({'status': 200})


@app.route('/user/delete', methods=['DELETE'])
def delete_ad():
    if not request.json or not request.args.get('user_id'):
        return jsonify(
            {'error': 'Request Error: no user Id in request', 'status': 400})
    query = {"ad_id": request.args.get('user_id')}
    delete_one_user(query=query)
    return jsonify({'status': 200})
