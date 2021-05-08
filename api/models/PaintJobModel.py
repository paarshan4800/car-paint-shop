from api import db
from datetime import datetime


class PaintJobModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(100))
    painted_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "ID - {} Color - {} Time - {}".format(self.id,self.color, self.painted_time)
