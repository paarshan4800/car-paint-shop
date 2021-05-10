from api.models.UserModel import User
from api import db


def getUser(email):
    return User.query.filter_by(email=email).first()


def getAllUsers():
    users = User.query.all()
    res = []
    for user in users:
        userData = {
            "email": user.email,
            "name": user.name,
            "admin": user.admin
        }
        res.append(userData)

    return {"message": "Returned list of all users", "data": res}, 200


def deleteUser(req):
    email = req["email"]

    # Check user exists or not
    user = getUser(email)
    if user is None:
        return {"message": "User doesn't exist"}, 404

    # Cannot delete an admin
    if user.admin:
        return {"message": "Cannot delete an admin"}, 404

    # Delete user from DB
    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted successfully"}, 200
