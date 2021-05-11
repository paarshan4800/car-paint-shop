def getServerErrorResponse():
    return {"message": "Server Error"}, 500


def getInvalidTokenErrorResponse():
    return {"message": "Invalid or Expired Token"}, 400
