from functools import wraps

import jwt
from flask import request
from jwt import InvalidSignatureError, ExpiredSignatureError

from api import ACCESSTOKEN
from api.misc.ErrorResponse import getServerErrorResponse
from api.services.TokenServices import decodeToken
from api.services.UserServices import getUser


def adminOnly(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = None

            # Check whether access token is included in the headers
            if "access-token" in request.headers:
                token = request.headers["access-token"]

            if not token:
                return {"message": "Access token is required"}, 401

            data = decodeToken(token)  # Decode token

            user = getUser(data["email"])

            # Check if the user exists and correct token type
            if user is None or data["type"] != ACCESSTOKEN:
                return {"message": "Invalid authorization token"}, 401

            # If the user is not an admin
            if not user.admin:
                return {"message": "Admin access required"}, 401

            return f(user,*args, **kwargs)

        except (InvalidSignatureError, ExpiredSignatureError) as e:
            return {"message": "Invalid or Expired Authorization Token"}, 400

        except Exception as e:
            print(e)
            return getServerErrorResponse()

    return decorated
