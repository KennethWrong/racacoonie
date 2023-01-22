import os

from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from firebase_admin import auth, initialize_app, credentials
from sqlalchemy import func

app = Flask(__name__)

# Credentials for firebase
cred = credentials.Certificate("./assets/secret.json")
default_app = initialize_app(cred)

# THIS IS ONLINE
app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://app:RYfC6wsILFZtZu1b7rOjmQ@void-carp-6949.5xj.cockroachlabs.cloud:26257/ken_db?sslmode=verify-full" 
# app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://root@localhost:26257/db1?sslmode=disable"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

CORS(app)

### Tabels ###
liked_recipes_table = db.Table('LikedRecipes',
                            db.Column('recipe_id', db.Integer, db.ForeignKey(
                                'recipe.id'), primary_key=True),
                            db.Column('user_id', db.String(100), db.ForeignKey(
                                'user.id'), primary_key=True)
                            )

ingredients_table = db.Table('RecipeIngredients',
                            db.Column('recipe_id', db.Integer, db.ForeignKey(
                                'recipe.id'), primary_key=True),
                            db.Column('ingredient_id', db.Integer, db.ForeignKey(
                                'ingredient.id'), primary_key=True)
                            )

tags_table = db.Table('RecipeTags',
                            db.Column('recipe_id', db.Integer, db.ForeignKey(
                                'recipe.id'), primary_key=True),
                            db.Column('tag_id', db.Integer, db.ForeignKey(
                                'tag.id'), primary_key=True)
                            )

### Models ###
class Recipe(db.Model, SerializerMixin):
  serialize_only = ('id', 'name', 'description', 'minutes',
                    'calories', 'total_fat', 'sugar', 'sodium', 'saturated_fat',
                    'n_steps', 'steps')
  # serialize_rules = ('-ingredients', '-tags') # exluded from serialization.

  id = db.Column(db.Integer, primary_key=True, unique=True)

  name = db.Column(db.String(1000), nullable=False)
  description = db.Column(db.String(4000))

  minutes = db.Column(db.Integer)

  calories = db.Column(db.Float)
  total_fat = db.Column(db.Float)
  sugar = db.Column(db.Float)
  sodium = db.Column(db.Float)
  saturated_fat = db.Column(db.Float)

  n_steps = db.Column(db.Integer)
  steps = db.Column(db.String(4000))


  ingredients = db.relationship('Ingredient', secondary=ingredients_table, backref='recipes', lazy=True)
  tags = db.relationship('Tag', secondary=tags_table, backref='recipes', lazy=True)
  # user_ratings = db.relationship(
  #       'User', secondary=liked_recipes, backref='user_ratings', lazy=True)

  # tags = db.relationship('tags', secondary=tags_table, backref="recipes", lazy=True)


  @staticmethod
  def get_dict(recipe_obj):
    recipe = recipe_obj.to_dict()
    recipe['users'] = [user.to_dict() for user in recipe_obj.user_ratings]
    recipe['ingredients'] = [ingred.to_dict() for ingred in recipe_obj.ingredients]
    recipe['tags'] = [tag.to_dict() for tag in recipe_obj.tags]

    return recipe
  
class User(db.Model, SerializerMixin):
  serialize_only = ('id', 'username', 'email')
  serialize_rules = ('-liked_recipes',)

  id = db.Column(db.String(100), primary_key=True, unique=True)
  username = db.Column(db.String(1000), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)

  liked_recipes = db.relationship('Recipe', secondary=liked_recipes_table, backref="user_ratings", lazy=True)

  @staticmethod
  def get_dict(user_obj):
    user = user_obj.to_dict()
    user['liked_recipes'] = [recipe.to_dict() for recipe in user_obj.liked_recipes]

    return user

class Ingredient(db.Model, SerializerMixin):
  serialize_only = ('id', 'name')
  serialize_rules = ('-recipes',) 

  id = db.Column(db.Integer, primary_key=True, unique=True)
  name = db.Column(db.String(100), nullable=False)


class Tag(db.Model, SerializerMixin):
  serialize_only = ('id', 'name')
  serialize_rules = ('-recipes',) 
  
  id = db.Column(db.Integer, primary_key=True, unique=True)
  name = db.Column(db.String(100), nullable=False)

@app.route("/init-db", methods=['POST', 'GET'])
def init_db():
  db.drop_all()
  db.create_all()

  r1 = Recipe(id=0, name="Ibrahim's Tomato Eggs!", description="Ibrahim has some big ass eggs, his eggs are tasty and full of tasty egg juices.", minutes=15,
              calories=42069.0, total_fat=69.0, sugar=420.0, sodium=69.0,
              saturated_fat=96.024, n_steps=5, steps=['make eggs and put tomatoes bruh', 'Ask Barry Wood to come over'])
  
  r2 = Recipe(id=1, name="Kenneth's Fried Rice!")
  r3 = Recipe(id=2, name="Chicken Lo Mein!")
  r4 = Recipe(id=3, name="Qdoba!")

  db.session.add(r1)
  db.session.add(r2)
  db.session.add(r3)
  db.session.add(r4)

  ing1 = Ingredient(id=0, name="eggs")
  ing2 = Ingredient(id=1, name="tomatoes")
  db.session.add(ing1)
  db.session.add(ing2)

  tag1 = Tag(id=0, name="vegetarian")
  db.session.add(tag1)

  r1.ingredients.append(ing1)
  r1.ingredients.append(ing2)
  r1.tags.append(tag1)

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
    users_dicts = [User.get_dict(x) for x in users]

    return jsonify({"users": users_dicts}), 200

  except Exception as exception:
    return f"{exception}"

@app.route("/user/<string:id>", methods=['GET'])
def get_user_by_id(id):
  try:
    user = User.query.filter_by(id = id).first()

    if not user:
      return {'message':'user not found'}, 404
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
      recipe_dic['ingredients'] = [i.to_dict() for i in recipe.ingredients]
      print(recipe_dic)
      recipe_dic['steps'] = parse_step_to_list(recipe_dic['steps'])
      return jsonify({'recipe': recipe_dic}), 200
    else:
      return jsonify({'recipe': None}), 404
  except Exception as exception:
    return f"{exception}"
  
@app.route("/ingredient/all", methods=['GET'])
def getAllIngredients():
  try:
    ingredients = [ingred.to_dict() for ingred in Ingredient.query.all()]
  
    return jsonify({"ingredients": ingredients}), 200

  except Exception as exception:
    return f"{exception}", 500
  
@app.route("/tag/all", methods=['GET'])
def getAllTags():
  try:
    tags = [tag.to_dict() for tag in Tag.query.all()]
  
    return jsonify({"tags": tags}), 200

  except Exception as exception:
    return f"{exception}", 500

#Get recipe with filter settings
@app.route('/recipe/filter', methods=['POST'])
def get_recipe_with_filter():
  req = request.json
  print(req)
  minutes = req["minutes"]
  tags = req["tags"]
  search_phrase = req["search"]
  ingredients = req["ingredients"]

  recipes = Recipe.query.filter_by()

  if minutes:
    recipes = recipes.filter(Recipe.minutes <  minutes)
  
  if search_phrase and search_phrase != "":
    recipes = recipes.filter(func.lower(Recipe.name).contains(search_phrase.lower()))
  
  if  tags and len(tags) != 0:
    for t in tags:
      recipes = recipes.filter(func.lower(Recipe.tags).contains(t.lower()))
  
  if ingredients and len(ingredients) != 0:
    for i in ingredients:
      recipes = recipes.filter(Recipe.ingredients.contains(i.lower()))
  
  recipe_list = [r.to_dict() for r in recipes]
  
  print(recipe_list)

  return jsonify(recipe_list)

@app.route('/recipe/create', methods=['POST'])
def create_recipe():
  # Write to database with user recipe
  return "200"

# Return jwt token to front-end 
@app.route('/signup', methods=["POST"])
def signup():
    req = request.json
    uid = req['uid']
    name = req['name']
    email = req['email']
    custom_token = uid
    user = User.query.filter_by(id = uid).first()

    if not user:
      new_user = User(id=uid, username=name, email=email)
      db.session.add(new_user)
      db.session.commit()

    return f"{custom_token}"

# Create a post request with
# header['authorization'] = racacoonie-auth-token
# {'rid': recipe_id}
@app.route('/recipe/like', methods=["POST"])
def like_recipe():
  req = request.json
  rid = req['rid']
  uid = request.headers['authorization']
  user = get_user_by_id_helper(uid)

  recipe = get_recipe_by_id_helper(rid)

  if not recipe:
    return "recipe not found", 404

  user.liked_recipes.append(recipe)
  user_dict = user.to_dict()
  db.session.commit()
  return jsonify(user_dict), 200


# Create a post request with
# header['authorization'] = racacoonie-auth-token
# {'rid': recipe_id}
@app.route('/recipe/unlike', methods=["POST"])
def unlike_recipe():
  req = request.json
  rid = req['rid']
  uid = request.headers['authorization']
  user = get_user_by_id_helper(uid)

  recipe = get_recipe_by_id_helper(rid)

  if not recipe:
    return "recipe not found", 404

  user.liked_recipes.remove(recipe)
  user_dict = user.to_dict()
  db.session.commit()
  return jsonify(user_dict), 200

def get_user_by_id_helper(uid):
  user = User.query.filter_by(id=uid).first()
  return user

def get_recipe_by_id_helper(rid):
  recipe = Recipe.query.filter_by(id=rid).first()
  return recipe

def parse_step_to_list(steps):
  if steps == "":
    return steps
  
  steps = steps[1:-1].split(",")
  return steps

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)), debug=True)
