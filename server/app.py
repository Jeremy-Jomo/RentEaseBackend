from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_migrate import Migrate
from flask_cors import CORS

from datetime import datetime
import os
import cloudinary
import cloudinary.uploader
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

from server.config import Config
from server.models import db, User, Property, PropertyImage, PropertyAmenity, Booking, Payment, Review


app = Flask(__name__)
app.config.from_object(Config)


CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://rent-ease-silk.vercel.app/" , "https://vercel.com/jeremykirubi-5207s-projects/rent-ease/9mB7K6o76qUNgpsEVwVHxFNKEx5z"])

jwt = JWTManager()



db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)


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
        # Use the database within app context
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


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})


#property routes
@app.route('/properties', methods=['GET'])
def get_properties():
    propertys= Property.query.all()
    return jsonify([prop.to_dict() for prop in propertys]), 200


@app.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Property not found"}), 404
    return jsonify(prop.to_dict()), 200

@app.route('/properties', methods=['POST'])
def create_property():
    data = request.get_json()
    new_property = Property(
        title=data['title'],
        description=data['description'],
        rent_price=data['price'],
        location=data['location']
    )
    db.session.add(new_property)
    db.session.commit()
    return jsonify(new_property.to_dict()), 201

@app.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Property not found"}), 404

    data = request.get_json()
    prop.title = data.get('title', prop.title)
    prop.description = data.get('description', prop.description)
    prop.rent_price = data.get('price', prop.price)
    prop.location = data.get('location', prop.location)
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


#bookings routes
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


@app.route('/bookings/<int:id>', methods=['PUT'])
def update_booking_status(id):

    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    data = request.get_json()
    status = data.get('status')
    if status not in ['Approved', 'Rejected']:
        return jsonify({"error": "Invalid status"}), 400

    booking.status = status
    db.session.commit()
    return jsonify(booking.to_dict()), 200


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


#admin routes
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

#login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        # Generate JWT token, for example
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": user.to_dict()
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(
        name=data['name'],
        email=data['email'],
        role=data['role']
    )
    new_user.password = data['password']  # ✅ triggers hashing automatically

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)