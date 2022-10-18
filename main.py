# from pprint import pprint
# import psycopg2
# from flask import Flask, request, jsonify

# # pipenv install psycopg2

# from db import *
# from users import Users
# from organizations import Organizations

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dakotahholmes@localhost:5432/alchemy"
# # conn = psycopg2.connect("dbname='usermgt' user='dakotahholmes' host='localhost'")

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init_db(app,db)


# def create_all():
#   with app.app_context():
#       print("creating tables")
#       db.create_all()
#       print("done")

# # # ************************** Add [x] *****************************

# def add_user(first_name, last_name, email, phone, city, state, org_id, active):
#   new_user = Users(first_name, last_name, email, phone, city, state, org_id, active)

#   db.session.add(new_user)

#   db.session.commit()

# @app.route('/user/add', methods=['POST']) # ^function has to be above decorator call
# def user_add():
#     post_data = request.form 
#     if not request.form: 
#         post_data = request.json

#     first_name = post_data.get('first_name')
#     last_name = post_data.get('last_name')
#     email = post_data.get('email')
#     phone = post_data.get('phone')
#     city = post_data.get('city')
#     state = post_data.get('state')
#     org_id = post_data.get('org_id')
#     active = post_data.get('active')

#     add_user(first_name, last_name, email, phone, city, state, org_id, active)
    
#     return jsonify("User created"), 201

# # #********************* Get user by ID [x] ***************************

# # @app.route('/user/<user_id>', methods=['GET']) # add decorator to normal funtion(<user_id>)
# # def get_user_by_id(user_id): #matches paramater
# #   cursor.execute(f"""
# #     SELECT u.user_id,
# #      u.first_name, 
# #      u.last_name, 
# #      u.email, 
# #      u.phone, 
# #      u.city, 
# #      u.state, 
# #      u.org_id, 
# #      u.active,
# #       o.org_id, 
# #       o.name,
# #       o.phone,
# #       o.city, 
# #       o.state, 
# #       o.active as active_org
# #     FROM Users u
# #     JOIN Organizations o
# #     ON u.org_id=o.org_id
# #        WHERE user_id=%s;""",
# #       [user_id])

# #   results = cursor.fetchone()

# #   if results:
# #     user = {
# #       'user_id':results[0],
# #       'first_name':results[1],
# #       'last_name':results[2],
# #        'email':results[3],
# #       'phone':results[4], 
# #       'city':results[5], 
# #       'state':results[6], 
# #       'org_id':results[7],
# #       'organization' : {
# #         'org_id': results[9],
# #         'name' : results[10],
# #         'phone' : results[11],
# #         'city' : results[12],
# #         'state' : results[12],
# #         'active_org': results[13]
# #       },
# #       'active':results[8]
# #     }
# #     return jsonify(user), 200 # jsonify response and status code
# #   else:
# #     return jsonify('user not found'), 418 # jsonify response and status code

# # # *********************** Activate User [x] ***********************

# # @app.route('/user/activate/<user_id>')
# # def activate_user(user_id):
# #     cursor.execute(f"""
# #         UPDATE Users
# #             SET active=1
# #             WHERE user_id=%s;""",
# #         [user_id])
    
# #     conn.commit()

# #     return jsonify("User activated"), 200

# # # ********************* Delete User [x] *************************

# # @app.route('/user/delete/<user_id>')
# # def delete_user(user_id):
# #   cursor.execute(f"""
# #       DELETE FROM Users
# #       WHERE user_id=%s;""", [user_id])

# #   # conn.commit()

# #   return jsonify("User permently deleted!")


# # # ********************* Deactivate User [x] *************************

# # @app.route('/user/deactivate/<user_id>')
# # def deactivate_user(user_id):
# #   cursor.execute(f"""
# #   UPDATE Users
# #     SET active=0
# #     WHERE user_id=%s;""", [user_id])
  
# #   conn.commit()

# #   return jsonify("User Deactivated")

# # # get all users
# @app.route('/users/get')
# def get_all_active_users():
#   new_user = db.session.query(Users).filter(Users.active == True).all()
#   users_list = []

#   for user in new_user:
#     # print(user.first_name)
#   # list_of_users = cursor.fetchall()
#   # if list_of_users:
#   #   user_list = []
#   #   for single_user in list_of_users:
#       user = {
#         'user_id':user.user_id,
#         'first_name':user.first_name,
#         'last_name':single_user[2],
#         'email':single_user[3],
#         'phone':single_user[4], 
#         'city':single_user[5], 
#         'state':single_user[6], 
#         'org_id': {
#           'org_id' : user.organization.org_id,
#           'name' : user.organization.name,
#           'phone' : user.organization.phone,
#           'city' : user.organization.city,
#           'state' : user.organization.state,
#           'active' : user.organization.active
#         },
#         'active':single_user[8]
#     }
#       user_list.append(new_user)
#       user = {}
#     return  jsonify(user_list),200 #user_list
#   else: 
#     return jsonify('sorry'),404 #None

# # #  no commit needed because its only querying

# # # **************************** Update [x] ****************************

# # @app.route('/user/update/<user_id>', methods=(['POST','PUT']))
# # def user_update(user_id):
# #   update_fields = []
# #   update_values = []
# #   field_names = ['first_name','last_name','email','phone','city','state','org_id','active']
  
# #   post_data = request.form
# #   if not post_data:
# #     post_data = request.json

# #   for field in field_names:
# #     field_value = post_data.get(field)
# #     if field_value:
# #       update_fields.append(str(field) + f'=%s')
# #       update_values.append(field_value)

# #   if update_fields:
# #     update_values.append(user_id)
# #     query_string = "UPDATE Users SET " + ', '.join(update_fields) + " WHERE user_id=%s"
# #     cursor.execute(query_string, update_values)

# #     conn.commit()

# #     return jsonify(("updated user settings")), 200
# #   else:
# #     return jsonify('no values sent in body'), 418

# # # - Add Org [x]
# # # - Update Org [x]
# # # - Get Org by ID [x]
# # # - Get all orgs [x]
# # # - Delete org [x]
# # # - Activate org [x]
# # # - Deactivate org [x]

# #       # CREATE TABLE IF NOT EXISTS Organizations (
# #       #    org_id SERIAL PRIMARY KEY,
# #       #    name VARCHAR NOT NULL,
# #       #    phone VARCHAR,
# #       #    city VARCHAR,
# #       #    state VARCHAR,
# #       #    active smallint
# #       # );


# # - Add Org
# def add_org(name ,phone, city, state, active):
#   new_org = Organizations(name ,phone ,city, state, active)

#   db.session.add(new_org)
#   db.session.commit()

# @app.route('/org/add', methods=['POST'])
# def add_org_route():
#   data = request.form 
#   if not data:
#     data = request.json

#   name = data.get('name')
#   phone = data.get('phone')
#   city = data.get('city')
#   state = data.get('state')
#   active = data.get('active')

#   add_org(name, phone, city, state, active)

#   return jsonify("org created"), 200

# # # - Update Org
# # @app.route('/org/update/<org_id>', methods=(['POST', 'PUT']))
# # def update_org(org_id):
# #   update_fields = []
# #   update_values = []
# #   field_names = ['name', 'phone', 'city', 'state', 'active']

# #   post_data = request.form if request.form else request.json

# #   for field in field_names:
# #     print(field)
# #     field_value = post_data.get(field)
# #     if field_value:
# #       update_fields.append(str(field) + f'=%s')
# #       print(update_fields)
# #       update_values.append(field_value)
# #       print(update_values)

# #   if update_fields:
# #     update_values.append(org_id)
# #     query_string = "UPDATE Organizations SET " + ', '.join(update_fields) + " WHERE org_id=%s"
# #     cursor.execute(query_string, update_values)

# #     conn.commit()

# #     return jsonify("org updated"), 200
# #   else:
# #     return jsonify("no values sent in body"), 418

# # # - Get Org by ID
# # @app.route('/org/get/<org_id>', methods=(['GET']))
# # def get_org_by_id(org_id):
# #   cursor.execute("""SELECT * FROM Organizations WHERE org_id=%s""",[org_id])

# #   results = cursor.fetchone()

# #   if results:
# #     org = {
# #       'org_id': results[0],
# #       'name' : results[1],
# #       'phone' : results[2],
# #       'city' : results[3],
# #       'state' : results[4],
# #       'active' :results[5]
# #     }

# #     return jsonify(org), 201
# #   else:
# #     return jsonify('sorry org not found'), 418

# # # - Get all orgs
# # @app.route('/org/get', methods=['GET'])
# # def get_all_orgs():
# #   cursor.execute("""SELECT * FROM Organizations WHERE active=1;""")

# #   results = cursor.fetchall()
# #   if results:
# #     org_list = []
# #     for org in results:
# #       org = {
# #         'org_id': org[0],
# #         'name' : org[1],
# #         'phone' : org[2],
# #         'city' : org[3],
# #         'state' : org[4],
# #         'active' : org[5]
# #       }
# #       org_list.append(org)

# #     return jsonify(org_list), 200
# #   else:
# #     return jsonify("no organizations"), 404


# # # - Delete org
# # @app.route('/org/delete/<org_id>')
# # def org_delete(org_id):
# #   cursor.execute(f"""DELETE FROM Organizations WHERE org_id=%s;""",[org_id])

# #   conn.commit()

# #   return jsonify("Organization Deleted")

# # # - Deactivate org
# # @app.route('/org/deactivate/<org_id>')
# # def org_deactivate(org_id):
# #   cursor.execute(f"""UPDATE Organizations SET active=0 WHERE org_id=%s;""",[org_id])

# #   conn.commit()

# #   return jsonify("Organization Deactivated")

# # # - Activate org
# # @app.route('/org/activate/<org_id>')
# # def org_activate(org_id):
# #   cursor.execute("""UPDATE Organizations SET active=1 WHERE org_id=%s;""",[org_id])

# #   conn.commit()

# #   return jsonify("Organization Activated")

# if __name__ == '__main__':
#   create_all()
#   app.run(host='0.0.0.0', port=8089)

