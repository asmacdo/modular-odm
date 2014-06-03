from modularodm import StoredObject, fields
from modularodm.validators import MinLengthValidator, MaxLengthValidator

#TODO(asmacdo) index type?
class User(StoredObject):

    _meta = {"optimistic": True}
    _id = fields.StringField(primary=True, index=True)
    username = fields.StringField(required=True, index=True)
    password = fields.StringField(required=True, validate=[MinLengthValidator(8)])

    def __repr__(self):
        return "<User: {0}>".format(self.username)

class Comment(StoredObject):
    _meta = {"optimistic": True}
    _id = fields.StringField(primary=True, index=True)
    text = fields.StringField(validate=MaxLengthValidator(500))
    user = fields.ForeignField("User", backref="comments")

    def __repr__(self):
        return "<Comment: {0}>".format(self.text)
