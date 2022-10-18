from flask import Flask, request, jsonify

from db import *
from users import Users
from organizations import Organizations

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dakotahholmes@localhost:5432/alchemy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)

def create_all():
  with app.app_context():
    print("creating tables")
    db.create_all()
    print("all done")

def populate_object(obj, data_dictionary):
  fields = data_dictionary.keys()
  for field in fields:
    if getattr(obj, field):   # If the user object has the field 'field'...
        setattr(obj, field, data_dictionary[field])

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

  add_user(first_name, last_name, email, phone, city, state, org_id, active)

  return jsonify("user created"), 201

def add_user(first_name, last_name, email, phone, city, state, org_id, active):
  new_user = Users(first_name, last_name, email, phone, city, state, org_id, active)

  db.session.add(new_user)
  db.session.commit()

@app.route('/users/get', methods=['GET'])
def get_all_active_users():
  users = db.session.query(Users).filter(Users.active == True).all()
  users_list = []

  for user in users:
    # print(user.first_name)
    new_user = {
      'user_id': user.user_id,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email,
      'phone': user.phone,
      'city': user.city,
      'state': user.state,
      # backref in the organizations.py
      'organization': {
        'org_id': user.organization.org_id,
        'name': user.organization.name,
        'phone': user.organization.phone,
        'city': user.organization.city,
        'state': user.organization.state
      },
      'active': user.active
    }

    users_list.append(new_user)
  return jsonify(users_list), 200

@app.route('/user/<user_id>',methods=['GET'])
def get_user_by_id(user_id):
  user_result = db.session.query(Users).filter(Users.user_id == user_id).first()

  if user_result:

    user = {
      'user_id' : user_result.user_id,
      'first_name': user_result.first_name,
      'last_name': user_result.last_name,
      'email': user_result.email,
      'phone': user_result.phone,
      'city': user_result.city,
      'state': user_result.state,
      'org_id': user_result.org_id,
      'active': user_result.active
    }

    return jsonify(user), 200
  else:
    return jsonify("sorry dude no user found"), 404

@app.route('/user/update/<user_id>', methods=['POST','PUT'])
def user_update(user_id):
  user = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user:
    return jsonify("sorry dude no user"), 404

  post_data = request.json
  if not post_data:
    post_data = request.form

  # if post_data.get('first_name'):
  #   user.first_name = post_data.get('first_name')
  # if post_data.get('last_name'):
  #   user.last_name = post_data.get('last_name')
  # if post_data.get('email'):
  #   user.email = post_data.get('email')
  # if post_data.get('phone'):
  #   user.phone = post_data.get('phone')
  # if post_data.get('city'):
  #   user.city = post_data.get('city')
  # if post_data.get('state'):
  #   user.state = post_data.get('state')
  # if post_data.get('org_id'):
  #   user.org_id = post_data.get('org_id')
  # if post_data.get('active'):
  #   user.active = post_data.get('active')

  populate_object(user, post_data)
  db.session.commit()

  return jsonify('user updated'), 200

@app.route('/user/activate/<user_id>')
def activate_user(user_id):
  user = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user:
    return(f"no user with {user_id}"), 418

  user.active = True
  db.session.commit()

  return jsonify('user active'),200

@app.route('/user/deactivate/<user_id>')
def deactivate_user(user_id):
  user = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user:
    return(f"no user with {user_id}"), 418

  user.active = False
  db.session.commit()

  return jsonify('user deactived'),200

# @app.route('user/delete/<user_id>')
# def delete_user(user_id):
#   user = db.session.query(Users).filter(Users.user_id == user_id).first()

#   db.session.delete(user)
#   db.session.commit()
#   return jsonify('user deleted')

# ---------------------------------------------------------------------------
@app.route('/org/add', methods=['POST'])
def org_add():
  post_data = request.json
  if not post_data:
    post_data = request.form

  name = post_data.get('name')
  phone = post_data.get('phone')
  city = post_data.get('city')
  state = post_data.get('state')
  active = post_data.get('active')

  add_org(name, phone, city, state, active)

  return jsonify("org created"), 201

def add_org(name, phone, city, state, active):
  new_org = Organizations(name, phone, city, state, active)

  db.session.add(new_org)
  db.session.commit()

@app.route('/org/<org_id>', methods=['GET'])
def get_org_by_id(org_id):
  org_result = db.session.query(Organizations).filter(Organizations.org_id==org_id).first()

  if org_result:

    org = {
      'org_id' : org_result.org_id,
      'name': org_result.name,
      'phone': org_result.phone,
      'city': org_result.city,
      'state': org_result.state,
      'active': org_result.active
    }

    return jsonify(org), 200
  else: 
    return jsonify("Sorry dude no org")

@app.route('/orgs/get', methods=['GET'])
def get_all_active_orgs():
  results = db.session.query(Organizations).filter(Organizations.active == True).all()
  org = None
  org_list = []

  for org in results:

    org = {
      'org_id': org.org_id,
      'name': org.name,
      'phone': org.phone,
      'city': org.city,
      'state': org.state,
      'active': org.active
    }

    org_list.append(org)

  if org in org_list:
    return jsonify(org_list), 200

  else:
    return jsonify("sorry no orgs"), 404

@app.route('/org/update/<org_id>', methods=['POST', 'PUT'])
def org_update(org_id):
  organization = db.session.query(Organizations).filter(Organizations.org_id==org_id).first()

  if not organization:
    return jsonify(f"org with id {org_id} not found"), 404

  post_data= request.json
  if not post_data:
    post_data = request.form

  # if post_data.get('name'):
  #   organization.name = post_data.get('name')
  # if post_data.get('phone'):
  #   organization.phone= post_data.get('phone')
  # if post_data.get('city'):
  #   organization.city = post_data.get('city')
  # if post_data.get('state'):
  #   organization.state = post_data.get('state')
  # if 'active' in post_data:
  #   organization.active = post_data.get('active')

  populate_object(organization, post_data)
  db.session.commit()

  return jsonify('Orgainiztion values updated'), 200

# @app.route('org/delete/<org_id>')
# def delete_org(org_id):
  # organization = db.session.query(Organizations).filter(Organizations.org_id == org_id)

  # db.session.delete(organization)
  # db.session.commit()
  # return jsonify('Org has been deleted')

@app.route('/org/activate/<org_id>')
def activate_org(org_id):
  organization = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

  if not organization:
    return(f"no user with {org_id}"), 418

  organization.active = True
  db.session.commit()

  return jsonify('organization active'),200

@app.route('/org/deactivate/<org_id>')
def deactivate_org(org_id):
  organization = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

  if not organization:
    return(f"no user with {org_id}"), 418

  organization.active = False
  db.session.commit()

  return jsonify('organization deactived'),200



if __name__ == '__main__':
  create_all()
  app.run(host='0.0.0.0', port="8089")

  # .first() gets single item
  # .all() gets list of items