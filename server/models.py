from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String, doc="admin, landlord, tenant")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #relationships
    properties = db.relationship('Property', back_populates='landlord')
    bookings = db.relationship('Booking', back_populates='tenant')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "properties": [prop.id for prop in self.properties],
            "bookings": [booking.id for booking in self.bookings],
        }

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    rent_price = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #relationships
    landlord = db.relationship('User', back_populates='properties')
    bookings = db.relationship('Booking', back_populates='prop')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "rent_price": self.rent_price,
            "location": self.location,
            "image_url": self.image_url,
            "available": self.available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "landlord_id": self.landlord_id,
            "landlord_name": self.landlord.name if self.landlord else None,
            "bookings": [booking.id for booking in self.bookings],
        }

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, nullable=False, doc="pending, approved, cancelled")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #relationships
    tenant = db.relationship('User', back_populates='bookings')
    prop = db.relationship('Property', back_populates='bookings')

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "tenant_name": self.tenant.name if self.tenant else None,
            "property_id": self.property_id,
            "property_title": self.prop.title if self.prop else None,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
