from api.validators.UserValidator import validateEmail


def validateDeleteUserRoute(req):
    # Check for keys
    if "email" not in req:
        return False, {"message": "Email is required"}, 400

    email = req["email"]

    # Validate values
    if len(email) == 0 or not validateEmail(email):
        return False, {"message": "Email is required"}, 400

    return True, {}, 200


def validateRegisterRoute(req):
    # Check for keys
    if "email" not in req:
        return False, {"message": "Email is required"}, 400

    if "password" not in req:
        return False, {"message": "Password is required"}, 400

    if "c_password" not in req:
        return False, {"message": "Confirmation Password is required"}, 400

    if "name" not in req:
        return False, {"message": "Name is required"}, 400

    email = req["email"]
    name = "".join(req["name"].split())
    password = "".join(req["password"].split())
    c_password = "".join(req["c_password"].split())

    # Validate values
    if len(email) == 0 or not validateEmail(email):
        return False, {"message": "Invalid Email"}, 400

    if len(password) < 8 or len(c_password) < 8:
        return False, {"message": "Invalid Password (Minimum 8 characters)"}, 400

    if len(name) < 4:
        return False, {"message": "Invalid Name (Minimum 4 characters)"}, 400

    return True, {}, 200


def validateLoginRoute(req):
    # Check for keys
    if "email" not in req:
        return False, {"message": "Email is required"}, 400

    if "password" not in req:
        return False, {"message": "Password is required"}, 400

    return True, {}, 200


def validateResetPasswordRequestRoute(req):
    # Check for keys
    if "email" not in req:
        return False, {"message": "Email is required"}, 400

    return True, {}, 200


def validateResetPasswordRoute(req):
    # Check for keys
    if "token" not in req:
        return False, {"message": "Token is required"}, 400

    if "password" not in req:
        return False, {"message": "Password is required"}, 400

    if "c_password" not in req:
        return False, {"message": "Confirmation Password is required"}, 400

    password = "".join(req["password"].split())
    c_password = "".join(req["c_password"].split())

    # Validate values
    if len(password) < 8 or len(c_password) < 8:
        return False, {"message": "Invalid Password (Minimum 8 characters)"}, 400

    return True, {}, 200


def validateTwoFactorAuthRoute(req):
    # Check for keys
    if "token" not in req:
        return False, {"message": "Token is required"}, 400

    if "otp" not in req:
        return False, {"message": "OTP is required"}, 400

    return True, {}, 200