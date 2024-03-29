import logging

from api import app
from flask import request
from api.decorators.AdminOnlyDecorator import adminOnly
from api.misc.ErrorResponse import getServerErrorResponse
from api.services.UserServices import getAllUsers, deleteUser

from api.validators.UserValidator import validateDeleteUserRoute


# Get all users
@app.route("/user", methods=["GET"])
@adminOnly
def getUsers(user):
    try:
        return getAllUsers()

    except Exception as e:
        logging.error("Error in getting all user details - {}".format(e))
        return getServerErrorResponse()


# Delete user
@app.route("/user", methods=["DELETE"])
@adminOnly
def deleteUserRoute(user):
    try:
        req = request.get_json(force=True)

        # Validate
        condition, msg, status = validateDeleteUserRoute(req)

        # Validation check
        if not condition:
            return msg, status

        return deleteUser(req)

    except Exception as e:
        logging.error("Error in deleting user - {}".format(e))
        return getServerErrorResponse()
