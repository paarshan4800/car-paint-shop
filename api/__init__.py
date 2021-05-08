from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from oauthlib.oauth2 import WebApplicationClient

import logging
import threading

from api.queue import Queue

from decouple import config

logging.basicConfig(filename="paint.log", level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")

app = Flask(__name__)
api = Api(app)
CORS(app)

mysql = MySQL(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['BUNDLE_ERRORS'] = config('BUNDLE_ERRORS')
app.config['MAIL_SERVER'] = config('MAIL_SERVER')
app.config['MAIL_PORT'] = config('MAIL_PORT')
app.config['MAIL_USE_TLS'] = config('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = config('MAIL_DEFAULT_SENDER')
app.config['GOOGLE_CLIENT_ID'] = config('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = config('GOOGLE_CLIENT_SECRET')
app.config['GOOGLE_DISCOVERY_URL'] = config('GOOGLE_DISCOVERY_URL')
app.config['APP_BASE_URL'] = config('APP_BASE_URL')

mail = Mail(app)

db = SQLAlchemy(app)

client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

lock = threading.Lock()
queue = Queue(2)
paintJobs = {
    "red": True,
    "blue": True,
    "yellow": True,
    "green": False,
}

from api import routes
