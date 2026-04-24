from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from utils.decorators import role_required
from utils.security import hash_password

auth_bp = Blueprint('auth', __name__)
user_model = None

def init_models(mongo):
    global user_model
    user_model = User(mongo)

@auth_bp.route('/register', methods=['GET' , 'POST'])
def register():
    try:
        data = request.get_json() or {} 
        
        # Validation
        required_fields = ['email', 'password', 'name', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user exists
        if user_model.db.users.find_one({'email': data['email'].lower()}):
            return jsonify({'error': 'Email already registered'}), 409
        
        user_id = user_model.create_user(
            data['email'], 
            data['password'], 
            data['role'], 
            data['name'],
            data.get('phone', '')
        )
        
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        user_data = user_model.authenticate(data['email'], data['password'])
        if not user_data:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user_data)
        
        return jsonify({
            'access_token': access_token,
            'user': user_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
