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

# Swagger setup
SWAGGER_URL = '/docs'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={'app_name': "Rent Ease API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# CORS setup
CORS(app,
     origins=["*"],
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
     allow_headers=["Content-Type", "Authorization", "Accept"]
)

# JWT setup
jwt = JWTManager()
db.init_app(app)
with app.app_context():
    db.create_all()
jwt.init_app(app)
migrate = Migrate(app, db)


@app.route('/swagger.json')
def swagger_spec():
    return jsonify(get_swagger_spec())


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})


# property routes
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
    required_fields = ['title', 'description', 'rent_price', 'location']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

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
    prop = db.session.get(Property, property_id)
    if not prop:
        return jsonify({"error": "Property not found"}), 404

    data = request.get_json()
    prop.title = data.get('title', prop.title)
    prop.description = data.get('description', prop.description)
    prop.location = data.get('location', prop.location)

    if 'rent_price' in data:
        try:
            prop.rent_price = float(data['rent_price'])
        except ValueError:
            return jsonify({"error": "Invalid rent price format"}), 400

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


# bookings routes
@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    tenant_id = data.get('tenant_id')
    property_id = data.get('property_id')
    start_date = data.get('start_date', datetime.utcnow().date())
    end_date = data.get('end_date', datetime.utcnow().date())

    if not all([tenant_id, property_id]):
        return jsonify({"error": "Missing required fields"}), 400

    # ✅ Check if tenant already booked this property (any status except cancelled)
    existing = Booking.query.filter_by(tenant_id=tenant_id, property_id=property_id).filter(Booking.status != "cancelled").first()
    if existing:
        return jsonify({"error": "You have already booked this property."}), 400

    new_booking = Booking(
        tenant_id=tenant_id,
        property_id=property_id,
        start_date=start_date,
        end_date=end_date,
        status="pending"
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


    result = []
    for b in bookings:
        b_dict = b.to_dict()
        property_obj = Property.query.get(b.property_id)
        if property_obj:
            b_dict['property'] = property_obj.to_dict()
        result.append(b_dict)

    return jsonify(result), 200



@app.route("/bookings/<int:id>", methods=["PUT"])
def update_booking_status(id):
    data = request.get_json()
    status = data.get("status", "").lower()
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

    landlord_id = int(landlord_id)  # direct cast

    bookings = (
        Booking.query.join(Property)
        .filter(Property.landlord_id == landlord_id)
        .all()
    )

    return jsonify([b.to_dict() for b in bookings]), 200


# payment routes
@app.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    data = request.get_json()
    booking_id = data.get('booking_id')
    payment_method = data.get('payment_method', 'digital_wallet')
    amount = data.get('amount')

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking.status != "approved":
        return jsonify({"error": "Booking must be approved before payment"}), 400

    tenant_id = booking.tenant_id
    landlord_id = booking.prop.landlord_id  # make sure your Booking model has a relationship to Property

    transaction_id = f"TXN-{datetime.utcnow().timestamp()}"
    payment = Payment(
        booking_id=booking_id,
        tenant_id=tenant_id,
        landlord_id=landlord_id,
        amount=amount,
        payment_method=payment_method,
        transaction_id=transaction_id,
        status="completed",
        paid_at=datetime.utcnow()
    )

    # ✅ Update booking status to "active" immediately
    booking.status = "active"

    db.session.add(payment)
    db.session.commit()
    return jsonify({
        "message": "Payment successful",
        "payment": payment.to_dict(),
        "booking_status": booking.status
    }), 201




@app.route('/payments', methods=['GET'])
@jwt_required()
def get_payments():
    user_id = get_jwt_identity()
    role = request.args.get("role", "tenant")

    if role == "tenant":
        payments = Payment.query.filter_by(tenant_id=user_id).all()
    else:
        payments = Payment.query.filter_by(landlord_id=user_id).all()

    return jsonify([p.to_dict() for p in payments]), 200


@app.route('/payments/<int:id>', methods=['PUT'])
@jwt_required()
def update_payment(id):
    data = request.get_json()
    status = data.get("status", "completed")

    payment = Payment.query.get(id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    allowed = ["pending", "completed", "failed", "refunded"]
    if status not in allowed:
        return jsonify({"error": f"Invalid status. Must be one of {allowed}"}), 400

    payment.status = status
    payment.paid_at = datetime.utcnow() if status == "completed" else None
    db.session.commit()
    return jsonify({"message": f"Payment updated to {status}", "payment": payment.to_dict()}), 200


# auth routes
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": user.to_dict()
        }), 200
    return jsonify({"error": "Invalid email or password"}), 401


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    role = data.get('role', 'tenant')
    if role not in ['admin', 'landlord', 'tenant']:
        return jsonify({"error": "Invalid role"}), 400

    new_user = User(name=data['name'], email=data['email'], role=role)
    new_user.password = data['password']
    db.session.add(new_user)
    db.session.commit()

    send_email(
    to_email=data['email'],
    subject="Welcome to RentEase 🎉",
    html_content=f"""
        <h2>Hello {data['name']},</h2>
        <p>Welcome to <strong>RentEase</strong>! Your account has been successfully created.</p>
        <p>Login anytime to explore rental properties.</p>
        <br/>
        <p>— The RentEase Team 🏡</p>
    """
)

    return jsonify({"message": "User registered successfully"}), 201


# admin routes
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


@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    to_email = data.get("to")
    subject = data.get("subject", "RentEase Notification")
    content = data.get("message", "This is a test email from RentEase.")

    message = Mail(
        from_email=os.getenv("SENDGRID_FROM_EMAIL"),
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return jsonify({"status": "success", "code": response.status_code}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
