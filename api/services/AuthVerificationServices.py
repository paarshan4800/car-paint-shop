from flask import render_template
from flask_mail import Message

from api import app, mail, db, ACCOUNTVERIFICATIONTOKEN
from api.services.TokenServices import generateToken, decodeToken, getUser
from api.models.UserModel import User


def isUserVerified(email):
    user = User.query.filter_by(email=email).first()
    if user.verified:
        return True
    else:
        return False


def sendAccountVerificationEmail(user, token):
    with app.app_context():
        message = Message(
            "Account Verification Mail",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user.email]
        )

        link = app.config['APP_BASE_URL'] + "/auth/verify?token=" + token

        message.body = """Hey {}. To verify your account please copy and paste the link below.\n\n{}""".format(
            user.name,
            link
        )

        message.html = render_template("accountVerificationEmail.html", name=user.name, link=link)

        print(message.body)
        mail.send(message)


def accountVerificationEmail(user):
    token = generateToken(user.email, ACCOUNTVERIFICATIONTOKEN)
    sendAccountVerificationEmail(user, token)


def verifyAccount(token):
    data = decodeToken(token)
    user = getUser(data["email"])

    # Check if the user exists and correct token type
    if user is None or data["type"] != ACCOUNTVERIFICATIONTOKEN:
        return {"message": "Invalid token"}, 400

    # Check if the user is already verified
    if user.verified:
        return {"message": "User account already verified"}, 200

    # Update DB
    user.verified = True
    db.session.commit()

    return {"message": "User account verified"}, 200
