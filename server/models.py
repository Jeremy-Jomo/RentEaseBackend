class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String, doc="admin, landlord, tenant")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullabe=False)
    description = db.Column(db.String, nullable=False)
    rent_price = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForignKey('properties.id'), nullable=False)
    start_date = db.Column(db.Date, nulllable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, nullable=False, doc="pending, approved, cancelled")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
