import os
import pandas as pd
import numpy as np

from ast import literal_eval
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import create_engine
from firebase_admin import auth, initialize_app, credentials
from sqlalchemy import func
from utils import cosine_similarity
from utils import cosine_similarity_to_all_other_user

app = Flask(__name__)

# Credentials for firebase
cred = credentials.Certificate("./assets/secret.json")
default_app = initialize_app(cred)

# THIS IS ONLINE
# app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://app:RYfC6wsILFZtZu1b7rOjmQ@void-carp-6949.5xj.cockroachlabs.cloud:26257/ken_db?sslmode=verify-full" 
app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://root@localhost:26257/defaultdb?sslmode=disable"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

CORS(app)
db = SQLAlchemy(app)


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
                    'n_steps', 'steps', 'region')
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
    recipe['ingredients'] = [ingred.to_dict() for ingred in recipe_obj.ingredients]
    recipe['tags'] = [tag.to_dict() for tag in recipe_obj.tags]

    return recipe
  
class User(db.Model, SerializerMixin):
  serialize_only = ('id', 'username', 'email')
  serialize_rules = ('-liked_recipes',)

  id = db.Column(db.String(100), primary_key=True, unique=True)
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

  r1 = Recipe(id=0, name="Ibrahim's Tomato Eggs!", description="This recipe is very delicious and it comes from a lot of generations to come", minutes=15,
              calories=420.0, total_fat=65.0, sugar=20.0, sodium=690.0,
              saturated_fat=20, n_steps=4, steps=['First stir the eggs up', 'Cut up the tomatoes', 'Stir fry the tomato and the eggs', 'Season and enjoy'],
              region="cn",
              )
  
  r2 = Recipe(id=1, name="Ground Beef Stroganoff Noodles", description="These ground beef stroganoff noodles are a shortcut version of classic beef stroganoff in a one-pan version. The ultimate comfort food with flavorful ground beef, mushrooms, and egg noodles."
            , minutes=40,
              calories=700.0, total_fat=77.0, sugar=10.0, sodium=700.0,
              saturated_fat=10, n_steps=4, 
              steps=['Melt butter and oil in a skillet over medium-high heat. ', 
                      'Stir in minced garlic and flour, and cook for 1 minute.',
                      'Reduce heat to medium, and mix in noodles. Cover with a tight-fitting lid and simmer for 5 minutes.',
                      'Once noodles are cooked, reduce heat to low, and stir in sour cream. Serve immediately with additional sour cream and green onions or chives if so desired.',
                      ],
              region="us",
              )

  r3 = Recipe(id=2, name="One Pot Tortellini Bake", description="This main dish comes together in under an hour and the best part, it cooks in one pot. Serve with crusty garlic bread and a nice green salad if desired.", 
              minutes=40,
              calories=783.0, total_fat=46.0, sugar=33.0, sodium=69.0,
              saturated_fat=55, n_steps=5, 
              steps=['Heat a Dutch oven over medium-high heat. Add ground beef and cook until brown and crumbly, 5 to 10 minutes. Add Italian seasoning, salt, and granulated garlic; mix to combine.', 
              'Stir in marinara sauce, diced tomatoes with liquid, water, and red wine until well combined. Reduce heat to low; add tortellini and cook until warmed through, about 10 to 15 minutes.',
              'Meanwhile, preheat the oven to 375 degrees F (190 degrees C).',
              'Add cream cheese to tortellini mixture and stir gently to blend; sprinkle mozzarella cheese over the surface.',
              'Bake in the preheated oven until cheese is melted and golden brown, about 15 minutes. Serve immediately.'
              ],
              region="it",
              )

  r4 = Recipe(id=3, name="Chicken Fajita Rice Casserole", description="This rice and chicken casserole is very easy to pull together and has a lot of flavor. Don't skip toasting the rice - it is an incredibly easy way to add just a hint of nuttiness and more depth of flavor. Top with shredded Cheddar cheese, sour cream, chopped tomatoes, or whatever topping you prefer.", 
  minutes=55,
              calories=256.0, total_fat=5.0, sugar=30.0, sodium=690.0,
              saturated_fat=23.3, n_steps=5, 
              steps=['Preheat the oven to 350 degrees F (175 degrees C).', 
              'Add uncooked rice to a dry saucepan over medium; cook, stirring constantly, until rice is fragrant and no longer translucent, 3 to 4 minutes. Transfer to an ungreased 13- x 9-inch baking dish and stir in cilantro, lime zest, and lime juice; mix until combined.',
              'Place chicken, bell peppers, onion, fajita seasoning, olive oil, salt, and pepper in a large bowl and toss until chicken and vegetables are evenly coated. Transfer to baking dish and place in an even layer over rice mixture. Pour in chicken broth and cover with aluminum foil.',
              'Bake in preheated oven until chicken is cooked through and rice is tender, about 45 to 50 minutes.',
              'Remove from oven, uncover, and top with desired toppings. Serve with lime wedges.'
              ],
              region="mx",
              )
  
  r5 = Recipe(id=4, name="Slow Cooker Butter Chicken", description="Butter chicken is one of my favorite Indian dishes. It's easy to prep for the slow cooker in the morning to come home to the wonderful aroma of warm Indian spices... I love it! Serve with basmati rice and warm naan bread.", 
  minutes=180,
              calories=480.0, total_fat=33.0, sugar=17.0, sodium=31.0,
              saturated_fat=90.3, n_steps=5, 
              steps=['Preheat the oven to 350 degrees F (175 degrees C).', 
              'Add uncooked rice to a dry saucepan over medium; cook, stirring constantly, until rice is fragrant and no longer translucent, 3 to 4 minutes. Transfer to an ungreased 13- x 9-inch baking dish and stir in cilantro, lime zest, and lime juice; mix until combined.',
              'Place chicken, bell peppers, onion, fajita seasoning, olive oil, salt, and pepper in a large bowl and toss until chicken and vegetables are evenly coated. Transfer to baking dish and place in an even layer over rice mixture. Pour in chicken broth and cover with aluminum foil.',
              'Bake in preheated oven until chicken is cooked through and rice is tender, about 45 to 50 minutes.',
              'Remove from oven, uncover, and top with desired toppings. Serve with lime wedges.'
              ],
              region="ind",
              )
  
  r6 = Recipe(id=5, name="Saucy Sriracha Franks", description="iA little heat, a little sweet, and a little Asian. Serve with toothpicks, and you have a one-bite appetizer that is so very simple to make.", 
  minutes=20,
              calories=480.0, total_fat=33.0, sugar=17.0, sodium=31.0,
              saturated_fat=90.3, n_steps=1, 
              steps=['Mix ketchup, soy sauce, vinegar, sriracha, brown sugar, sesame oil, ginger, and garlic in a saucepan and bring to a simmer over low heat. Add franks and heat until warm, about 5 minutes. Serve with toothpicks.'
              ],
              region="ger",
              )
  
  r7 = Recipe(id=6, name="Traditional Sauerbraten", description="For this sauerbraten, I found two slightly different handwritten versions of my Grandmother's recipe. Born in Nekkar am Rhein in 1904", 
  minutes=20,
              calories=480.0, total_fat=33.0, sugar=17.0, sodium=31.0,
              saturated_fat=90.3, n_steps=1, 
              steps=['Mix ketchup, soy sauce, vinegar, sriracha, brown sugar, sesame oil, ginger, and garlic in a saucepan and bring to a simmer over low heat. Add franks and heat until warm, about 5 minutes. Serve with toothpicks.'
              ],
              region="ger",
              )

  r8 = Recipe(id=7, name="Chicken Katsu", description="Chicken katsu is Japanese-style fried chicken. This is my family recipe and can also be used to make tonkatsu by using pork cutlets instead of chicken. Serve with white rice and tonkatsu sauce.", 
  minutes=20,
              calories=480.0, total_fat=33.0, sugar=17.0, sodium=31.0,
              saturated_fat=90.3, n_steps=1, 
              steps=[
                'Season chicken breasts on both sides with salt and pepper. Place flour, beaten egg, and panko crumbs into separate shallow dishes. Coat chicken breasts in flour, shaking off any excess; dip into egg, and then press into panko crumbs until well coated on both sides.',
                'Heat oil in a large skillet over medium-high heat. Place chicken in the hot oil, and fry until golden brown, 3 or 4 minutes per side. Transfer to a paper towel-lined plate to drain.'

              ],
              region="jp",
              )

  r9 = Recipe(id=8, name="Russian Pelmeni", description="Pelmeni are traditional Russian meat-filled dumplings. Making pelmeni is favorite family pastime in the long winter months. These dumplings are a common convenience food - big batches can be frozen and quickly boiled or fried on demand.", 
  minutes=180,
              calories=480.0, total_fat=33.0, sugar=17.0, sodium=31.0,
              saturated_fat=90.3, n_steps=1, 
              steps=[
                'Season chicken breasts on both sides with salt and pepper. Place flour, beaten egg, and panko crumbs into separate shallow dishes. Coat chicken breasts in flour, shaking off any excess; dip into egg, and then press into panko crumbs until well coated on both sides.',
                'Heat oil in a large skillet over medium-high heat. Place chicken in the hot oil, and fry until golden brown, 3 or 4 minutes per side. Transfer to a paper towel-lined plate to drain.'

              ],
              region="ru",
              )

  r10 = Recipe(id=9, name="Al Kabsa", description="Al kabsa was the first Arabic dish I ever made. It turned out extremely delicious and is a new favorite. Serve with fresh mixed cucumber, carrot, lettuce, and tomato salad ??? preferably with a little lime vinaigrette. ", 
  minutes=180,
              calories=480.0, total_fat=33.0, sugar=17.0, sodium=31.0,
              saturated_fat=90.3, n_steps=1, 
              steps=[
                'Season chicken breasts on both sides with salt and pepper. Place flour, beaten egg, and panko crumbs into separate shallow dishes. Coat chicken breasts in flour, shaking off any excess; dip into egg, and then press into panko crumbs until well coated on both sides.',
                'Heat oil in a large skillet over medium-high heat. Place chicken in the hot oil, and fry until golden brown, 3 or 4 minutes per side. Transfer to a paper towel-lined plate to drain.'

              ],
              region="sa",
              )

  db.session.add(r1)
  db.session.add(r2)
  db.session.add(r3)
  db.session.add(r4)
  db.session.add(r5)
  db.session.add(r6)
  db.session.add(r7)
  db.session.add(r8)
  db.session.add(r9)
  db.session.add(r10)

  eggs = Ingredient(id=0, name="eggs")
  tomato = Ingredient(id=1, name="tomato")
  tortellini = Ingredient(id=2, name="tortellini")
  beef = Ingredient(id=3, name="beef")
  pasta = Ingredient(id=4, name="pasta")
  tortilla = Ingredient(id=5, name="tortilla")
  chicken = Ingredient(id=6, name="chicken")
  rice = Ingredient(id=7, name="rice")
  butter = Ingredient(id=8, name="butter")
  sausage = Ingredient(id=9, name="sausage")
  flour = Ingredient(id=10, name="flour")
  noodle = Ingredient(id=11, name="noodle")

  db.session.add(eggs)
  db.session.add(tomato)
  db.session.add(tortellini)
  db.session.add(beef)
  db.session.add(pasta)
  db.session.add(tortilla)
  db.session.add(chicken)
  db.session.add(rice)
  db.session.add(butter)
  db.session.add(sausage)
  db.session.add(flour)
  db.session.add(noodle)

  tag1 = Tag(id=0, name="vegetarian")
  db.session.add(tag1)

  r1.ingredients.append(tomato)
  r1.ingredients.append(eggs)
  r2.ingredients.append(beef)
  r2.ingredients.append(noodle)

  r3.ingredients.append(tortellini)
  r3.ingredients.append(tomato)
  r3.ingredients.append(butter)
  r3.ingredients.append(eggs)

  r4.ingredients.append(chicken)
  r4.ingredients.append(rice)
  r4.ingredients.append(butter)
  r4.ingredients.append(flour)

  r5.ingredients.append(chicken)
  r5.ingredients.append(butter)
  r5.ingredients.append(rice)

  r6.ingredients.append(sausage)
  r7.ingredients.append(sausage)

  r8.ingredients.append(chicken)
  r8.ingredients.append(flour)
  r8.ingredients.append(rice)

  r9.ingredients.append(beef)
  r9.ingredients.append(butter)
  r9.ingredients.append(flour)

  r10.ingredients.append(beef)
  r10.ingredients.append(butter)
  r10.ingredients.append(flour)
  r10.ingredients.append(rice)

  r2.tags.append(tag1)

  u1 = User(id=0, username='cheesus', email='ibrahim@gmail.com')
  u2 = User(id=1, username='kenneth', email='Kenneth@gmail.com')

  u1.liked_recipes.append(r1)
  u2.liked_recipes.append(r3)
  u2.liked_recipes.append(r4)
  db.session.add(u1)

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
      nutrition = literal_eval(row['nutrition'])
      recipe = Recipe(
        id=row['id'],
        name=str(row['name']),
        description=str(row['description']),
        minutes=int(row['minutes']),
        calories=float(nutrition[0]),
        total_fat=float(nutrition[1]),
        sugar=float(nutrition[2]),
        sodium=float(nutrition[3]), 
        saturated_fat=float(nutrition[4]),
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
    recipes = recipes.filter(Recipe.minutes < minutes)
  
  if search_phrase and search_phrase != "":
    recipes = recipes.filter(func.lower(Recipe.name).contains(search_phrase.lower()))
  
  if tags and len(tags) != 0:
    for t in tags:
      check_tag = Tag(id=t['id'], name=t['name'])
      recipes = recipes.filter(Recipe.tags.contains(check_tag))
  
  if ingredients and len(ingredients) != 0:
    for i in ingredients:
      ing = Ingredient(id=i['id'], name=i['name'])
      recipes = recipes.filter(Recipe.ingredients.contains(ing))
  
  if recipes:
    recipe_list = [r.to_dict() for r in recipes]
    print(recipe_list)
    return {"recipes": recipe_list}, 200


  return "", 404

@app.route('/recipe/create', methods=['POST'])
def create_recipe():
  # Write to database with user recipe
  return "200"

@app.route('/recommend/users/<int:user_id>', methods=['GET'])
def recommend_other_users(user_id):
  try:
    user_recipe_matrix = []
    num_recipes = db.session.query(Recipe).count()
    users = User.query.all()

    for user in users:
      user_vector = np.zeros(num_recipes)
      for recipe in user.liked_recipes:
        user_vector[recipe.id] = 1
      
      user_recipe_matrix.append(user_vector)
    
    user_recipe_matrix = np.array(user_recipe_matrix) 
    user_similarity = cosine_similarity_to_all_other_user(user_id, user_recipe_matrix)
    top_5_similar_users_dict = dict(sorted(user_similarity.items(), key=lambda item:-item[1])[:5])    

    top_5_similar_users = User.query.filter(User.id.in_(top_5_similar_users_dict.keys())).all()
    recommendations = []
    for user in top_5_similar_users:
      recipes = user.liked_recipes[:2]
      recipes = [recipe.to_dict() for recipe in recipes]
      entry = {'user_id': user.id, 'recipes': recipes, 'similarity': top_5_similar_users_dict[user.id]}
      recommendations.append(entry)


    return jsonify({'recommendations': recommendations}), 200

  
  except Exception as e:
    print(e)
    return 'Something went wrong', 500
  
  return 'Does not exist', 404




# @app.route('/recipe/create', methods=['POST'])

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

@app.route('/user/liked', methods=["GET"])
def get_user_liked():
  uid = request.headers['authorization']
  user = User.query.filter_by(id=uid).first()
  if not user:
    print('Not found')
    return "User not found", 404
  user_dic = user.to_dict()
  # print(user_dic)
  liked_recipes = [recipe.to_dict() for recipe in user.liked_recipes]
  print(liked_recipes)
  return jsonify(liked_recipes), 200



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
  print(user.to_dict())
  return user

def get_recipe_by_id_helper(rid):
  recipe = Recipe.query.filter_by(id=rid).first()
  return recipe

def parse_step_to_list(steps):
  if not steps or steps == "":
    return steps
  
  steps = steps[1:-1].split(",")
  steps = [s[1:-1] for s in steps]
  return steps

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)), debug=True)
