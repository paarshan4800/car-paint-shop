class Queue:
    def __init__(self, maxCapacity):
        self.queue = list()
        self.maxCapacity = maxCapacity

    def push(self, value):
        if self.isQueueFull():
            # Queue full
            return False

        self.queue.append(value)
        return True

    def pop(self):
        if self.isQueueEmpty():
            # Queue empty
            return False

        return self.queue.pop(0)

    def getLength(self):
        return len(self.queue)

    def getFront(self):
        if self.getLength() == 0:
            # Queue empty
            return False

        return self.queue[0]

    def isQueueFull(self):
        if self.getLength() == self.maxCapacity:
            return True
        else:
            return False

    def isQueueEmpty(self):
        if self.getLength() == 0:
            return True
        else:
            return False

    def getMaxCapacity(self):
        return self.maxCapacity

    def setMaxCapacity(self, maxCapacity):
        self.maxCapacity = maxCapacity

    def getQueue(self):
        return self.queue




