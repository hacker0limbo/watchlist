from flask import Blueprint, render_template
from models.movie import Movie

router = Blueprint('index_bp', __name__)


@router.route('/', methods=['GET'])
def index():
    movies = Movie.all()
    return render_template('index.html', movies=movies)
