from flask import Blueprint

router = Blueprint('api_v1_bp', __name__)

from routes.api.v1 import movie
