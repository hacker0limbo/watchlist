import unittest
from app import create_app, db
from models.user import User
from models.movie import Movie
from commands import forge, initdb

app = create_app()


class TestCommands(unittest.TestCase):
    """test application functionality"""

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

    # 测试命令
    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)
        self.assertEqual(0, User.query.count())

    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('Mock data generated.', result.output)
        self.assertNotEqual(0, Movie.query.count())
