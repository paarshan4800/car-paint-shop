from flask_restful import reqparse

user_create_args = reqparse.RequestParser(bundle_errors=True)
user_create_args.add_argument(
    "email", type=str, help="Email Required : {error_msg}", required=True)
user_create_args.add_argument(
    "password", type=str, help="Password Required", required=True)
user_create_args.add_argument(
    "name", type=str, help="Name Required", required=True)
