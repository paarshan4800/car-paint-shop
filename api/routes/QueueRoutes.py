from flask import request

from api import *
from api.misc.ServerError import getServerErrorResponse
from api.services.QueueServices import getQueueDetails, updateQueueLength
from api.validators.QueueValidator import validateUpdateQueueLengthRoute


# Get queue length
@app.route("/getQueueLength", methods=["GET"])
def getQueueLengthRoute():
    try:
        return getQueueDetails()
    except:
        return getServerErrorResponse()


# Update Queue Length
@app.route("/updateQueueLength", methods=["PUT"])
def updateQueueLengthRoute():
    try:
        req = request.get_json(force=True)

        # Validate
        condition, msg, status = validateUpdateQueueLengthRoute(req)

        # Validation check
        if not condition:
            return msg, status

        return updateQueueLength(req)

    except:
        return getServerErrorResponse()
