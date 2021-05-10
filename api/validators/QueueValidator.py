def validateUpdateQueueLengthRoute(req):
    # Check for keys
    if "maxCapacity" not in req:
        return False, {"message": "Queue Length is required"}, 400

    maxCapacity = req["maxCapacity"]

    # Validate values
    if type(maxCapacity) != int or maxCapacity < 0:
        return False, {"message": "Invalid Maximum Capacity"}, 400

    return True, {}, 200
