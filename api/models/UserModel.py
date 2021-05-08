from api import db


class User(db.Model):
    email = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    external_id = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "Email - {} Name - {} Admin - {} Type - {}".format(self.email, self.name, self.admin, self.type)
