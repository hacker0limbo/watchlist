from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.movie import Movie
from models.user import User
from flask_login import login_user, login_required, logout_user

router = Blueprint('index_bp', __name__)


@router.route('/', methods=['GET'])
def index():
    movies = Movie.get_all()
    return render_template('index.html', movies=movies)


@router.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form.to_dict()
        username = form.get('username', None)
        password = form.get('password', None)
        if not username or not password:
            flash('Invalid input', 'danger')
            return redirect(url_for('index_bp.login'))

        user = User.validate_login(form)
        if user is not None:
            # 说明用户存在, 验证登录成功
            login_user(user)
            flash('Login successfully.', 'success')
            return redirect(url_for('index_bp.index'))
        else:
            flash('username or password is wrong, please try again.', 'danger')
            return redirect(url_for('index_bp.login'))

    return render_template('login.html')


@router.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out.', 'info')
    return redirect(url_for('index_bp.index'))


@router.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = request.form.to_dict()
        user = User.register(form)
        if user is None:
            flash('The username has already been registered, please try a new one.', 'warning')
            return redirect(url_for('index_bp.signup'))
        else:
            flash('Registration successfully!', 'success')
            return redirect(url_for('index_bp.login'))

    return render_template('signup.html')
