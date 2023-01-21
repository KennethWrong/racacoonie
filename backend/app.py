import os

from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)

# THIS IS ONLINE
# app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://app:RYfC6wsILFZtZu1b7rOjmQ@void-carp-6949.5xj.cockroachlabs.cloud:26257/db1?sslmode=verify-full" 

app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://root@localhost:26257/db1?sslmode=disable"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

CORS(app)

### Models ###
class Recipe(db.Model, SerializerMixin):
  serialize_only = ('id', 'name')
  # serialize_rules = ('-employees', '-job_postings') # exluded from serialization.


  id = db.Column(db.Integer, primary_key=True, unique=True)
  name = db.Column(db.String(300), nullable=False)


@app.route("/init-db", methods=['POST', 'GET'])
def init_db():
  db.drop_all()
  db.create_all()

  r1 = Recipe(id=0, name="Ibrahim's Tomato Eggs!")
  db.session.add(r1)

  db.session.commit()
  return "Databse initalized successfully", 200

@app.route("/recipe/all", methods=['GET'])
def getAllRecipes():
  try:
    recipes = Recipe.query.all()
    recipes_dict = [c.to_dict() for c in recipes]

    return jsonify({"recipes": recipes_dict}), 200

  except Exception as exception:
    return f"{exception}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
