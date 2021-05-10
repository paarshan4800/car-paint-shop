def validateRequestPaintJobRoute(req):
    # Check for keys
    if "color" not in req:
        return False, {"message": "Color is required"}, 400
    if "model" not in req:
        return False, {"message": "Model is required"}, 400

    model = "".join(req["model"].split())
    color = "".join(req["color"].split())

    # Validate values
    if len(model) == 0:
        return False, {"message": "Model name is required"}, 400

    if len(color) == 0:
        return False, {"message": "Color is required"}, 400

    return True, {}, 200


def validateClosePaintAreaRoute(req):
    # Check for keys
    if "color" not in req:
        return False, {"message": "Color is required"}, 400
    if "status" not in req:
        return False, {"message": "Status is required"}, 400

    color = "".join(req["color"].split())
    status = req["status"]

    # Validate values
    if len(color) == 0:
        return False, {"message": "Color is required"}, 400

    if type(status) != bool:
        return False, {"message": "Invalid Status"}, 400

    return True, {}, 200
