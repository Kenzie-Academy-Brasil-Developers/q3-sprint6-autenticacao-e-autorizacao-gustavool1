from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from app.configs.database import db
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class UserModel(db.Model):

    __tablename__= "users"

    id = Column(Integer, primary_key = True)
    name:str = Column(String(127), nullable = False)
    last_name:str = Column(String(511), nullable = False)
    email:str = Column(String(255), nullable = False, unique = True)
    password_hash = Column(String(511), nullable = False)
    api_key = Column(String(511), nullable = False)

    @property
    def password(self):
        raise AttributeError("password attribute it's not acessible")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
