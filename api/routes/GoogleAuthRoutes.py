from api import app
from flask import redirect

from api.misc.ErrorResponse import getServerErrorResponse
from api.services.GoogleAuthServices import googleLogin, googleCallback


# Redirects to Google Login API
@app.route("/googleauth/login", methods=["GET"])
def googleLoginRoute():
    try:
        return redirect(googleLogin())
    except:
        return getServerErrorResponse()


# Google Login Callback Route
@app.route("/googleauth/callback")
def googleCallbackRoute():
    try:
        return googleCallback()
    except:
        return getServerErrorResponse()
