from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.leave import LeaveRequest
from models.billing import Billing
from utils.decorators import role_required

member_bp = Blueprint('member', __name__)
leave_model = None
billing_model = None

def init_models(mongo):
    global leave_model, billing_model
    leave_model = LeaveRequest(mongo)
    billing_model = Billing(mongo)

@member_bp.route('/leave', methods=['POST'])
@jwt_required()
@role_required('member')
def submit_leave():
    try:
        identity = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['start_date', 'end_date', 'reason']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        leave_id = leave_model.submit_leave(
            identity['id'],
            data['start_date'],
            data['end_date'],
            data['reason']
        )
        
        return jsonify({'message': 'Leave request submitted', 'leave_id': leave_id}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@member_bp.route('/billing/current', methods=['GET'])
@jwt_required()
@role_required('member')
def get_current_bill():
    try:
        identity = get_jwt_identity()
        bill = billing_model.calculate_monthly_bill(identity['id'])
        return jsonify(bill), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
