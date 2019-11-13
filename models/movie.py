from models.base_model import db
from models.base_model import BaseModel


class Movie(BaseModel):
    __tablename__ = 'movies'

    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self.title == other.title \
               and self.year == other.year

    def __hash__(self):
        return hash((self.title, self.year))
