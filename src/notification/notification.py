import uuid
from __main__ import app
from flask import request, jsonify
from src.db.db_notification import *
from src.common import get_current
from src.db.db_user import find_one_user, update_one_user, update_user_list_property
from src.user.user import check_user_exists


@app.route('/notification/get_by_user', methods=['Get'])
def kad_get_notification():
    if not request.json or not request.args.get('user'):
        return jsonify(
            {'error': 'Request Error: no notification Id in request', 'status': 400})
    user_email = request.args.get('user')
    notification = find_notification(query={'receiver': user_email})
    print(notification)
    return jsonify({'notification': notification, 'status': 200})


@app.route('/notification/add', methods=['POST'])
def kad_add_notification():
    required_keys = ['senderName', 'title', 'msg', 'sender', 'receiver', 'adId']
    if not request.json or not set(required_keys).issubset(set(request.json.keys())):
        return jsonify(
            {'error': 'Request Error: no sufficient data', 'status': 400})
    user = find_one_user(query={"email": request.json['receiver']})
    if not user:
        return jsonify(
            {'error': 'Request Error: user not exists', 'status': 404})
    new_notification = {
        'senderName': request.json['senderName'],
        'title': request.json['title'],
        'time': get_current(),
        'isRead': False,
        'msg': request.json['msg'],
        'sender': request.json['sender'],
        'receiver': request.json['receiver'],
        'notificationId': str(uuid.uuid4().hex),
        'adId': request.json['adId'],
    }
    add_one_notification(data=new_notification)
    return jsonify({'status': 200})


@app.route('/notification/update', methods=['POST'])
def update_notification():
    if not request.json or 'notificationId' not in request.json or 'isRead' not in request.json:
        return jsonify(
            {'error': 'Request Error: missing keys', 'status': 400})
    query = {
        'notificationId': request.json['notificationId']
    }
    update_one_notification(query=query, data={'isRead': request.json['isRead']})
    return jsonify({'status': 200})


@app.route('/notification/delete', methods=['DELETE'])
def kad_delete_notification():
    if not request.json or not request.args.get('notificationId'):
        return jsonify(
            {'error': 'Request Error: no notification Id in request', 'status': 400})
    query = {"notificationId": request.args.get('notification_id')}
    delete_one_notification(query=query)
    return jsonify({'status': 200})
