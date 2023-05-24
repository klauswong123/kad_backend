import uuid
from __main__ import app
from flask import request, jsonify
from src.db.db_ads import *
from src.common import get_current
from src.db.db_user import find_one_user, update_one_user, update_user_list_property


@app.route('/ads/get_all', methods=['Get'])
def kad_get_ads():
    ads = find_ads(query={})
    if len(ads) == 0:
        return jsonify({'error': f'No ads in db', 'status': 404})
    print(ads)
    return jsonify({'ads': ads, 'status': 200})


@app.route('/ads/apply', methods=['POST'])
def kad_apply_ad():
    if not request.json or 'ad_id' not in request.json or 'new_applier' not in request.json:
        return jsonify(
            {'error': 'Request Error: no AD Id in request', 'status': 400})
    query = {"ad_id": request.json['ad_id']}
    old_ad = find_one_ad(query=query)
    appliers = old_ad['applier'].append(request.json['new_applier'])
    data = {
        'applier': appliers
    }
    update_one_ad(query=query, data=data)
    user_query = {
        'email': request.json['new_applier']
    }
    update_user_list_property(data_key='apply_ads', query=user_query, data=request.json['ad_id'], remove_when_duplicate=False)
    return jsonify({'status': 200})


@app.route('/ads/add', methods=['POST'])
def kad_add_ad():
    if not request.json or not 'role' in request.json or \
            'title' not in request.json or 'description' not in request.json \
            or 'upperPrice' not in request.json or 'req' not in request.json \
            or 'user' not in request.json  or 'lowerPrice' not in request.json:
        return jsonify(
            {'error': 'Request Error: no sufficient data', 'status': 400})
    ad_owner = request.json['user']
    user = find_one_user(query={"email": ad_owner})
    if not user:
        return jsonify(
            {'error': 'Request Error: user not exists', 'status': 400})
    new_ad = {
        'logoUrl': user['icon'] if 'icon' in user else '',
        'role': request.json['role'],
        'owner': user['name'],
        'owner_email': user['email'],
        'isMark': False,
        'title': request.json['title'],
        'description': request.json['description'],
        'upperPrice': request.json['upperPrice'],
        'lowerPrice': request.json['lowerPrice'],
        'req': request.json['req'],
        'ad_id': str(uuid.uuid4().hex),
        'applier': [],
        'time': get_current(),
        'tags': request.json['tags'],
        'view': 0,
        'like': 0
    }
    add_one_ad(data=new_ad)
    return jsonify({'status': 200})


@app.route('/ads/delete', methods=['DELETE'])
def kad_delete_ad():
    if not request.json or not request.args.get('ad_id'):
        return jsonify(
            {'error': 'Request Error: no ad Id in request', 'status': 400})
    query = {"ad_id": request.args.get('ad_id')}
    delete_one_ad(query=query)
    return jsonify({'status': 200})
