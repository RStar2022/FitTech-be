from flask import request, jsonify, Response
from flask_restful import Resource
from database.models import Profile, User
from database.db import db

class ProfileApi(Resource):
    def get(self):
        get_profile = Profile.query.to_json()
        return Response(get_profile, mimetype="application/json", status=200)
    
    def post(self):
        body = request.get_json()
        req_name = body["name"]
        req_age = body["age"]
        req_gender =body["gender"]
        req_hobby = body["hobby"]
        req_desc = body["desc"]
        data = Profile(name=req_name, age=req_age,
                       gender= req_gender, hobby = req_hobby,
                       desc=req_desc)
        db.session.add(data)
        db.session.commit()

        id = data.id
        return {'id':str(id)}, 200
    
class ProfilesApi(Resource):
    def get(self, id):
        profile_info = Profile.query.filter_by(id=id).first()
        if not profile_info :
            return "Not Found", 404
        return jsonify(profile_info.to_json())
    
    def put(self, id):
        profile = Profile.query.filter_by(id=id).first()
        body = request.get_json()

        profile.name = body["name"]
        db.session.commit()

        profile.age = body["age"]
        db.session.commit()

        profile.gender = body["gender"]
        db.session.commit()

        profile.hobby = body["hobby"]
        db.session.commit()

        profile.desc = body["desc"]
        db.session.commit()

        return 'Update successful', 200

    