from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Product Class/Model
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(50))
  last_name = db.Column(db.String(50))
  user_name = db.Column(db.String(50))
  email = db.Column(db.String(50))

  def __init__(self, first_name, last_name, user_name, email):
    self.first_name = first_name
    self.last_name = last_name
    self.user_name = user_name
    self.email = email


with app.app_context():
    db.create_all()

# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'first_name', 'last_name', 'user_name', 'email')

# Init Schema
user_schema = UserSchema()
users_Schema = UserSchema(many=True)

# Create a User
@app.route('/createUser', methods=['POST'])
def create_user():
  first_name = request.json['first_name']
  last_name = request.json['last_name']
  user_name = request.json['user_name']
  email = request.json['email']

  user_details = User(first_name, last_name, user_name, email)
  db.session.add(user_details)
  db.session.commit()
  return user_schema.jsonify(user_details)

# Update a User
@app.route('/updateUser/<id>', methods=['PUT'])
def update_user(id):
  user = User.query.get_or_404(id)

  if user:
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    user_name = request.json['user_name']
    email = request.json['email']

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.user_name = user_name

    db.session.commit()

  return user_schema.jsonify(user)

# Delete User by Id
@app.route('/deleteUserById/<id>', methods=['POST'])
def delete_user_by_id(id):
  user = User.query.get_or_404(id)
  if user:
    db.session.delete(user)
    db.session.commit()
  return user_schema.jsonify(user)

# Get All Users
@app.route('/findAllUsers', methods=['GET'])
def find_all_users():
  all_users = User.query.all()
  result = users_Schema.dump(all_users)
  return jsonify(result)

# Get User by Id
@app.route('/findUserById/<id>', methods=['GET'])
def find_user_by_id(id):
  user = User.query.get_or_404(id)
  return user_schema.jsonify(user)



# Run Server
if __name__ == '__main__':
  app.run(debug=True)