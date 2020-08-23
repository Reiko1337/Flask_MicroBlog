from flask.blueprints import Blueprint

profile = Blueprint('profile', __name__)

from . import controllers
