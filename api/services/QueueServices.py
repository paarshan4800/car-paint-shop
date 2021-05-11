import logging

from api import queue


def getQueueDetails():
    data = {
        "length": queue.getLength(),
        "maxCapacity": queue.getMaxCapacity()
    }
    return {"message": "Returned Queue Length and Max Capacity", "data": data}, 200


def updateQueueLength(req):
    maxCapacity = req["maxCapacity"]
    queue.setMaxCapacity(maxCapacity)
    logging.info("Queue Capacity updated to {}".format(maxCapacity))

    return {"message": "Changed queue max capacity", "data": maxCapacity}, 200
