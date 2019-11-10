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
        m = cls()
        for name, value in form.items():
            setattr(m, name, value)
        db.session.add(m)
        db.session.commit()
        return m
