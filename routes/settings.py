from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES

router = Blueprint('settings_bp', __name__)
avatars = UploadSet('avatars', IMAGES)


@router.route('/')
@login_required
def index():
    return render_template('settings.html')


@router.route('/password', methods=['POST'])
@login_required
def reset_password():
    new_password = request.form['new-password']
    password_confirm = request.form['password-confirm']
    if new_password != password_confirm:
        # 后端检查两次密码输入是否一致
        flash('Two password input have to be the same', 'danger')
        return redirect(url_for('settings_bp.index'))

    current_user.set_hash_password(new_password)
    flash('Password successfully updated', 'success')
    return redirect(url_for('settings_bp.index'))


@router.route('/avatar', methods=['POST'])
@login_required
def upload_avatar():
    try:
        if 'avatar' in request.files:
            avatar_name = avatars.save(request.files['avatar'])
            # 上传的图片的 url 地址为: /_uploads/avatars/filename.png
            avatar_url = avatars.url(avatar_name)
            current_user.set_avatar(avatar_name)
            flash('Upload avatar successfully!', 'success')
    except Exception as e:
        flash('Please choose an image before upload.', 'warning')
    return redirect(url_for('settings_bp.index'))
