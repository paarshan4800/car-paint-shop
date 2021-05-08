from flask_restful import reqparse

queue_length_update_args = reqparse.RequestParser()
queue_length_update_args.add_argument(
    "maxCapacity", type=int, help="Queue max capacity required", required=True)
