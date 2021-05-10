from api import api, app
from api.misc.ServerError import getServerErrorResponse


# Welcome Route
@app.route("/", methods=["GET"])
def welcome():
    try:
        return {"message": "Hello everyone. This is from CTF Student Directors Recruitment Task API"}, 200

    except:
        return getServerErrorResponse()

