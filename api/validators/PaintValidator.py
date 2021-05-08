from flask_restful import reqparse

paint_car_args = reqparse.RequestParser()
paint_car_args.add_argument(
    "num", type=int, help="Car Number Required", required=True)
paint_car_args.add_argument(
    "color", type=str, help="Paint Color Required", required=True)

paint_area_status_args = reqparse.RequestParser()
paint_area_status_args.add_argument("color", type=str, help="Paint color required", required=True)
paint_area_status_args.add_argument("status", type=bool, help="Paint area status required", required=True)
