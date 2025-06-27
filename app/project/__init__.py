from flask import Blueprint

projectBp = Blueprint("projectBp", __name__)

from . import routes  
