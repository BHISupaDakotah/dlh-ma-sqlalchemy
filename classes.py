from email.policy import default
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma
# from users import UsersSchema
from students_class_association import association_table

class Classes(db.Model):
  __tablename__='classes'
  class_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(), nullable=False, unique=True)
  credit = db.Column(db.Integer(), nullable=False)
  active = db.Column(db.Boolean(), default=True)
 # var name = db.relationship('[Class Name]', secondary=[Many:Many table], back_populates='[virtual_column_variable ie 'subject_class' from users.py line 24 ]')
  users = db.relationship('Users', secondary=association_table, back_populates='subject_class')

  def __init__(self, name, credit, active):
    self.name = name
    self.credit = credit
    self.active = active


class ClassesSchema(ma.Schema):
  users = ma.fields.Nested('UsersSchema', many=True, exclude=['subject_class'])
  class Meta:
    fields = ['class_id', 'name', 'credit', 'active', 'users']

class_schema = ClassesSchema()
classes_schema = ClassesSchema(many=True)
