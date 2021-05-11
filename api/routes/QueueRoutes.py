from flask import request

from api import *
from api.decorators.AdminOnlyDecorator import adminOnly
from api.decorators.TokenRequiredDecorator import tokenRequired
from api.misc.ErrorResponse import getServerErrorResponse
from api.services.QueueServices import getQueueDetails, updateQueueLength
from api.validators.QueueValidator import validateUpdateQueueLengthRoute


# Get queue length
@app.route("/queue/getLength", methods=["GET"])
@tokenRequired
def getQueueLengthRoute(user):
    try:
        return getQueueDetails()
    except Exception as e:
        logging.error("Error in getting queue details - {}".format(e))
        return getServerErrorResponse()


# Update Queue Length
@app.route("/queue/updateLength", methods=["PUT"])
@adminOnly
def updateQueueLengthRoute(user):
    try:
        req = request.get_json(force=True)

        # Validate
        condition, msg, status = validateUpdateQueueLengthRoute(req)

        # Validation check
        if not condition:
            return msg, status

        return updateQueueLength(req)

    except Exception as e:
        logging.error("Error in updating queue details - {}".format(e))
        return getServerErrorResponse()
