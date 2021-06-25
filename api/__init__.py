from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from oauthlib.oauth2 import WebApplicationClient

import dotenv
import logging
import threading

from api.misc.queue import Queue
import os

logging.basicConfig(filename="paint.log", level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")

app = Flask(__name__)
api = Api(app)
CORS(app)

dotenv.load_dotenv()

ACCESSTOKEN = "ACCESSTOKEN"
RESETPASSWORDTOKEN = "RESETPASSWORDTOKEN"
ACCOUNTVERIFICATIONTOKEN = "ACCOUNTVERIFICATIONTOKEN"
TWOFACTORAUTHENTICATION = "TWOFACTORAUTHENTICATION"

APIDOCS_URL = "https://documenter.getpostman.com/view/11508905/TzRU9mNK"

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['BUNDLE_ERRORS'] = os.getenv('BUNDLE_ERRORS')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
app.config['GOOGLE_DISCOVERY_URL'] = os.getenv('GOOGLE_DISCOVERY_URL')
app.config['APP_BASE_URL'] = os.getenv('APP_BASE_URL')

mail = Mail(app)

db = SQLAlchemy(app)

client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

lock = threading.Lock()
queue = Queue(10)
paintJobs = {
    "red": True,
    "blue": False,
    "yellow": True,
    "green": False,
}

from api.routes import AuthRoutes, GoogleAuthRoutes, PaintRoutes, QueueRoutes, routes, UserRoutes
