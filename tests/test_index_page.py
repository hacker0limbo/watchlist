import unittest
from app import create_app, db
from models.user import User
from models.movie import Movie

app = create_app()


class TestIndexPage(unittest.TestCase):
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

    def test_get_movies(self):
        """测试所有 movies"""
        response = self.client.get('/api/v1/movie')
        json_data = response.get_json()
        movie = json_data[0]
        self.assertEquals('Test Movie Title', movie.get('title', None))
        self.assertEquals('2019', movie.get('year', None))

    def test_get_movie(self):
        """测试单个 move"""
        response = self.client.get('/api/v1/movie/1')
        movie = response.get_json()
        self.assertEquals('Test Movie Title', movie.get('title', None))
        self.assertEquals('2019', movie.get('year', None))

    def test_post_movie(self):
        """测试 movie 增加"""

        self.login_as_admin()
        # post 需要登录, 且发送方式仍旧为 form 方式
        response = self.client.post('/api/v1/movie', data={
            'title': 'Test Movie Title2',
            'year': '2018'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item created', data)
        self.assertEquals(2, Movie.query.count())

        # 测试失败情况, 例如 year 不符合
        response = self.client.post('/api/v1/movie', data={
            'title': 'Test Movie Title3',
            'year': '20190'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Invalid input.', data)
        self.assertEquals(2, Movie.query.count())

    def test_put_movie(self):
        """测试 movie 更新"""
        self.login_as_admin()

        response = self.client.put('/api/v1/movie/1', json={
            'title': 'Movie Title',
            'year': '2017'
        })
        updated_movie = response.get_json()
        self.assertEquals(1, Movie.query.count())
        self.assertEquals('Movie Title', updated_movie.get('title', None))
        self.assertEquals('2017', updated_movie.get('year', None))

    def test_delete_movie(self):
        """测试 movie 删除"""
        self.login_as_admin()
        response = self.client.delete('/api/v1/movie/1')
        deleted_movie = response.get_json()
        self.assertEquals(0, Movie.query.count())
        self.assertEquals('Test Movie Title', deleted_movie.get('title', None))
        self.assertEquals('2019', deleted_movie.get('year', None))
