import math
from datetime import datetime, timedelta
import random

import jwt
from api import app, TWOFACTORAUTHENTICATION
from api.models.UserModel import User


def getUser(email):
    return User.query.filter_by(email=email).first()


def generateToken(email, type, otp=0, expiry=30):
    payload = {
        "email": email,
        "type": type,
        "exp": datetime.utcnow() + timedelta(minutes=expiry)
    }

    if type == TWOFACTORAUTHENTICATION:
        payload["otp"] = otp

    token = jwt.encode(
        payload
        ,
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return token


def decodeToken(token):
    return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])


def validateToken(token, tokenType):
    data = decodeToken(token)
    user = getUser(data["email"])
    type = data["type"]

    if user is None or type != tokenType:
        return False, user
    else:
        return True, user


def generateOTP():
    digits = "0123456789"
    OTP = ""

    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP
