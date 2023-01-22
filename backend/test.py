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
# app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://app:RYfC6wsILFZtZu1b7rOjmQ@void-carp-6949.5xj.cockroachlabs.cloud:26257/ken_db?sslmode=verify-full" 
app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://kenneth:oR5IsoHrDJksC2cecDf0Cg@low-gosling-6971.5xj.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"
# app.config["SQLALCHEMY_DATABASE_URI"]= "cockroachdb://root@localhost:26257/db1?sslmode=disable"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route('/')
def lmao():
    return "lmao"

if __name__ == "__main__":
    app.run(port=8000)
