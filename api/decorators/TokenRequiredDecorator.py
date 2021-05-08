from functools import wraps
from flask import request
import jwt
from jwt import InvalidSignatureError

from api import app, db
from api.controllers.UserController import getUser


def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = None

            if "access-token" in request.headers:
                token = request.headers["access-token"]

            if not token:
                return {"message": "Access token is required"}, 401

            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(data)

            user = getUser(data["email"])

            if user is None:
                return {"message": "Invalid authorization token"}, 401

            return f(user, *args, **kwargs)

        except InvalidSignatureError as e:
            return {"message": "Invalid Authorization Token"}, 400

    return decorated
