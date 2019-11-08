from flask import Blueprint, render_template


router = Blueprint('index_bp', __name__)


@router.route('/')
def index():
    return render_template('index.html')