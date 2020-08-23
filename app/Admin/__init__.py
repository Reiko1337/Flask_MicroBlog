from flask import Blueprint

Admin = Blueprint('Admin', __name__)

from . import controllers
