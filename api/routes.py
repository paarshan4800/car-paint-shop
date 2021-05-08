from jwt import InvalidSignatureError, ExpiredSignatureError

from api import api, app
from api.controllers.AuthController import sendResetPassword, resetPassword, login
from api.controllers.GoogleAuthController import googleLogin, googleCallback
from api.resources import WelcomeResource, PaintResource, QueueResource
from api.validators.UserValidator import *
from api.controllers.UserController import *
from flask import request, redirect
from api.decorators.TokenRequiredDecorator import tokenRequired


# Get all users ADMIN
@app.route("/user", methods=["GET"])
@tokenRequired
def getUsers(user):
    try:
        return getAllUsers()

    except:
        return {"message": "Server Error"}, 500


# Create users (Register) USER
@app.route("/user", methods=["DELETE"])
def delete():
    try:
        req = request.get_json()
        return deleteUser(req["email"])

    except:
        return {"message": "server error"}, 500


# Create users (Register) USER
@app.route("/register", methods=["POST"])
def register():
    try:
        args = user_create_args.parse_args()
        return createUser(args)

    except:
        return {"message": "server error"}, 500


@app.route("/login", methods=["POST"])
def loginRoute():
    try:
        req = request.get_json()
        email = req["email"]
        password = req["password"]

        # Validate
        if not email or not password:
            return {"message": "Login credentials required"}, 400

        return login(req)

    except Exception as e:
        print(e)
        return {"message": "server error"}, 500


@app.route("/resetPasswordRequest", methods=["POST"])
def resetPasswordRequest():
    try:
        req = request.get_json()

        # Validate
        if "email" not in req:
            return {"message": "Email required"}, 400

        return sendResetPassword(req)

    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500


@app.route("/resetPassword", methods=["POST"])
def resetPasswordRoute():
    try:
        req = request.get_json()

        return resetPassword(req)

    except (InvalidSignatureError, ExpiredSignatureError) as e:
        return {"message": "Invalid or Expired Token"}, 400

    except:
        return {"message": "Server error"}, 500


@app.route("/googleLogin", methods=["GET"])
def googleLoginRoute():
    try:
        return redirect(googleLogin())
    except Exception as e:
        print(e)
        return {"message": "Server Error"}


@app.route("/callback")
def googleCallbackRoute():
    try:
        return googleCallback()
    except Exception as e:
        print(e)
        return {"message": "Server Error"}


@app.route("/home")
def home():
    return {"message": "Hello from home"}


# Welcome
api.add_resource(WelcomeResource.Welcome, "/")

# Painting
api.add_resource(PaintResource.Paint, "/paint", methods=["POST", "GET", "PATCH", "PUT"])

# Queue
api.add_resource(QueueResource.QueueResource, "/queue", methods=["GET", "PUT"])
