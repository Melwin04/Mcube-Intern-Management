from flask import Blueprint

mainBp = Blueprint("mainBp", __name__)

from . import routes