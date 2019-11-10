from flask import Blueprint, render_template
from models.movie import Movie

router = Blueprint('index_bp', __name__)


@router.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)
