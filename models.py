from mongoengine import *
from uuid import uuid4
from datetime import datetime

class User(Document):
    meta = {"collection" : "user"}

    id = StringField (primary_key = True, default = lambda:str (uuid4()))
    name = StringField (required = True)
    email = EmailField(required = True)
    password = StringField(required = True)
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

class Project(Document):
    meta = {"collection": "projects"}

    id = StringField(primary_key=True, default=lambda: str(uuid4()))
    name = StringField(required=True)
    description = StringField()
    addedTime = DateField(default=datetime.now())
    updatedTime = DateField()

class Task(Document):
    meta = {"collection": "task"}
    
    id = StringField(primary_key=True, default=lambda: str(uuid4()))
    taskName = StringField(required=True)
    taskDescription = StringField()
    project = ReferenceField(Project,reverse_delete_rule=CASCADE, required = True)
    user = ReferenceField(User,reverse_delete_rule=CASCADE, required = True)
    addedTime = DateField(default=datetime.now())
    updatedTime = DateField()