import logging

from flask import render_template
from werkzeug.security import check_password_hash, generate_password_hash

from api import mail, app, db, RESETPASSWORDTOKEN, ACCESSTOKEN, TWOFACTORAUTHENTICATION
from flask_mail import Message

from api.services.AuthVerificationServices import accountVerificationEmail
from api.services.TokenServices import generateToken, validateToken, generateOTP, decodeToken
from api.services.UserServices import getUser
from api.models.UserModel import User


def userLogin(args):
    # Find user with NORMAL registration type with given email
    user = User.query.filter_by(type="NORMAL").filter_by(email=args["email"]).first()
    if user is not None and check_password_hash(user.password, args["password"]):
        return True
    else:
        return False


# Check password and confirmation password
def checkPasswordAndCPassword(password, c_password):
    if password != c_password:
        return False
    else:
        return True


# Send Reset Password Mail
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

        message.html = render_template("resetPasswordRequest.html", name=user.name, token=token)

        mail.send(message)
        logging.info("Reset Password Mail sent to {}".format(user.email))


def sendResetPassword(req):
    email = req["email"]

    # Check whether user exists for this email
    user = getUser(email)

    # If there is no such user or the user has registered using social account
    if not user or user.type != "NORMAL":
        return {"message": "Invalid Email"}, 400

    # Generate Reset password token and send to mail
    token = generateToken(email, RESETPASSWORDTOKEN)
    sendResetPasswordMail(user, token)

    return {"message": "Password reset link sent to mail. Check."}, 200


def resetPassword(req):
    # Validate token
    token = req["token"]
    condition, user = validateToken(token, RESETPASSWORDTOKEN)

    if not condition:
        return {"message": "Invalid authorization token"}, 401

    password = req["password"]
    c_password = req["c_password"]

    # Check password and confirmation password
    if not checkPasswordAndCPassword(password, c_password):
        return {"message": "Passwords not matching"}, 400

    # Update password
    hashedPassword = generate_password_hash(password)
    user.password = hashedPassword
    db.session.commit()
    logging.info("Password resetted for - {}".format(user.email))

    return {"message": "Password reset successful"}, 200


def createUser(req):
    email = req["email"]
    name = req["name"]

    # Check email already used or not
    if getUser(email) is not None:
        return {"message": "Email already in use"}, 200

    password = req["password"]
    c_password = req["c_password"]
    # Check password and confirmation password
    if not checkPasswordAndCPassword(password, c_password):
        return {"message": "Passwords not matching"}, 400

    hashedPwd = generate_password_hash(password, method='sha256')
    user = User(
        email=email,
        password=hashedPwd,
        name=name,
        admin=False,
        type="NORMAL",
        verified=False
    )

    # Add to DB
    db.session.add(user)
    db.session.commit()
    logging.info("Registered new user - {}".format(user.email))

    accountVerificationEmail(user)  # Send Verification Email

    return {
               "message": "User Created Successfully. Verification mail sent. Please verify your account to access all the features"}, 201


def twofactorauthenticationmail(user, token, otp):
    with app.app_context():
        digits = "0123456789"

        message = Message(
            "Two Factor Authentication",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user.email]
        )

        message.body = """Hey {}. Your One Time Password (OTP) is {}. This will expire in the next 10 minutes. Use the below token and send it with the OTP.\nAuthentication Token - {}""".format(
            user.name,
            otp,
            token)

        message.html = render_template("twoFactorAuthenticationEmail.html", name=user.name, otp=otp, token=token)
        mail.send(message)
        logging.info("Sent two factor auth mail to - {}".format(user.email))


def login(req):
    email = req["email"]
    password = req["password"]

    # Check whether email and password is correct or not
    if not userLogin(req):
        return {"message": "Invalid Email/Password"}, 400

    # Generate access token
    otp = generateOTP()
    token = generateToken(email, TWOFACTORAUTHENTICATION, otp, 10)
    user = getUser(email)
    twofactorauthenticationmail(user, token, otp)

    return {"message": "OTP sent to mail. Enter your OTP to login."}, 200


def twoFactorAuth(req):
    # Validate token
    token = req["token"]
    condition, user = validateToken(token, TWOFACTORAUTHENTICATION)

    if not condition:
        return {"message": "Invalid authorization token"}, 401

    otp = req["otp"]
    data = decodeToken(token)

    # Check if otp matches
    if int(data["otp"]) != otp:
        return {"message": "Invalid OTP"}, 401

    token = generateToken(data["email"], ACCESSTOKEN)
    logging.info("User {} logged in".format(user.email))

    return {"message": "Logged in Successfully", "token": token}, 200
