from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson import ObjectId

class User:
    COLLECTION = 'users'
    
    def __init__(self, mongo: PyMongo):
        self.db = mongo.db
    
    def create_user(self, email: str, password: str, role: str = 'member', name: str = '', phone: str = ''):
        """Create new user with hashed password"""
        user_data = {
            'email': email.lower(),
            'password': generate_password_hash(password),
            'name': name,
            'phone': phone,
            'role': role,  # 'admin' or 'member'
            'is_active': True,
            'created_at': datetime.utcnow(),
            'profile': {
                'join_date': datetime.utcnow(),
                'total_leaves': 0,
                'current_month_bill': 0
            }
        }
        
        result = self.db[self.COLLECTION].insert_one(user_data)
        return str(result.inserted_id)
    
    def authenticate(self, email: str, password: str):
        """Authenticate user and return user data"""
        user = self.db[self.COLLECTION].find_one({'email': email.lower()})
        if user and check_password_hash(user['password'], password):
            return {
                'id': str(user['_id']),
                'email': user['email'],
                'name': user.get('name', ''),
                'role': user['role'],
                'is_active': user['is_active']
            }
        return None
    
    def get_user_by_id(self, user_id: str):
        """Get user by ID"""
        user = self.db[self.COLLECTION].find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
            return user
        return None
