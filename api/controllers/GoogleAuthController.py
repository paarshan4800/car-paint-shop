import json

import requests

from flask import request
from api import app, db, client
from api.controllers.AuthController import generateToken
from api.controllers.UserController import getUser
from api.models.UserModel import User


def getGoogleProviderConfiguration():
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()


def googleLogin():
    googleProviderConfiguration = getGoogleProviderConfiguration()
    authorizationEndpoint = googleProviderConfiguration["authorization_endpoint"]
    print(authorizationEndpoint)

    requestURI = client.prepare_request_uri(
        authorizationEndpoint,
        redirect_uri=app.config['APP_BASE_URL'] + "/callback",
        scope=["openid", "email", "profile"],
    )

    return requestURI


def googleCallback():
    code = request.args.get("code")
    googleProviderConfiguration = getGoogleProviderConfiguration()
    tokenEndpoint = googleProviderConfiguration["token_endpoint"]

    tokenURL, headers, body = client.prepare_token_request(
        tokenEndpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    tokenResponse = requests.post(
        tokenURL,
        headers=headers,
        data=body,
        auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
    )

    client.parse_request_body_response(json.dumps(tokenResponse.json()))

    userInfoEndpoint = googleProviderConfiguration["userinfo_endpoint"]
    uri, headers, body = client.add_token(userInfoEndpoint)
    userInfoResponse = requests.get(uri, headers=headers, data=body)

    userInfo = userInfoResponse.json()
    print(userInfo)

    if not userInfo.get("email_verified"):
        return {"message": "User email not verified by Google"}, 400

    user = getUser(userInfo.get("email"))

    if user is None:  # Register
        user = User(
            email=userInfo.get("email"),
            name=userInfo.get("name"),
            admin=False,
            external_id=userInfo.get("sub"),
            type="GOOGLE"
        )
        db.session.add(user)
        db.session.commit()

    # Generate Token
    token = generateToken(user.email)
    return {"message": "Logged in Successfully", "token": token}, 200
