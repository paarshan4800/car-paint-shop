from flask_restful import reqparse
import re

user_create_args = reqparse.RequestParser(bundle_errors=True)
user_create_args.add_argument(
    "email", type=str, help="Email Required : {error_msg}", required=True)
user_create_args.add_argument(
    "password", type=str, help="Password Required", required=True)
user_create_args.add_argument(
    "name", type=str, help="Name Required", required=True)

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
