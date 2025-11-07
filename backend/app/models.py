"""SQLAlchemy models for the application."""
from datetime import datetime
from app.db import db


class User(db.Model):
    """User model with RFID tag support."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    rfid_tag = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reads = db.relationship('Read', back_populates='user', cascade='all, delete-orphan')
    accesses = db.relationship('Access', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'


class Read(db.Model):
    """Read model with relationships to Pump, Sensor, Fan, and Smoke."""
    
    __tablename__ = 'reads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships (one-to-one)
    user = db.relationship('User', back_populates='reads')
    pump = db.relationship('Pump', back_populates='read', uselist=False, cascade='all, delete-orphan')
    sensor = db.relationship('Sensor', back_populates='read', uselist=False, cascade='all, delete-orphan')
    fan = db.relationship('Fan', back_populates='read', uselist=False, cascade='all, delete-orphan')
    smoke = db.relationship('Smoke', back_populates='read', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Read {self.name}>'


class Pump(db.Model):
    """Pump model linked to a Read."""
    
    __tablename__ = 'pumps'
    
    id = db.Column(db.Integer, primary_key=True)
    read_id = db.Column(db.Integer, db.ForeignKey('reads.id'), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    
    # Relationship
    read = db.relationship('Read', back_populates='pump')
    
    def __repr__(self):
        return f'<Pump read_id={self.read_id}>'


class Sensor(db.Model):
    """Sensor model with humidity and temperature readings."""
    
    __tablename__ = 'sensors'
    
    id = db.Column(db.Integer, primary_key=True)
    read_id = db.Column(db.Integer, db.ForeignKey('reads.id'), unique=True, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    
    # Relationship
    read = db.relationship('Read', back_populates='sensor')
    
    def __repr__(self):
        return f'<Sensor read_id={self.read_id}>'


class Fan(db.Model):
    """Fan model linked to a Read."""
    
    __tablename__ = 'fans'
    
    id = db.Column(db.Integer, primary_key=True)
    read_id = db.Column(db.Integer, db.ForeignKey('reads.id'), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    
    # Relationship
    read = db.relationship('Read', back_populates='fan')
    
    def __repr__(self):
        return f'<Fan read_id={self.read_id}>'


class Smoke(db.Model):
    """Smoke detector model linked to a Read."""
    
    __tablename__ = 'smokes'
    
    id = db.Column(db.Integer, primary_key=True)
    read_id = db.Column(db.Integer, db.ForeignKey('reads.id'), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    
    # Relationship
    read = db.relationship('Read', back_populates='smoke')
    
    def __repr__(self):
        return f'<Smoke read_id={self.read_id}>'


class Access(db.Model):
    """Access log model for tracking user access."""
    
    __tablename__ = 'access'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', back_populates='accesses')
    
    def __repr__(self):
        return f'<Access user_id={self.user_id}>'


class Threshold(db.Model):
    """Threshold model for humidity and temperature limits (single record)."""
    
    __tablename__ = 'thresholds'
    
    id = db.Column(db.Integer, primary_key=True)
    min_humidity = db.Column(db.Float, nullable=False)
    max_humidity = db.Column(db.Float, nullable=False)
    min_temperature = db.Column(db.Float, nullable=False)
    max_temperature = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Threshold hum:{self.min_humidity}-{self.max_humidity} temp:{self.min_temperature}-{self.max_temperature}>'
