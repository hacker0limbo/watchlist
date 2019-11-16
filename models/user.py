from models.base_model import db
from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    username = db.Column(db.String(20))
    # 存取密码的散列值
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(60), default='avatar_default.png')

    def set_hash_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_avatar(self, new_avatar):
        self.avatar = new_avatar
        db.session.commit()

    @property
    def is_admin(self):
        """判断是否是 admin 用户, 账号硬编码为 admin, admin"""
        admin = self.__class__.get(username='admin')
        if self.password_hash != admin.password_hash or self.username != admin.username:
            return False
        return True

    @classmethod
    def validate_login(cls, form):
        username = form.get('username', '')
        password = form.get('password', '')
        user = cls.get(username=username)
        if user is not None and user.validate_password(password):
            return user
        return None

    @classmethod
    def register(cls, form):
        username = form.get('username', '')
        password = form.get('password', '')
        if username and password and cls.get(username=username) is None:
            # 检查用户名不能重复
            user = cls.new(username=username)
            user.set_hash_password(password)
            return user

        return None

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
