# an example of an sql alchemy model - how to define our tables using a python class

import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

# table and table fields
class Organizations(db.Model):
  __tablename__='organizations'
  org_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(), nullable=False, unique=True)
  phone = db.Column(db.String())
  city = db.Column(db.String())
  state = db.Column(db.String())
  active = db.Column(db.Boolean(), default=True)
  users = db.relationship('Users', backref='organization', lazy=True)

# how to set values on table fields
  def __init__(self, name, phone, city, state, active):
    self.name = name
    self.phone = phone
    self.city = city
    self.state = state
    self.active = active

# schema class will define what feilds within organization are going to be built
# marshmallow aliased as ma
class OrganizationsSchema(ma.Schema):
  # meta class is used by marshmallow to determine what fields to return in the json
  class Meta:
    fields = ['org_id', 'name', 'phone', 'city', 'state', 'active']

# single get - single dictionary /.first()
organization_schema = OrganizationsSchema()
# many get - list of dictionaries / .all()
organizations_schema = OrganizationsSchema( many=True )