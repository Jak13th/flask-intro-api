from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from services.strapi import strapi
from database.models import db, Rating
import requests
from flask import current_app

class RatingsAPI(Resource):
    @jwt_required()
    def get(self):
        rating = Rating.query.all()
        return jsonify(rating)
    
    @jwt_required()
    def post(self):
        body = request.get_json()
        score = body.get('score')
        if score == None or (score < 0 or score > 5):
            return {'error': 'Review score must be between 0 and 5'}, 400
        try:
            recipe_id = body.get('recipe_id')

            ## checking if the recipe exists in the Strapi API
            strapi_recipe = strapi.get('/recipes/' + recipe_id)
            if strapi_recipe == None:
                return {'error': 'The specified recipe %s doesnt exist' % recipe_id }, 404
            
            # extract info from the jwt token
            user_id = get_jwt_identity()
            existing_rating = Rating.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
            if existing_rating:
                return {'error': 'You have already reviewed this recipe'}, 400
            rating = Rating(
                score=body.get('score'),
                user_id=user_id,
                recipe_id=body.get('recipe_id'),
                description=body.get('description')
            )
            db.session.add(rating)
            db.session.commit()
            return jsonify(rating)
        ## triggered if Strapi API call fails
        except requests.exceptions.HTTPError as err:
            return {'error': 'The specified recipe %s doesnt exist' % recipe_id}, 404
        except Exception as e:
            print(e)
            return {'error': 'Couldnt create recipe because : %s' % e}, 400

# GET
class RatingsRecipesAPI(Resource):
    @jwt_required()
    def get(self, recipeId):
        rating = Rating.query.filter_by(recipe_id = recipeId).all()
        return jsonify(rating)

# PUT
class RatingsUpdateAPI(Resource):
    @jwt_required()
    def put(self, recipeId):
        body = request.get_json()
        user_id = get_jwt_identity()
        existing_rating = Rating.query.filter_by(user_id=user_id, recipe_id=recipeId).first()
        if existing_rating:
            existing_rating.score = body.get('score')
            existing_rating.description = body.get('description')
        else:
            {'error': 'The specified recipe %s doesnt exist' % recipeId }, 400
        db.session.add(existing_rating)
        db.session.commit()
        return jsonify(existing_rating)

class DeleteRatingAPI(Resource):
    @jwt_required()
    def delete(self, ratingId):
        user_id = get_jwt_identity()
        # à vérifier que le rating existe bien: If_ 
        existing_rating = Rating.query.filter_by(user_id=user_id, id=ratingId).first()
        if existing_rating:
            db.session.delete(existing_rating)
        else:
            {'error': 'The specified recipe %s doesnt exist' % ratingId }, 400
        db.session.commit()
        return True