import logging

from api import api, app
from api.misc.ErrorResponse import getServerErrorResponse


# Welcome Route
@app.route("/", methods=["GET"])
def welcome():
    try:
        return {"message": "Hello mate. This is from CTF Student Directors Recruitment Task API. Cheers!"}, 200

    except Exception as e:
        logging.error("Error in welcome route - {}".format(e))
        return getServerErrorResponse()
