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

logging.basicConfig(filename="paint.log", level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")

app = Flask(__name__)
api = Api(app)
CORS(app)

mysql = MySQL(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:PaarShanDB0408@localhost:3306/ctfsd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'ZA8cPQfHALBMYgUE4EdQUCCMj5XmA7889NikUDIztrNfGWmsYH1OwXznJBLmPMG'
app.config['BUNDLE_ERRORS'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'paarshan4800@gmail.com'
app.config['MAIL_PASSWORD'] = 'ggmu1008'
app.config['MAIL_DEFAULT_SENDER'] = 'paarshan4800@gmail.com'
app.config['GOOGLE_CLIENT_ID'] = '994181888367-tblo1lfujqi80tc857vflslokmj416fj.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = 'LJRWQWFprqsyJtILtiSGdHgx'
app.config['GOOGLE_DISCOVERY_URL'] = 'https://accounts.google.com/.well-known/openid-configuration'
app.config['APP_BASE_URL'] = 'https://127.0.0.1:5000'

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
