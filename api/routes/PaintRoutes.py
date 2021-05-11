from flask import request

from api import *
from api.decorators.AdminOnlyDecorator import adminOnly

from api.misc.ErrorResponse import getServerErrorResponse

from api.services.PaintServices import requestPaint, getAllPaintJobs, closeSpecificPaintingArea, \
    getAllPaintJobRecords
from api.validators.PaintValidator import validateClosePaintAreaRoute, \
    validateRequestPaintJobRoute
from api.decorators.TokenRequiredDecorator import tokenRequired


# Get All Paint Job Records
@app.route("/paint/getAllRecords", methods=["GET"])
@adminOnly
def getAllPaintJobRecordsRoute(user):
    try:
        return getAllPaintJobRecords()
    except Exception as e:
        logging.error("Error in getting all paint job records - {}".format(e))
        return getServerErrorResponse()


# Get Paint Jobs available
@app.route("/paint/getAvailable", methods=["GET"])
def getAvailablePaintJobsRoute():
    try:
        return getAllPaintJobs()
    except Exception as e:
        logging.error("Error in getting available paint job - {}".format(e))
        return getServerErrorResponse()


# Request Paint Job
@app.route("/paint/request", methods=["POST"])
@tokenRequired
def requestPaintJobRoute(user):
    try:
        req = request.get_json(force=True)

        # Validate
        condition, msg, status = validateRequestPaintJobRoute(req)

        # Validation check
        if not condition:
            return msg, status

        return requestPaint(req, user)

    except Exception as e:
        logging.error("Error in painting car - {}".format(e))
        return getServerErrorResponse()


# Close Specific Painting Area
@app.route("/paint/closeArea", methods=["PATCH"])
@adminOnly
def closePaintAreaRoute(user):
    try:
        req = request.get_json(force=True)

        # Validate
        condition, msg, status = validateClosePaintAreaRoute(req)

        # Validation check
        if not condition:
            return msg, status

        return closeSpecificPaintingArea(req)

    except Exception as e:
        logging.error("Error in closing paint area - {}".format(e))
        return getServerErrorResponse()
