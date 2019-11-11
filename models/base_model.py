import time
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    # https://stackoverflow.com/questions/22976445/how-do-i-declare-a-base-model-class-in-flask-sqlalchemy
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_time = db.Column(db.Integer, default=int(time.time()))
    updated_time = db.Column(db.Integer, default=int(time.time()))

    @classmethod
    def new(cls, form):
        """增加一个 record"""
        m = cls()
        for name, value in form.items():
            setattr(m, name, value)
        db.session.add(m)
        db.session.commit()
        return m

    @classmethod
    def update_by_id(cls, m_id, **kwargs):
        """根据 id 更新一个 record"""
        m = cls.query.filter_by(id=m_id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)
        db.session.add(m)
        db.session.commit()

    @classmethod
    def all(cls, **kwargs):
        """query 所有数据"""
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def one(cls, **kwargs):
        """query 一个数据"""
        m = cls.query.filter_by(**kwargs).first()
        return m

    @classmethod
    def get(cls, m_id):
        """根据 id 获取一个数据"""
        m = cls.query.get(m_id)
        return m

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        d = dict()
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                d[attr] = v
        return d

    def to_dict(self):
        d = {}
        for key in self.__mapper__.c.keys():
            d[key] = getattr(self, key)
        return d

    @classmethod
    def to_dict_all(cls):
        return [m.to_dict() for m in cls.all()]

    def __repr__(self):
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)
