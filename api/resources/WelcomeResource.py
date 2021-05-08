from flask_restful import Resource


class Welcome(Resource):

    def get(self):
        return {"message": "Hello everyone. This is from CTF Student Directors Recruitment Task API"}, 201
