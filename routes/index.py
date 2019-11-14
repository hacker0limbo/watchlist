from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.movie import Movie
from models.user import User
from flask_login import login_user, login_required, logout_user, current_user

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
            flash('Login success.', 'success')
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


@router.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        new_password = request.form['new-password']
        password_confirm = request.form['password-confirm']
        if new_password != password_confirm:
            # 后端检查两次密码输入是否一致
            flash('Two password input have to be the same', 'danger')
            return redirect(url_for('index_bp.settings'))

        current_user.set_hash_password(new_password)
        flash('Password successfully updated', 'success')
        return redirect(url_for('index_bp.settings'))

    return render_template('settings.html')
