from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
from dataclasses import dataclass


db = SQLAlchemy()

@dataclass
class User(db.Model):
    ## For API JSON reponse
    id: int
    email: str
    full_name: str
    ##

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String())
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)

    ## Auto generated timestamps for creation & update of the row
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    ## Method to instanciate class (doesnt save in the database)
    def __init__(self, full_name, email, password_hash):
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash

    ## Method to print the class in the terminal: print(User)
    def __repr__(self):
        return f"<User ({self.id}): {self.email}>"

    ## Method to hash a password with Bcrypt
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password).decode('utf8')
 
    ## Method to compare a password with an hashed string
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@dataclass
class Rating(db.Model):
    ## For API JSON reponse
    id: int
    score: int
    user_id: int
    recipe_id: str
    description: str
    created_at: datetime
    updated_at: datetime
    ##

    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    recipe_id = db.Column(db.String(), nullable=False) ## must be a valid strapi recipe id
    description = db.Column(db.String())
    
    ## Auto generated timestamps for creation & update of the row
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, score, user_id, recipe_id, description):
        self.score = score
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.description = description

    def __repr__(self):
        return f"<Rating by user {self.user_id} for recipe {self.recipe_id}>"