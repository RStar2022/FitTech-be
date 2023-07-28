from flask import Flask, current_app, request, Response
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from resources.profile import ProfileApi, ProfilesApi
from resources.user import SignupApi, LoginApi
from flask_cors import CORS
from database.db import db

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://hacks:hacks123@localhost/fittech"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_envvar('ENV_FILE_LOCATION')

db.init_app(app)

with app.app_context():
    try:
       db.create_all()
    except Exception as ex :
        print("Got wrong create all"+str(ex))      

api = Api(app)
api.add_resource(SignupApi, '/signup')
api.add_resource(LoginApi, '/login')
api.add_resource(ProfileApi, '/profiles')
api.add_resource(ProfilesApi, '/profiles/<id>')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

with app.app_context():
    @current_app.before_request
    def basic_authentication():
        if request.method.lower() == 'options':
            return Response()

if __name__ ==  '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)