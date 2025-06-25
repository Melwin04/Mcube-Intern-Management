from flask import Blueprint

taskBp = Blueprint("taskBp", __name__)

from . import routes