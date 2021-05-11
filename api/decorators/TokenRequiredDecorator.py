from functools import wraps
from flask import request
import jwt
from jwt import InvalidSignatureError, ExpiredSignatureError

from api import app, ACCESSTOKEN
from api.misc.ErrorResponse import getServerErrorResponse
from api.services.AuthVerificationServices import isUserVerified
from api.services.TokenServices import decodeToken
from api.services.UserServices import getUser


def tokenRequired(f):
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
                print(data["type"])
                return {"message": "Invalid authorization token"}, 401

            # Check if user is verified or not
            if not isUserVerified(user.email):
                return {"message": "Account not verified. Verification mail sent."}, 401

            return f(user, *args, **kwargs)

        except (InvalidSignatureError, ExpiredSignatureError) as e:
            return {"message": "Invalid or Expired Authorization Token"}, 400

        except:
            return getServerErrorResponse()

    return decorated
