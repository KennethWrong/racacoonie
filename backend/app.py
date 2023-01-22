import os
import pandas as pd

from ast import literal_eval
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
# app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://app:RYfC6wsILFZtZu1b7rOjmQ@void-carp-6949.5xj.cockroachlabs.cloud:26257/ken_db?sslmode=verify-full" 
# app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://dan:EfRUhPejLHVWl_HmxrFIQA@eager-dog-6969.5xj.cockroachlabs.cloud:26257/dev?sslmode=verify-full" 
app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://root@localhost:26257/db1?sslmode=disable"
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
  description = db.Column(db.String(5000))

  minutes = db.Column(db.Integer)

  calories = db.Column(db.Float)
  total_fat = db.Column(db.Float)
  sugar = db.Column(db.Float)
  sodium = db.Column(db.Float)
  saturated_fat = db.Column(db.Float)

  n_steps = db.Column(db.Integer)
  steps = db.Column(db.String(7000))
  region = db.Column(db.String(400))


  ingredients = db.relationship('Ingredient', secondary=ingredients_table, backref='recipes', lazy=True)
  tags = db.relationship('Tag', secondary=tags_table, backref='recipes', lazy=True)
  # user_ratings = db.relationship(
  #       'User', secondary=liked_recipes, backref='user_ratings', lazy=True)

  # tags = db.relationship('tags', secondary=tags_table, backref="recipes", lazy=True)


  @staticmethod
  def get_dict(recipe_obj):
    recipe = recipe_obj.to_dict()
    recipe['users'] = [user.to_dict() for user in recipe_obj.user_ratings]
    recipe['ingredients'] = [ingred.to_dict()['name'] for ingred in recipe_obj.ingredients]
    recipe['tags'] = [tag.to_dict()['name'] for tag in recipe_obj.tags]

    return recipe
  
class User(db.Model, SerializerMixin):
  serialize_only = ('id', 'username', 'email')
  serialize_rules = ('-liked_recipes',)

  id = db.Column(db.Integer, primary_key=True, unique=True)
  username = db.Column(db.String(1000), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=True)

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

  # r1 = Recipe(id=0, name="Ibrahim's Tomato Eggs!", description="", minutes=15,
  #             calories=0.0, total_fat=0.0, sugar=0.0, sodium=0.0,
  #             saturated_fat=0.0, n_steps=5, steps=['make eggs and put tomatoes bruh'])
  
  # r2 = Recipe(id=1, name="Kenneth's Fried Rice!")
  # r3 = Recipe(id=2, name="Chicken Lo Mein!")
  # r4 = Recipe(id=3, name="Qdoba!")

  # db.session.add(r1)
  # db.session.add(r2)
  # db.session.add(r3)
  # db.session.add(r4)

  # ing1 = Ingredient(id=0, name="eggs")
  # ing2 = Ingredient(id=1, name="tomatoes")
  # db.session.add(ing1)
  # db.session.add(ing2)

  # tag1 = Tag(id=0, name="vegetarian")
  # db.session.add(tag1)

  # r1.ingredients.append(ing1)
  # r1.ingredients.append(ing2)
  # r1.tags.append(tag1)

  # u1 = User(id=0, username='cheesus', email='ibrahim@gmail.com')
  # u1.liked_recipes.append(r1)
  # db.session.add(u1)

  db.session.commit()
  return "Databse initalized successfully", 200

# initialize database with preprocessed CSVs
@app.route("/init-db/ingredients", methods=["GET"])
def init_ingredients_db():
  try:
    ingredient_csv = "./assets/ingredients.csv"
    data = pd.read_csv(ingredient_csv)

    for i, row in data.iterrows():
      record = Ingredient(id=row['id'], name=row['name'])

      db.session.add(record)
    
    db.session.commit()

  except Exception as e:
    print(e)
    
    db.session.rollback()

    return "Something went wrong", 500
  
  finally:
    db.session.close()
  
  return "Ingredient table populated successfully", 200

        
@app.route("/init-db/tags", methods=["GET"])
def init_tags_db():
  try:
    tags_csv = "./assets/tags.csv"
    data = pd.read_csv(tags_csv)

    for i, row in data.iterrows():
      record = Tag(id=row['id'], name=str(row['name']))

      db.session.add(record)
    
    db.session.commit()
  except Exception as e:
    print(e)
    
    db.session.rollback()

    return "Something went wrong", 500
  
  finally:
    db.session.close()
  
  return "Tag table populated successfully", 200

  

@app.route("/init-db/recipes", methods=["GET"])
def init_recipes_db():
  try:
    recipes_csv = "./assets/recipes.csv"
    data = pd.read_csv(recipes_csv)

    for i, row in data.iterrows():
      ingredients = literal_eval(row['ingredients'])
      tags = literal_eval(row['tags'])
      recipe = Recipe(
        id=row['id'],
        name=str(row['name']),
        description=str(row['description']),
        minutes=int(row['minutes']),
        n_steps=int(row['n_steps']),
        steps=str(row['steps']),
        region=str(row['region'])
      )
      db.session.add(recipe)

      for ingredient_id in ingredients:
        ing_obj = Ingredient.query.get(ingredient_id)
        recipe.ingredients.append(ing_obj)

      for tag_id in tags:
        tag_obj = Tag.query.get(tag_id)
        recipe.tags.append(tag_obj)



    
    db.session.commit()
  except Exception as e:
    print(e)
    db.session.rollback()

    return "Something went wrong", 500
  
  
  finally:
    db.session.close()
  
  return "Recipe table populated successfully", 200

  

@app.route("/init-db/users", methods=["GET"])
def init_users_db():
  try:
    interaction_csv = "./assets/interactions.csv"
    data = pd.read_csv(interaction_csv)
    user_ids = data['user_id'].unique()

    for user_id in user_ids:
      liked_recipes = data[data['user_id'] == user_id]['recipe_id']
      user = User(id=int(user_id), username=f"user_{user_id}", email=f"user_{user_id}@email.com")
      db.session.add(user)

      for recipe_id in liked_recipes:
        recipe_obj = Recipe.query.get(int(recipe_id))
        user.liked_recipes.append(recipe_obj)
          
    db.session.commit()

  except Exception as e:
    print(e)
    db.session.rollback()

    return "Something went wrong", 500
  
  
  finally:
    db.session.close()
  
  return "Users table populated successfully", 200


# Get all recipes from database

@app.route("/user/all", methods=['GET'])
def getAllUsers():
  try:
    users = User.query.all()
    users_dicts = [User.get_dict(x) for x in users]

    return jsonify({"users": users_dicts}), 200

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
  
@app.route("/ingredient/all", methods=['GET'])
def getAllIngredients():
  try:
    ingredients = [ingred.to_dict()['name'] for ingred in Ingredient.query.all()]
  
    return jsonify({"recipes": ingredients}), 200

  except Exception as exception:
    return f"{exception}", 500
  
@app.route("/tag/all", methods=['GET'])
def getAllTags():
  try:
    tags = [tag.to_dict()['name'] for tag in Tag.query.all()]
  
    return jsonify({"recipes": tags}), 200

  except Exception as exception:
    return f"{exception}", 500

#Get recipe with filter settings
@app.route('/recipe/filter', methods=['POST'])
def get_recipe_with_filter():
  # get specific recipe from DB 
  return "200"

# @app.route('/recipe/create', methods=['POST'])

# Return jwt token to front-end 
@app.route('/signup', methods=["POST"])
def signup():
    req = request.json
    uid = req['uid']
    custom_token = auth.create_custom_token(uid)

    return f"{custom_token}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)), debug=True)
