import logging

from api import app, APIDOCS_URL
from api.misc.ErrorResponse import getServerErrorResponse
from flask import redirect


# Welcome Route
@app.route("/", methods=["GET"])
def welcome():
    try:
        return {
                   "message": "Hello mate. Welcome to Car Paint Shop API. You can find the API docs at the below link. Cheers!",
                   "link": "https://car-paint-shop.herokuapp.com/api-docs"
               }, 200

    except Exception as e:
        logging.error("Error in welcome route - {}".format(e))
        return getServerErrorResponse()


@app.route("/api-docs")
def apiDocs():
    return redirect(APIDOCS_URL)
