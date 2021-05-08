import json
from datetime import datetime, timedelta

import requests
import jwt
from jwt import InvalidSignatureError
from werkzeug.security import check_password_hash, generate_password_hash

from api import mail, app, db, client
from flask_mail import Message
from flask import request, redirect
from api.controllers.UserController import getUser
from api.models.UserModel import User


def userLogin(args):
    user = User.query.filter_by(type="NORMAL").filter_by(email=args["email"]).first()
    print(user)
    if user is not None and check_password_hash(user.password, args["password"]):
        return True
    else:
        return False


def checkPasswordAndCPassword(password, c_password):
    if password != c_password:
        return False
    else:
        return True


def sendResetPasswordMail(user, token):
    with app.app_context():
        message = Message(
            "Password Reset Request",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user.email]
        )

        message.body = """Hey {}. You have requested to reset your password. Use the below token and send it with the request along with the new password. \nReset Password Token - {}""".format(
            user.name,
            token)

        print(message.body)
        mail.send(message)


def sendResetPassword(req):
    email = req["email"]

    # Check whether user exists for this email
    user = getUser(email)

    # If there is no such user or the user has registered using social account
    if not user or user.type != "NORMAL":
        return {"message": "Invalid Email"}, 400

    token = generateToken(email)
    sendResetPasswordMail(user, token)
    return {"message": "Password reset link sent to mail. Check."}, 200


def generateToken(email):
    token = jwt.encode(
        {"email": email, "exp": datetime.utcnow() + timedelta(minutes=30)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return token


def validateToken(token):
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    print(data)

    user = getUser(data["email"])
    print(user)

    if user is None:
        return False, user
    else:
        return True, user


def resetPassword(req):
    # Validate token
    token = req["token"]
    condition, user = validateToken(token)

    if not condition:
        return {"message": "Invalid authorization token"}, 401

    password = req["password"]
    c_password = req["c_password"]

    # Check password and confirmation password
    if not checkPasswordAndCPassword(password, c_password):
        return {"message": "Passwords not matching"}, 400

    hashedPassword = generate_password_hash(password)
    user.password = hashedPassword
    db.session.commit()

    return {"message": "Password reset successful"}, 200


def login(req):
    email = req["email"]
    password = req["password"]

    # Validate
    if not email or not password:
        return {"message": "Login credentials required"}, 400

    # Check whether email and password is correct or not
    if not userLogin(req):
        return {"message": "Invalid Email/Password"}, 400

    # Generate access token
    token = generateToken(email)
    return {"message": "Logged in Successfully", "token": token}, 200
