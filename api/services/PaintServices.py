from datetime import datetime

from api import *
import time

from api.models.PaintJobModel import PaintJob


def getAllPaintJobRecords():
    paintJobRecords = PaintJob.query.all()

    res = []
    for record in paintJobRecords:
        res.append({
            "id": record.id,
            "color": record.color,
            "paintedTime": record.painted_time,
            "user": record.user_email
        })

    return {
               "message": "All paint job records returned",
               "data": res
           }, 200


def getAllPaintJobs():
    res = []
    for key, value in paintJobs.items():
        res.append({
            "color": key,
            "status": value
        })

    return {
               "message": "All paint jobs with its status returned",
               "data": res
           }, 200


def paintCar(color, user, model):
    lock.acquire()  # Acquire the painting area

    logging.info("Painting {} - {} at {}".format(queue.getFront().email, model, datetime.now().time()))
    time.sleep(20)

    # Add to DB
    paintJob = PaintJob(color=color, model=model, user=user)
    db.session.add(paintJob)
    db.session.commit()

    lock.release()  # Release the painting area


def requestPaint(req, user):
    color = req["color"]
    model = "".join(req["model"].split())

    # Invalid Paint Job
    if color not in paintJobs:
        return {"message": "Invalid Paint Job"}, 200

    # If specific paint job not available
    if not paintJobs[color]:
        return {"message": "Requested Paint Job not available"}, 200

    # If queue is full
    if queue.isQueueFull():
        return {"message": "Queue full. Please wait"}, 200

    queue.push(user)  # Add user to the queue
    logging.info("{} - {} added to the queue".format(user.email, model))

    paintCar(color, user, model)  # Paint

    leftTheQueue = queue.pop()  # Remove user from the queue
    logging.info("Car {} - {} left the queue".format(leftTheQueue.email, model))

    return {"message": "Paint Work completed successfully"}, 200


def closeSpecificPaintingArea(req):
    color = req["color"]
    status = bool(req["status"])

    # Invalid Paint Job
    if color not in paintJobs:
        return {"message": "Invalid Paint Job"}, 200

    txt = "opened" if status else "closed"

    # If already opened or closed
    if paintJobs[color] == status:
        return {"message": "Already {}".format(txt)}

    # Change paint area status
    paintJobs[color] = status
    logging.info("{} {} area".format(txt.capitalize(), color))

    return {"message": "{} {} area".format(txt.capitalize(), color)}, 200
