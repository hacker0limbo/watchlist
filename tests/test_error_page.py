import unittest
from app import create_app, db

app = create_app()


class TestErrorPage(unittest.TestCase):
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

        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_404_page(self):
        """测试错误页面"""
        response = self.client.get('/nothing')
        data = response.get_data(as_text=True)
        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(404, response.status_code)

    def test_400_page(self):
        pass

    def test_500_page(self):
        pass
