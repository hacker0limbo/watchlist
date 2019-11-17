import unittest
from app import create_app, db
from models.user import User
from models.movie import Movie

app = create_app()


class TestSettingsPage(unittest.TestCase):
    """测试基本的 index page 增删改查 功能"""

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

    def login_as_admin(self):
        response = self.client.post('/login', data=dict(
            username='admin',
            password='admin'
        ), follow_redirects=True)
        return response

    def test_index_page(self):
        self.login_as_admin()

        response = self.client.get('/settings/')
        data = response.get_data(as_text=True)
        self.assertIn('Settings', data)
        self.assertIn('Update your password', data)
        self.assertIn('Update your avatar', data)

    def test_reset_password(self):
        self.login_as_admin()
        response = self.client.post('/settings/password', data={
            'new-password': '321',
            'password-confirm': '321'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Password successfully updated', data)

        response = self.client.post('/settings/password', data={
            'new-password': '123',
            'password-confirm': '321'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Two password input have to be the same', data)
