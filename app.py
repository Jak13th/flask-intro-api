from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from database.models import db
from services.strapi import initialize_strapi
from resources.users import UsersApi, UserApi
from resources.ratings import RatingsAPI, RatingsRecipesAPI, RatingsUpdateAPI, DeleteRatingAPI
from resources.recipes import RecipesAPI, RecipeAPI
from resources.chefs import ChefsAPI, ChefAPI, ChefUpdateAPI
from resources.auth import SignupApi, LoginApi, SessionAPI

app = Flask(__name__, instance_relative_config=True)

# Loads configuration from config.py
app.config.from_object('config')
## From here you can access config variables like this:
## value_from_config = app.config['CONFIG_VARIABLE_NAME']

## Initialisation des modules

db.init_app(app)
migrate = Migrate(app, db)
initialize_strapi(app)
api = Api(app)
Bcrypt(app)
JWTManager(app)

## Declaration of API routes

api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')
api.add_resource(SessionAPI, '/auth/me')

api.add_resource(UsersApi, '/users')
api.add_resource(UserApi, '/users/<userId>')

api.add_resource(RatingsAPI, '/ratings')
api.add_resource(RatingsRecipesAPI, '/ratings/recipes/<recipeId>')
api.add_resource(RatingsUpdateAPI, '/ratings/recipes/<recipeId>')
api.add_resource(DeleteRatingAPI, '/ratings/<ratingId>')

api.add_resource(RecipesAPI, '/recipes')
api.add_resource(RecipeAPI, '/recipes/<recipeId>')

api.add_resource(ChefsAPI, '/chefs')
api.add_resource(ChefAPI, '/chefs/<chefId>')
api.add_resource(ChefUpdateAPI, '/chefs/<chefId>/recipe/<recipeId>')


@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World"})