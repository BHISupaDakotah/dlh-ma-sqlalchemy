from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from db import *
from users import Users, user_schema, users_schema
from organizations import Organizations, organization_schema, organizations_schema
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dakotahholmes@localhost:5432/alchemy"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
ma = Marshmallow(app) 
# passing the flask app into marshmallow
# tying marshmallow to the flask app

def create_all():
  with app.app_context():
    print("creating tablers")
    db.create_all()
    print("all done")

def populate_object(obj, data_dictionary):
  fields = data_dictionary.keys()
  for field in fields:
    if getattr(obj, field):   # If the user object has the field 'field'...
        setattr(obj, field, data_dictionary[field])

# ---
@app.route('/users/get', methods=['GET'])
def get_all_active_users():
  users = db.session.query(Users).filter(Users.active == True).all()

  return jsonify(users_schema.dump(users)), 200
#--
@app.route('/user/<user_id>',methods=['GET'])
def get_user_by_id(user_id):
  
  user_result = db.session.query(Users).filter(Users.user_id == user_id).first()

  return jsonify(user_schema.dump(user_result)), 200

@app.route('/user/add', methods=['POST'])
def user_add():
  post_data = request.json
  if not post_data:
    post_data = request.form

  first_name = post_data.get('first_name')
  last_name = post_data.get('last_name')
  email = post_data.get('email')
  phone = post_data.get('phone')
  city = post_data.get('city')
  state = post_data.get('state')
  org_id = post_data.get('org_id')
  active = post_data.get('active')
# use three lines below to skip using a function 
  # new_user = Users(first_name, last_name, email, phone, city, state, org_id, active)
  # db.session.add(new_user)
  # db.session.commit()
  try:
    response = add_user(first_name, last_name, email, phone, city, state, org_id, active)
    return response
  except IntegrityError:
    return jsonify("duplicate value for unique key"), 400

def add_user(first_name, last_name, email, phone, city, state, org_id, active):
  new_user = Users(first_name, last_name, email, phone, city, state, org_id, active)
  
  db.session.add(new_user)

  db.session.commit()
  return jsonify(user_schema.dump(new_user)), 200

@app.route('/user/update/<user_id>', methods=['POST','PUT'])
def user_update(user_id):
  user = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user:
    return jsonify("sorry dude no user"), 404

  post_data = request.json
  if not post_data:
    post_data = request.form

  populate_object(user, post_data)
  db.session.commit()

  return jsonify(user_schema.dump(user)), 200
# --
@app.route('/user/activate/<user_id>', methods=['GET'])
def activate_user(user_id):
  user = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user:
    return(f"no user with {user_id}"), 418

  user.active = True
  db.session.commit()

  return jsonify(user_schema.dump(user)), 200

@app.route('/user/deactivate/<user_id>', methods=['GET'])
def deactivate_user(user_id):
  user = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user:
    return(f"no user with {user_id}"), 418

  user.active = False
  db.session.commit()

  return jsonify(user_schema.dump(user)), 200

@app.route('/user/delete/<user_id>')
def delete_user(user_id):
  user = db.session.query(Users).filter(Users.user_id == user_id).first()

  db.session.delete(user)
  db.session.commit()
  return jsonify(user_schema.dump(user)), 201
@app.route('/orgs/get', methods=['GET'])
def get_all_active_orgs():
  results = db.session.query(Organizations).filter(Organizations.active == True).all()

  if results:
    return jsonify(organizations_schema.dump(results)), 200
    # .dump() format that can be jsonified
    # pass in sqlalchemy query object into - ie .dump(results)

  else:
    return jsonify("sorry no orgs"), 404

@app.route('/org/add', methods=['POST'] )
def org_add():
    post_data = request.json
    if not post_data:
        post_data = request.form

    name = post_data.get('name')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')  
    active = post_data.get('active')

    add_org(name,phone, city, state, active)
    db.session.commit()
    return jsonify("Org created"), 201

def add_org(name, phone, city, state, active):
    new_org = Organizations(name, phone, city, state, active)
    db.session.commit()
    return jsonify(organization_schema.dump(new_org)), 200

@app.route('/org/update/<org_id>', methods=['POST', 'PUT'])
def org_update(org_id):
  organization = db.session.query(Organizations).filter(Organizations.org_id==org_id).first()

  if not organization:
    return jsonify(f"org with id {org_id} not found"), 404

  post_data = request.json
  if not post_data:
    post_data = request.form

  populate_object(organization, post_data)
  db.session.commit()

  return jsonify(organization_schema.dump(organization)), 200
  # return jsonify('Orgainiztion values updated', 200)

@app.route('/org/activate/<org_id>')
def activate_org(org_id):
  organization = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

  if not organization:
    return(f"no user with {org_id}"), 418

  organization.active = True
  db.session.commit()

  return jsonify(organization_schema.dump(organization)),200

@app.route('/org/deactivate/<org_id>')
def deactivate_org(org_id):
  organization = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

  if not organization:
    return(f"no user with {org_id}"), 418

  organization.active = False
  db.session.commit()

  return jsonify(organization_schema.dump(organization)),200

@app.route('/org/delete/<user_id>')
def delete_org(org_id):
  organization = db.session.query(Users).filter(Users.org_id == org_id).first()

  db.session.delete(organization)
  db.session.commit()
  return jsonify(organization_schema.dump(organization)),201
# ---
if __name__ == '__main__':
  create_all()
  app.run(host='0.0.0.0', port="8089")

  # brew services start postgresql@14
  # brew services restart postgresql@14

  # marshmallow takes sqlalchemy objects and put them into json for us