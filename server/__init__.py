# from flask import Flask, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# import os

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)

#     # Configuration
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///rentease.db')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

#     # Initialize extensions
#     db.init_app(app)
#     CORS(app)

#     # Basic route
#     @app.route('/')
#     def home():
#         return jsonify({
#             'message': 'RentEase Backend API is running! 🚀',
#             'status': 'success',
#             'database': 'connected'
#         })

#     @app.route('/health')
#     def health():
#         return jsonify({
#             'status': 'healthy',
#             'database': 'connected'
#         })

#     # Register blueprints/routes here when you create them
#     # Example:
#     # from server.routes import main_bp
#     # app.register_blueprint(main_bp)

#     with app.app_context():
#         db.create_all()

#     return app