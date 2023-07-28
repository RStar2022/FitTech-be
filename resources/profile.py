from flask import request, jsonify, Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Profile, User
from database.db import db

class ProfileApi(Resource):
    def get(self):
        get_profile = Profile.query.to_json()
        return Response(get_profile, mimetype="application/json", status=200)
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        body = request.get_json()
        req_name = body["name"]
        req_age = body["age"]
        req_gender =body["gender"]
        req_hobby = body["hobby"]
        req_desc = body["desc"]
        data = Profile(name=req_name, age=req_age,
                       gender= req_gender, hobby = req_hobby,
                       desc=req_desc, added_by=[user])
        db.session.add(data)
        db.session.commit()

        id = data.id
        return {"id" :str(id)}, 200
    
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        profile = Profile.query.filter(Profile.added_by.any(id=user_id)).first()
        body = request.get_json()
        profile.name = body["name"]
        profile.age = body["age"]
        profile.gender = body["gender"]
        profile.hobby = body["hobby"]
        profile.desc = body["desc"]
        db.session.commit()
        return 'Update successful', 200
    
class ProfilesApi(Resource):
    def get(self, id):
        profile_info = Profile.query.filter(Profile.added_by.any(id=id)).first()
        if not profile_info:
            return "Not Found", 404
        return jsonify(profile_info.to_json())
    
    

    