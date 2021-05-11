import logging

from api import app, APIDOCS_URL
from api.misc.ErrorResponse import getServerErrorResponse
from flask import redirect


# Welcome Route
@app.route("/", methods=["GET"])
def welcome():
    try:
        return {"message": "Hello mate. This is from CTF Student Directors Recruitment Task API. Cheers!"}, 200

    except Exception as e:
        logging.error("Error in welcome route - {}".format(e))
        return getServerErrorResponse()


@app.route("/api-docs")
def apiDocs():
    return redirect(APIDOCS_URL)
