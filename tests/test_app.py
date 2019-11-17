import unittest
from app import create_app, db
from models.user import User
from models.movie import Movie

app = create_app()


class TestApp(unittest.TestCase):
    """测试基本的 login, logout, admin 功能"""

    @classmethod
    def setUpClass(cls):
        # 进入测试配置
        app.config.from_object("config.TestingConfig")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # 传入上下文
        self.ctx = app.app_context()
        self.ctx.push()
        # 手动生成数据库表 schema
        db.create_all()

        user = User.new(username='test1')
        user.set_hash_password('test1')
        admin = User.new(username='admin')
        admin.set_hash_password('admin')

        Movie.new(title='Test Movie Title', year='2019')

        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def login(self, post_data):
        response = self.client.post('/login', data=post_data, follow_redirects=True)
        return response

    def logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        return response

    def test_index_page(self):
        """测试未登录下的主页"""
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn("Limboer's Watchlist", data)
        self.assertIn("Home", data)
        # 未登录无法访问 movie list, settings, Logout page
        self.assertNotIn("Test Movie Title", data)
        self.assertNotIn("Logout", data)
        self.assertNotIn("Settings", data)

    def test_user_login_success(self):
        response = self.login(dict(
            username='test1',
            password='test1'
        ))
        data = response.get_data(as_text=True)
        self.assertIn('Login successfully.', data)
        self.assertIn('Logout', data)
        self.assertIn('Settings', data)
        self.assertIn("Test Movie Title", data)
        self.assertIn("Add New Movie", data)

        # 测试非 admin 用户
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)

    def test_admin_login_success(self):
        response = self.login(dict(
            username='admin',
            password='admin'
        ))
        data = response.get_data(as_text=True)
        self.assertIn('Login successfully.', data)
        self.assertIn('Edit', data)
        self.assertIn('Delete', data)

    def test_user_login_fail(self):
        response = self.login(dict(
            username='xxx',
            password='yyy'
        ))
        data = response.get_data(as_text=True)
        self.assertNotIn('Login successfully.', data)
        self.assertIn('Username or password is wrong, please try again.', data)

    def test_logout_success(self):
        self.login(dict(
            username='test1',
            password='test1'
        ))
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('You logged out.', data)
        self.assertNotIn("Test Movie Title", data)
        self.assertNotIn("Logout", data)
        self.assertNotIn("Settings", data)
