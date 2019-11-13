import unittest
from app import create_app, db
from models.movie import Movie

app = create_app()


class TestDb(unittest.TestCase):
    """test database functionality"""

    @classmethod
    def setUpClass(cls):
        # 进入测试配置
        app.config.from_object("config.TestingConfig")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

        self.m1 = Movie.new(title='t1', year='2019')
        self.m2 = Movie.new({'title': 't2', 'year': '2019'})

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_new(self):
        self.assertEqual(2, Movie.query.count())
        self.assertEqual(self.m1.__dict__, Movie.query.filter_by(title='t1').first().__dict__)
        self.assertEqual(self.m2.__dict__, Movie.query.filter_by(title='t2').first().__dict__)

    def test_update_by_id(self):
        m1_id = Movie.query.filter_by(title='t1').first().id
        m2_id = Movie.query.filter_by(title='t2').first().id
        Movie.update_by_id(m1_id, year='2018')
        self.assertEqual('2018', Movie.query.filter_by(title='t1').first().year)
        Movie.update_by_id(m2_id, {'title': 'T2'})
        self.assertEqual('T2', Movie.query.filter_by(year='2019').first().title)

    def test_delete_by_id(self):
        m1_id = Movie.query.filter_by(title='t1').first().id
        Movie.delete_by_id(m1_id)
        self.assertEqual(1, Movie.query.count())

    def test_get_all(self):
        self.assertEqual(Movie.query.all(), Movie.get_all())

    def test_get(self):
        self.assertEqual(Movie.query.filter_by(title='t1').first(), Movie.get(title='t1'))

    def test_get_by_id(self):
        m1_id = Movie.query.filter_by(title='t1').first().id
        self.assertEqual(Movie.query.filter_by(id=m1_id).first(), Movie.get_by_id(m1_id))

    def test_to_dict(self):
        d1 = {
            'title': 't1',
            'year': '2019'
        }
        self.assertTrue(d1.items() <= self.m1.to_dict().items())

    def test_to_dict_all(self):
        d1 = {
            'title': 't1',
            'year': '2019'
        }
        d2 = {
            'title': 't2',
            'year': '2019'
        }
        l = [d1, d2]
        pairs = zip(l, Movie.to_dict_all())
        self.assertTrue(all(x.items() <= y.items() for x, y in pairs))
