from .. import db
from datetime import datetime
import enum
from flask_bcrypt import Bcrypt


class HIVStatusEnum(str, enum.Enum):
    Positive = "Positive"
    Negative = "Negative"


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(100), unique=True, nullable=False)
    password = db.Column(db.VARCHAR(500), nullable=False)
    first_name = db.Column(db.VARCHAR(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    surname = db.Column(db.VARCHAR(100), nullable=False)
    HIV_status = db.Column(db.Enum(HIVStatusEnum,
                                     values_callable=lambda x: [str(e.value) for e in HIVStatusEnum]),
                                     nullable=False)
    Phone_number = db.Column(db.VARCHAR(20), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=db.func.current_timestamp())

    def serialise(self):
        '''serialize model object into json object'''
        json_obj = {}
        for column in self.__table__.columns:
            json_obj[column.name] = str(getattr(self, column.name))
        return json_obj



    @staticmethod
    def hash_password(password):
        '''use bcrypt to hash passwords'''
        return Bcrypt().generate_password_hash(password).decode()

    def is_password_valid(self, password):
        '''Check the password against it's hash to validates the user's password
            (returns True if passwords match)
        '''
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
