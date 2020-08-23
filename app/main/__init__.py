from flask.blueprints import Blueprint

main = Blueprint('main', __name__)

from . import controllers
