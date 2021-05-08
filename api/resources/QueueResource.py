from flask_restful import Resource
from api import *

from api.validators.QueueValidator import *


class QueueResource(Resource):

    # Get Queue Length
    def get(self):
        try:
            data = {
                "length": queue.getLength(),
                "maxCapacity": queue.getMaxCapacity()
            }
            return {"message": "Returned Queue Length and Max Capacity", "data": data}, 200
        except:
            return {"message": "Server Error"}, 500

    # Update Queue Length
    def put(self):
        try:
            args = queue_length_update_args.parse_args()
            length = int(args["length"])

            if length < 0:
                return {"message": "Invalid queue length"}, 200

            queue.setMaxCapacity(length)
            return {"message": "Changed queue max capacity", "data": length}, 200

        except:
            return {"message": "Server Error"}, 500
