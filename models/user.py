from models.base_model import db
from models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    name = db.Column(db.String(20))
