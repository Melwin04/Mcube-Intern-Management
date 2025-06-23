from mongoengine import *
from uuid import uuid4
from datetime import datetime

class User(Document):
    meta = {"collection" : "app"}

    id = StringField (primary_key = True, default = lambda:str (uuid4()))
    name = StringField (required = True)
    email = EmailField(required = True)
    pasword = StringField(required = True)
    mobileNumber = StringField()
    addedTime = DateField(default=datetime.now())
    updatedTime = DateField()