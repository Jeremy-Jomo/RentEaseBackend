from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_migrate import Migrate
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import os
import cloudinary
import cloudinary.uploader
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from server.swagger_spec import get_swagger_spec


from server.config import Config
from server.models import db, User, Property, PropertyImage, PropertyAmenity, Booking, Payment, Review

app = Flask(__name__)
app.config.from_object(Config)


SWAGGER_URL = '/docs'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Rent Ease API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

CORS(app,
     origins=["*"],
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
     allow_headers=["Content-Type", "Authorization", "Accept"]
)

jwt = JWTManager()

db.init_app(app)
with app.app_context():
    db.create_all()
jwt.init_app(app)

from server.models import User, Property, Booking


@app.route('/swagger.json')
def swagger_spec():
    return jsonify(get_swagger_spec())



@app.route('/properties/<int:property_id>', methods=['OPTIONS'])
def options_property(property_id):
    return '', 200


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "Rent Ease Backend"
    }), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        total_users = User.query.count()
        total_properties = Property.query.count()
        total_bookings = Booking.query.count()

        return jsonify({
            "total_users": total_users,
            "total_properties": total_properties,
            "total_bookings": total_bookings
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get stats: {str(e)}"}), 500

@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']

        if image_file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        upload_result = cloudinary.uploader.upload(image_file)

        return jsonify({
            "message": "Image uploaded successfully",
            "image_url": upload_result['secure_url']
        }), 200

    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

def send_booking_email(recipient_email, recipient_name, booking_type, booking_data):
    """Send booking notification emails"""
    try:
        if not Config.SENDGRID_API_KEY:
            print("SendGrid not configured - skipping email")
            return True

        sg = sendgrid.SendGridAPIClient(api_key=Config.SENDGRID_API_KEY)
        return True

    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False

migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

# Property routes (your existing code remains unchanged)
@app.route('/properties')
def get_properties():
    properties = Property.query.all()
    return jsonify([p.to_dict() for p in properties])

@app.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Property not found"}), 404
    return jsonify(prop.to_dict()), 200

@app.route('/properties', methods=['POST'])
def create_property():
    data = request.get_json()

    # Check required fields
    required_fields = ['title', 'description', 'rent_price', 'location']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Create the property
    new_property = Property(
        title=data['title'],
        description=data['description'],
        rent_price=float(data['rent_price']),
        location=data['location'],
        image_url=data.get('image_url'),
        landlord_id=data.get('landlord_id')
    )

    db.session.add(new_property)
    db.session.commit()

    return jsonify(new_property.to_dict()), 201


@app.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    prop = db.session.get(Property, property_id)  # ✅ modern SQLAlchemy 2.0 style
    if not prop:
        return jsonify({"error": "Property not found"}), 404

    data = request.get_json()

    prop.title = data.get('title', prop.title)
    prop.description = data.get('description', prop.description)
    prop.location = data.get('location', prop.location)

    # ✅ Convert rent_price safely
    if 'rent_price' in data:
        try:
            prop.rent_price = float(data['rent_price'])
        except ValueError:
            return jsonify({"error": "Invalid rent price format"}), 400

    # ✅ Handle image update (if link provided)
    if 'image_url' in data:
        prop.image_url = data['image_url']

    db.session.commit()
    return jsonify(prop.to_dict()), 200


@app.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Property not found"}), 404

    db.session.delete(prop)
    db.session.commit()
    return jsonify({"message": "Property deleted"}), 200

# Bookings routes (your existing code remains unchanged)
@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()

    tenant_id = data['tenant_id']
    property_id = data['property_id']
    start_date = data['start_date']
    end_date = data['end_date']

    if not all([tenant_id, property_id, start_date, end_date]):
        return jsonify({"error": "Missing required fields"}), 400

    new_booking = Booking(
        tenant_id=tenant_id,
        property_id=property_id,
        start_date=start_date,
        end_date=end_date
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify(new_booking.to_dict()), 201

@app.route('/bookings', methods=['GET'])
def get_tenant_bookings():
    tenant_id = request.args.get('tenant_id')
    if not tenant_id:
        return jsonify({"error": "tenant_id query param required"}), 400

    bookings = Booking.query.filter_by(tenant_id=tenant_id).all()
    return jsonify([b.to_dict() for b in bookings]), 200

@app.route('/bookings/<int:id>', methods=['GET'])
def get_booking(id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(booking.to_dict()), 200

@app.route("/bookings/<int:id>", methods=["PUT"])
def update_booking_status(id):
    data = request.get_json()
    status = data.get("status", "").lower()  # normalize to lowercase

    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    allowed = ["pending", "approved", "cancelled"]
    if status not in allowed:
        return jsonify({"error": f"Invalid status. Must be one of {allowed}"}), 400

    booking.status = status
    db.session.commit()
    return jsonify({"message": f"Booking status updated to {status}"}), 200



@app.route('/bookings/<int:id>', methods=['DELETE'])
def cancel_booking(id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200

@app.route('/landlord/bookings', methods=['GET'])
def get_landlord_bookings():
    landlord_id = request.args.get('landlord_id')
    if not landlord_id:
        return jsonify({"error": "landlord_id query param required"}), 400

    bookings = (
        Booking.query.join(Property)
        .filter(Property.landlord_id == landlord_id)
        .all()
    )
    return jsonify([b.to_dict() for b in bookings]), 200

@app.route('/bookings/<int:id>/payment', methods=['PUT'])
def simulate_payment(id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    booking.payment_status = 'Paid'
    db.session.commit()
    return jsonify({"message": "Payment simulated successfully", "booking": booking.to_dict()}), 200



@app.route('/admin/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@app.route('/admin/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {id} deleted successfully"}), 200

@app.route('/admin/properties', methods=['GET'])
def get_all_properties():
    properties = Property.query.all()
    return jsonify([p.to_dict() for p in properties]), 200

@app.route('/admin/bookings', methods=['GET'])
def get_all_bookings_admin():
    bookings = Booking.query.all()
    return jsonify([b.to_dict() for b in bookings]), 200

# Login route (your existing code remains unchanged)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": user.to_dict(),
            "id":user.id
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Validation
    if not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    role = data.get('role', 'tenant')
    if role not in ['admin', 'landlord', 'tenant']:
        return jsonify({"error": "Invalid role"}), 400

    new_user = User(
        name=data['name'],
        email=data['email'],
        role=role
    )
    new_user.password = data['password']

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
# ✅ Temporary route to seed Render database
@app.route('/seed', methods=['POST'])
def seed_data():
    from server.models import Property
    from server import db

    with app.app_context():
        # Prevent duplicate seeding
        if Property.query.first():
            return jsonify({"message": "Database already seeded!"}), 200

        properties = [
            Property(
                title="Modern Apartment in Westlands",
                description="Spacious 2-bedroom apartment with balcony and parking.",
                location="Nairobi",
                rent_price=75000,
                image_url="https://res.cloudinary.com/demo/image/upload/sample.jpg"
            ),
            Property(
                title="Beachfront Villa",
                description="Luxury 4-bedroom villa overlooking the Indian Ocean.",
                location="Mombasa",
                rent_price=250000,
                image_url="https://res.cloudinary.com/demo/image/upload/sample.jpg"
            ),
            Property(
                title="Affordable Studio",
                description="Compact studio ideal for singles near CBD.",
                location="Kisumu",
                rent_price=30000,
                image_url="https://res.cloudinary.com/demo/image/upload/sample.jpg"
            )
        ]

        db.session.add_all(properties)
        db.session.commit()
        return jsonify({"message": "✅ Database seeded successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)