from datetime import datetime, timedelta
import jwt
from api import app
from api.models.UserModel import User


def getUser(email):
    return User.query.filter_by(email=email).first()


def generateToken(email, type):
    token = jwt.encode(
        {
            "email": email,
            "type": type,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
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
