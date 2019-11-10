from models.base_model import db
from models.base_model import BaseModel


class Movie(BaseModel):
    __tablename__ = 'movies'

    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
