class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String, doc="admin", "landlord", "tenant")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

