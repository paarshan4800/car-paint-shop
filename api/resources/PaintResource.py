from flask_restful import Resource
import time
from datetime import datetime

from api import *
from api.models import PaintJobModel
from api.validators.PaintValidator import *


class Paint(Resource):
    # Get Paint Jobs available
    def get(self):
        try:
            data = paintJobs
            return {"data": data}, 200
        except:
            return {"message": "Server Error"}, 500

    def paint(self, color):
        lock.acquire()  # Acquire the painting area
        print("--- Painting {} at {} ---".format(queue.getFront(), datetime.now().time()))
        time.sleep(5)
        paintJob = PaintJobModel.PaintJobModel(color=color)
        db.session.add(paintJob)
        db.session.commit()
        lock.release()  # Release the painting area

    # Request Paint Job
    def post(self):
        try:
            args = paint_car_args.parse_args()

            color = args["color"]

            # Invalid Paint Job
            if color not in paintJobs:
                return {"message": "Invalid Paint Job"}, 200

            # If specific paint job not available
            if not paintJobs[color]:
                return {"message": "Requested Paint Job not available"}, 200

            # If queue is full
            if queue.isQueueFull():
                return {"message": "Queue full. Please wait"}, 200

            queue.push(args["num"])
            print("--- Car {} added to the queue ---".format(args["num"]))

            self.paint(color)

            print("--- Car {} left the queue ---".format(queue.pop()))

            return {"message": queue.getLength()}, 200
        except Exception as e:
            return {"message": "Server Error {}".format(e)}, 500

    def patch(self):  # Close Specific Painting Area
        try:
            args = paint_area_status_args.parse_args()
            color = args["color"]
            status = bool(args["status"])

            # Invalid Paint Job
            if color not in paintJobs:
                return {"message": "Invalid Paint Job"}, 200

            txt = "opened" if status else "closed"

            # If already opened or closed
            if paintJobs[color] == status:
                return {"message": "Already {}".format(txt)}

            # Change paint area status
            paintJobs[color] = status

            return {"message": "{} {} area".format(txt.capitalize(), color)}, 200
        except:
            return {"message": "Server Error"}, 500
