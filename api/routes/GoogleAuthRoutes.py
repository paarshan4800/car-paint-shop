from api import app
from flask import redirect

from api.misc.ServerError import getServerErrorResponse
from api.services.GoogleAuthServices import googleLogin, googleCallback


@app.route("/googleauth/login", methods=["GET"])
def googleLoginRoute():
    try:
        return redirect(googleLogin())
    except Exception as e:
        print(e)
        return getServerErrorResponse()


@app.route("/googleauth/callback")
def googleCallbackRoute():
    try:
        return googleCallback()
    except Exception as e:
        print(e)
        return getServerErrorResponse()
