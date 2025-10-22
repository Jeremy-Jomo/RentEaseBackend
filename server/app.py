from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from config import Config
from models import db, User, Property, Booking
import cloudinary
import cloudinary.uploader
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime
import os


app = Flask(__name__)
app.config.from_object(Config)



jwt = JWTManager()



db.init_app(app)
jwt.init_app(app)


from models import User, Property, Booking


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



if __name__ == '__main__':
    app.run(debug=True)