"""Database models."""
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

"""This is where we create our tables which MODEL the tables in the database. MODELS GET IT?! HAHA... help"""


class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=False)

    email = db.Column(db.String(40), unique=True, nullable=False)

    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    website = db.Column(db.String(60), index=False, unique=False, nullable=True)

    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Plants(db.Model):
    """Model for Plants"""

    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    userID = db.Column(db.Integer, nullable=False)

    plantName = db.Column(db.String(100), nullable=False)

    plantType = db.Column(db.String(100), nullable=False)

    plantThirst = db.Column(db.Integer, nullable=False)

    sensorID = db.Column(db.Integer)

    def __repr__(self):
        return '<Plants {}>'.format(self.plantName)


class SensorInfo(db.Model):
    """Model for sensorInfo table"""

    __tablename__ = 'sensorInfo'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    sensorID = db.Column(db.Integer)

    sensorTime = db.Column(db.DATETIME, nullable=False)

    moistRead = db.Column(db.Integer)

    def __repr__(self):
        return '<SensorInfo {}>'.format(self.moistRead)




class Sensors(db.Model):
    """Model for sensors table """

    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    sensorID = db.Column(db.Integer, nullable=False)

    sensorName = db.Column(db.String(100))

    def __repr__(self):
        return '<Sensors {}>'.format(self.sensorName)

