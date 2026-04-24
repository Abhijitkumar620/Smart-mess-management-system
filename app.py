from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mess_system')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-prod')
app.config['BASE_FEE'] = float(os.getenv('BASE_FEE', 3000))

mongo = PyMongo(app)
jwt = JWTManager(app)
CORS(app)

# Import models and routes
from models.user import User
from models.leave import LeaveRequest
from models.billing import Billing
from routes.auth import auth_bp
from routes.member import member_bp


app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(member_bp, url_prefix='/api/member')


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
