from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db,User, Property, PropertyImage, PropertyAmenity, Booking, Payment, Review

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

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
        price=data['price'],
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
    prop.price = data.get('price', prop.price)
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


@app.route('/admin/bookings', methods=['GET'])
def get_all_bookings():

    bookings = Booking.query.all()
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

if __name__ == '__main__':
    app.run(debug=True)