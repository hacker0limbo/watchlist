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
    def new(cls, form=None, **kwargs):
        """增加一个 record, 可以接受字典形式, 也可以接受 k:v 形式"""
        m = cls()
        if form:
            for name, value in form.items():
                setattr(m, name, value)
        else:
            for name, value in kwargs.items():
                setattr(m, name, value)
        db.session.add(m)
        db.session.commit()
        return m

    @classmethod
    def update_by_id(cls, m_id, form=None, **kwargs):
        """根据 id 更新一个 record, 可以接受字典形式, 也可以接受 k:v 形式"""
        m = cls.query.filter_by(id=m_id).first()
        if form:
            for name, value in form.items():
                setattr(m, name, value)
        else:
            for name, value in kwargs.items():
                setattr(m, name, value)
        db.session.commit()

    @classmethod
    def delete_by_id(cls, m_id):
        """根据 id 删除一个数据"""
        m = cls.get_by_id(m_id)
        db.session.delete(m)
        db.session.commit()

    @classmethod
    def get_all(cls, **kwargs):
        """query 所有数据"""
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def get(cls, **kwargs):
        """query 一个数据"""
        m = cls.query.filter_by(**kwargs).first()
        return m

    @classmethod
    def get_by_id(cls, m_id):
        """根据 id 获取一个数据"""
        m = cls.query.get(m_id)
        return m

    def to_dict(self):
        d = {}
        for key in self.__mapper__.c.keys():
            d[key] = getattr(self, key)
        return d

    @classmethod
    def to_dict_all(cls):
        return [m.to_dict() for m in cls.get_all()]

    def __repr__(self):
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)
