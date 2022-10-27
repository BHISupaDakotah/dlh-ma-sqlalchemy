import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma
from organizations import OrganizationsSchema
from classes import ClassesSchema # to use object and virtual columns
from students_class_association import association_table

class Users(db.Model):
  __tablename__='users' # in future name class Users and __tablename__ 'Users' the same
  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  first_name = db.Column(db.String(), nullable=False)
  last_name = db.Column(db.String())
  email = db.Column(db.String(), nullable=False, unique=True)
  phone = db.Column(db.String())
  city = db.Column(db.String())
  state = db.Column(db.String())
  org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.org_id'), nullable = False)
  active = db.Column(db.Boolean(), default=True)
  

  # class_id = db.Column(UUID(as_uuid=True), db.ForignKey('classes.class)_id'), nullable=True)
  # var name = db.relationship('[Class Name]', secondary=[Many:Many table], back_populates='[virtual_column_variable ie 'users' from classes.py line 15 ]')
  subject_class = db.relationship('Classes', secondary=association_table, back_populates='users')
  organization = db.relationship('Organizations', back_populates='users')


  def __init__(self, first_name,last_name, email, phone, city, state, org_id, active):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.phone = phone
    self.city = city
    self.state = state
    self.org_id = org_id
    self.active = active

class UsersSchema(ma.Schema):
  # uses reflection from marshmallow library
  class Meta:
    fields = ['user_id', 'first_name', 'last_name', 'email', 'phone', 'city', 'state', 'organization', 'active', 'class_id', 'subject_class'] #-from line 24
  
  # make sure schema matches backref in fields value
  # var name = ma.fields.Nested(Schema(only=(specific keys from object)))
  organization = ma.fields.Nested(OrganizationsSchema(only=('org_id', 'name', 'active')))

  # subject_class = ma.fields.Nested(ClassesSchema(only=('name', 'credit')))
  # var name = ma.fields.Nested('[Schema as string]', many=True, exclude='[var name from classes.py line 16]')
  subject_class = ma.fields.Nested('ClassesSchema', many=True, exclude=['users'])

user_schema = UsersSchema()
users_schema = UsersSchema( many=True )
                                # ^^ list of objects