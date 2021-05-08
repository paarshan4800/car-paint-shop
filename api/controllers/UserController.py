from api.models.UserModel import User
from werkzeug.security import generate_password_hash, check_password_hash
from api import db


def getUser(email):
    return User.query.filter_by(email=email).first()


def deleteUser(email):
    # Check user exists or not
    user = getUser(email)
    if user is None:
        return {"message": "User doesn't exist"}, 404

    if user.admin:
        return {"message": "Cannot delete an admin"}, 404

    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}, 200


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


def createUser(args):
    # Check email already used or not
    if getUser(args["email"]) is not None:
        return {"message": "Email already in use"}, 200

    hashedPwd = generate_password_hash(args["password"], method='sha256')
    user = User(
        email=args["email"],
        password=hashedPwd,
        name=args["name"],
        admin=False,
        type="NORMAL"
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "User Created Successfully"}, 201
