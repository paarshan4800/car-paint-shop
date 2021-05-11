from jwt import InvalidSignatureError, ExpiredSignatureError
from api import app
from api.misc.ServerError import getServerErrorResponse
from api.services.AuthServices import login, sendResetPassword, resetPassword, createUser
from api.services.AuthVerificationServices import verifyAccount
from api.validators.AuthValidators import validateRegisterRoute, validateLoginRoute, validateResetPasswordRequestRoute, \
    validateResetPasswordRoute
from flask import request


# Register - Create user
@app.route("/auth/register", methods=["POST"])
def registerRoute():
    try:
        req = request.get_json(force=True)

        # Validate
        condition, msg, status = validateRegisterRoute(req)

        # Validation check
        if not condition:
            return msg, status

        return createUser(req)

    except Exception as e:
        print(e)
        return getServerErrorResponse()


# Login
@app.route("/auth/login", methods=["POST"])
def loginRoute():
    try:
        req = request.get_json()

        # Validate
        condition, msg, status = validateLoginRoute(req)

        # Validation check
        if not condition:
            return msg, status

        return login(req)

    except Exception as e:
        print(e)
        return getServerErrorResponse()


# Reset Password Request
@app.route("/auth/resetPasswordRequest", methods=["POST"])
def resetPasswordRequestRoute():
    try:
        req = request.get_json()

        # Validate
        condition, msg, status = validateResetPasswordRequestRoute(req)

        # Validation check
        if not condition:
            return msg, status

        return sendResetPassword(req)

    except Exception as e:
        print(e, "EXC")
        return getServerErrorResponse()


# Reset Password
@app.route("/auth/resetPassword", methods=["POST"])
def resetPasswordRoute():
    try:
        req = request.get_json()

        # Validate
        condition, msg, status = validateResetPasswordRoute(req)

        # Validation check
        if not condition:
            return msg, status

        return resetPassword(req)

    except (InvalidSignatureError, ExpiredSignatureError) as e:
        return {"message": "Invalid or Expired Token"}, 400

    except:
        return getServerErrorResponse()


@app.route("/auth/verify")
def accountVerificationRoute():
    try:
        token = request.args.get("token")

        if token is None:
            return {"message": "Token required"}, 400

        return verifyAccount(token)

    except (InvalidSignatureError, ExpiredSignatureError) as e:
        return {"message": "Invalid or Expired Token"}, 400

    except:
        return getServerErrorResponse()


