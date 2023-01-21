# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, jsonify
from flask_cors import CORS  # comment this on deployment
from firebase_admin import auth, initialize_app, credentials
 
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("./assets/secret.json")
default_app = initialize_app(cred)

 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

@app.route('/signup', methods=["POST"])
def signup():
    print(request.headers)
    req = request.json
    uid = req['uid']
    custom_token = auth.create_custom_token(uid)

    return f"{custom_token}"
 
# main driver function
if __name__ == '__main__':
    app.run(port=8000, debug=True)