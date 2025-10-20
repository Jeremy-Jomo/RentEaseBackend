from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, User, Property, Booking

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route('/test')
def test():
    return jsonify({"message": "This is a test endpoint."})


if __name__ == '__main__':
    app.run(debug=True)