from flask import Blueprint

internBp = Blueprint("internBp", __name__)

from . import routes
