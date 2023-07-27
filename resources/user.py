from flask import request, Response
from flask_restful import Resource
from database.models import User
from database.db import db

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        req_email = body["email"]
        req_password = body["password"]

        data = User(email=req_email, password=req_password)
        data.hash_password()
        db.session.add(data)
        db.session.commit()
        id = data.id
        return {'id':str(id)}

class LoginApi(Resource):
    def post(self, id):
        body = request.get_json()
        req_email = body["email"]
        req_password = body["password"]
        user = User.query.filter_by(email=req_email).first()
        check = user.check_password(req_password)
        if not check :
            return {'error':'Email or password is invalid'}, 401
        return {'Login Successful'}, 200

        