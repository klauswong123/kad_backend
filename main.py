from flask import Flask, jsonify

app = Flask(__name__)

from src.user import user
from src.ads import home_ads
from src.notification import notification

if __name__ == '__main__':
    app.run(debug=True)
