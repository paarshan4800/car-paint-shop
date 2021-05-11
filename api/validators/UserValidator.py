import re

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def validateEmail(email):
    if re.search(regex, email):
        return True
    else:
        return False


def validateDeleteUserRoute(req):
    # Check for keys
    if "email" not in req:
        return False, {"message": "Email is required"}, 400

    email = req["email"]

    # Validate values
    if len(email) == 0 or not validateEmail(email):
        return False, {"message": "Email is required"}, 400

    return True, {}, 200
