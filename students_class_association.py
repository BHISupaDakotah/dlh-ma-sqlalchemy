from db import db
import marshmallow as ma

association_table = db.Table(
  "UserClassAssociation",
  db.Model.metadata,
  db.Column('user_id', db.ForeignKey('users.user_id'), primary_key=True),
  db.Column('class_id', db.ForeignKey('classes.class_id'), primary_key=True)
)

#class or vairable  - - for simple join
# 