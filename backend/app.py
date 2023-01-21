import os

from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from firebase_admin import auth, initialize_app, credentials

app = Flask(__name__)

# Credentials for firebase
cred = credentials.Certificate("./assets/secret.json")
default_app = initialize_app(cred)

# THIS IS ONLINE
app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://app:RYfC6wsILFZtZu1b7rOjmQ@void-carp-6949.5xj.cockroachlabs.cloud:26257/db1?sslmode=verify-full" 
# app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://root@localhost:26257/db1?sslmode=disable"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

CORS(app)

### Tabels ###
liked_recipes_table = db.Table('LikedRecipes',
                            db.Column('recipe_id', db.Integer, db.ForeignKey(
                                'recipe.id'), primary_key=True),
                            db.Column('user_id', db.Integer, db.ForeignKey(
                                'user.id'), primary_key=True)
                            )

### Models ###
class Recipe(db.Model, SerializerMixin):
  serialize_only = ('id', 'name', 'description', 'minutes', 'tags', 'ingredients',
                    'calories', 'total_fat', 'sugar', 'sodium', 'saturated_fat',
                    'n_steps', 'steps')
  # serialize_rules = ('-employees', '-job_postings') # exluded from serialization.

  id = db.Column(db.Integer, primary_key=True, unique=True)

  name = db.Column(db.String(1000), nullable=False)
  description = db.Column(db.String(4000))

  minutes = db.Column(db.Integer)
  tags = db.Column(db.String(4000))
  ingredients = db.Column(db.String(4000))

  calories = db.Column(db.Float)
  total_fat = db.Column(db.Float)
  sugar = db.Column(db.Float)
  sodium = db.Column(db.Float)
  saturated_fat = db.Column(db.Float)

  n_steps = db.Column(db.Integer)
  steps = db.Column(db.String(4000))

  # user_ratings = db.relationship(
  #       'User', secondary=liked_recipes, backref='user_ratings', lazy=True)

class User(db.Model, SerializerMixin):
  serialize_only = ('id', 'username', 'email')
  serialize_rules = ('-liked_recipes',)

  id = db.Column(db.Integer, primary_key=True, unique=True)
  username = db.Column(db.String(1000), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)

  liked_recipes = db.relationship('Recipe', secondary=liked_recipes_table, backref="user_ratings", lazy=True)


@app.route("/init-db", methods=['POST', 'GET'])
def init_db():
  db.drop_all()
  db.create_all()

  r1 = Recipe(id=0, name="Ibrahim's Tomato Eggs!", description="", minutes=15, tags=['vegetarian'],
              ingredients=['eggs', 'tomatoes'], calories=0.0, total_fat=0.0, sugar=0.0, sodium=0.0,
              saturated_fat=0.0, n_steps=5, steps=['make eggs and put tomatoes bruh'])
  
  r2 = Recipe(id=1, name="Kenneth's Fried Rice!")
  r3 = Recipe(id=2, name="Chicken Lo Mein!")
  r4 = Recipe(id=3, name="Qdoba!")

  db.session.add(r1)
  db.session.add(r2)
  db.session.add(r3)
  db.session.add(r4)

  u1 = User(id=0, username='cheesus', email='ibrahim@gmail.com')
  u2 = User(id=1, username='kenneth', email='Kenneth@gmail.com')

  u1.liked_recipes.append(r1)
  u2.liked_recipes.append(r3)
  u2.liked_recipes.append(r4)
  db.session.add(u1)

  db.session.commit()
  return "Databse initalized successfully", 200

# Get all recipes from database

@app.route("/user/all", methods=['GET'])
def getAllUsers():
  try:
    users = User.query.all()
    users_dicts = [x.to_dict() for x in users]

    for i in range(len(users_dicts)):
      users_dicts[i]['liked_recipes'] = [recipe.to_dict() for recipe in users[i].liked_recipes]


    return jsonify({"users": users_dicts}), 200

  except Exception as exception:
    return f"{exception}"

@app.route("/user/<string:id>", methods=['GET'])
def get_user_by_id(id):
  try:
    user = User.query.filter_by(id = id).first()
    user_dict = user.to_dict()

    user_dict['liked_recipes'] = [recipe.to_dict() for recipe in user.liked_recipes]


    return jsonify({"user": user_dict}), 200

  except Exception as exception:
    return f"{exception}"

@app.route("/recipe/all", methods=['GET'])
def getAllRecipes():
  try:
    recipes = Recipe.query.all()
    recipes_dict = [c.to_dict() for c in recipes]
    return jsonify({"recipes": recipes_dict}), 200

  except Exception as exception:
    return f"{exception}"

# Get specific recipe from database
@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_specific_recipe(recipe_id):
  try:
    recipe = Recipe.query.filter_by(id = recipe_id).first()
    if recipe:
      recipe_dic = recipe.to_dict()
      print(recipe_dic)
      return jsonify({'recipe': recipe_dic}), 200
    else:
      return jsonify({'recipe': None}), 404
  except Exception as exception:
    return f"{exception}"

#Get recipe with filter settings
@app.route('/recipe/filter', methods=['POST'])
def get_recipe_with_filter():
  # get specific recipe from DB 
  return "200"

@app.route('/recipe/create', methods=['POST'])

# Return jwt token to front-end 
@app.route('/signup', methods=["POST"])
def signup():
    req = request.json
    uid = req['uid']
    custom_token = auth.create_custom_token(uid)

    return f"{custom_token}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)), debug=True)
