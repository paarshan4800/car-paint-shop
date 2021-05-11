from api import db
from datetime import datetime


class PaintJob(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    painted_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

    def __repr__(self):
        return "ID - {} Color - {} Time - {}".format(self.id, self.color, self.painted_time)
