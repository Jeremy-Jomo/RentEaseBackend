from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

favorites = db.Table(
    'favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, doc="admin, landlord, tenant")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    properties = db.relationship('Property', back_populates='landlord', cascade="all, delete-orphan")
    bookings = db.relationship('Booking', back_populates='tenant', cascade="all, delete-orphan")
    favorite_properties = db.relationship('Property', secondary=favorites, back_populates='favorited_by')

    # relationship for landlord/tenant payments
    tenant_payments = db.relationship('Payment', foreign_keys='Payment.tenant_id', back_populates='tenant', cascade="all, delete-orphan")
    landlord_payments = db.relationship('Payment', foreign_keys='Payment.landlord_id', back_populates='landlord', cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_password):
        """Automatically hash passwords when setting them"""
        self._password_hash = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        """Verify a plaintext password against the stored hash"""
        return check_password_hash(self._password_hash, plain_password)


    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Invalid email address.")
        return address

    @validates('role')
    def validate_role(self, key, value):
        allowed = ['admin', 'landlord', 'tenant']
        if value not in allowed:
            raise ValueError(f"Invalid role. Must be one of {allowed}.")
        return value

    # total income property for landlords
    @property
    def total_income(self):
        """Calculate total completed payments for this landlord."""
        total = db.session.query(func.sum(Payment.amount)).filter_by(landlord_id=self.id, status='completed').scalar()
        return float(total or 0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "properties": [prop.id for prop in self.properties],
            "bookings": [booking.id for booking in self.bookings],
            "favorites": [p.id for p in self.favorite_properties],
            "total_income": self.total_income if self.role == "landlord" else None
        }


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rent_price = db.Column(db.Numeric(10, 2), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    landlord = db.relationship('User', back_populates='properties')
    bookings = db.relationship('Booking', back_populates='prop', cascade="all, delete-orphan")
    amenities = db.relationship('PropertyAmenity', back_populates='property', cascade="all, delete-orphan")
    images = db.relationship('PropertyImage', back_populates='property', cascade="all, delete-orphan")
    favorited_by = db.relationship('User', secondary=favorites, back_populates='favorite_properties')

    @validates('rent_price')
    def validate_rent_price(self, key, value):
        if value <= 0:
            raise ValueError("Rent price must be greater than 0.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "rent_price": str(self.rent_price),
            "location": self.location,
            "image_url": self.image_url,
            "available": self.available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "landlord_id": self.landlord_id,
            "landlord_name": self.landlord.name if self.landlord else None,
            "bookings": [booking.id for booking in self.bookings],
            "amenities": [a.to_dict() for a in self.amenities],
            "favorited_by": [u.id for u in self.favorited_by],
        }


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending", doc="pending, approved, paid, cancelled")  # ✅ ADDED paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tenant = db.relationship('User', back_populates='bookings')
    prop = db.relationship('Property', back_populates='bookings')
    payments = db.relationship('Payment', back_populates='booking', cascade="all, delete-orphan")
    review = db.relationship('Review', back_populates='booking', uselist=False)

    @validates('status')
    def validate_status(self, key, value):
        allowed = ["pending", "approved", "paid", "cancelled", "active"]
        if value not in allowed:
            raise ValueError(f"Invalid status. Must be one of {allowed}.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "tenant_name": self.tenant.name if self.tenant else None,
            "property_id": self.property_id,
            "property": self.prop.to_dict() if self.prop else None,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False, doc="credit_card, debit_card, bank_transfer, digital_wallet")
    status = db.Column(db.String(20), nullable=False, default="pending", doc="pending, completed, failed, refunded")
    transaction_id = db.Column(db.String(255), unique=True, nullable=False)
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship('Booking', back_populates='payments')
    tenant = db.relationship('User', foreign_keys=[tenant_id], back_populates='tenant_payments')  # ✅ ADDED back_populates
    landlord = db.relationship('User', foreign_keys=[landlord_id], back_populates='landlord_payments')  # ✅ ADDED back_populates

    @validates('amount')
    def validate_amount(self, key, value):
        if value <= 0:
            raise ValueError("Payment amount must be greater than 0.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "tenant_id": self.tenant_id,
            "tenant_name": self.tenant.name if self.tenant else None,
            "landlord_id": self.landlord_id,
            "landlord_name": self.landlord.name if self.landlord else None,
            "amount": str(self.amount),
            "payment_method": self.payment_method,
            "status": self.status,
            "transaction_id": self.transaction_id,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PropertyAmenity(db.Model):
    __tablename__ = "property_amenities"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    amenity_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    included = db.Column(db.Boolean, default=True)

    property = db.relationship('Property', back_populates='amenities')

    def to_dict(self):
        return {
            "id": self.id,
            "amenity_name": self.amenity_name,
            "description": self.description,
            "included": self.included
        }


class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    image_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String)
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    property = db.relationship('Property', back_populates='images')

    def to_dict(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "is_primary": self.is_primary,
            "sort_order": self.sort_order,
        }


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), unique=True, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    landlord_reply = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    booking = db.relationship('Booking', back_populates='review')

    @validates('rating')
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5 stars.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "review_text": self.review_text,
            "landlord_reply": self.landlord_reply,
            "is_approved": self.is_approved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
