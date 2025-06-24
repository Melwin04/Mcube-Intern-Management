from mongoengine import *
from uuid import uuid4
from datetime import datetime

class User(Document):
    meta = {"collection" : "user"}

    id = StringField (primary_key = True, default = lambda:str (uuid4()))
    name = StringField (required = True)
    email = EmailField(required = True)
    pasword = StringField(required = True)
    mobileNumber = StringField()
    addedTime = DateField(default=datetime.now())
    updatedTime = DateField()

class Intern(Document):
    meta = {"collection": "intern"}

    id = StringField(primary_key= True, default = lambda:str(uuid4()))
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    skills = ListField()
    addedTime = DateField(default=datetime.now())
    updatedTime = DateField()