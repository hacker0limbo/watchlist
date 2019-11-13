from models.base_model import db
from models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    name = db.Column(db.String(20))

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
