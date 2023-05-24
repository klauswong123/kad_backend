from flask import make_response, jsonify
from main import app


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(401)
def not_authorized(error):
    return make_response(jsonify({'error': error}))

@app.errorhandler(400)
def server_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 400)