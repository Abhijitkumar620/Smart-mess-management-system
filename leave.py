from datetime import datetime
from enum import Enum
from bson import ObjectId

class LeaveStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class LeaveRequest:
    COLLECTION = 'leaves'
    
    def __init__(self, mongo: PyMongo):
        self.db = mongo.db
    
    def submit_leave(self, member_id: str, start_date: str, end_date: str, reason: str):
        """Submit leave request"""
        leave_data = {
            'member_id': ObjectId(member_id),
            'start_date': datetime.strptime(start_date, '%Y-%m-%d'),
            'end_date': datetime.strptime(end_date, '%Y-%m-%d'),
            'reason': reason,
            'status': LeaveStatus.PENDING.value,
            'submitted_at': datetime.utcnow()
        }
        
        result = self.db[self.COLLECTION].insert_one(leave_data)
        return str(result.inserted_id)
    
    def approve_leave(self, leave_id: str, admin_id: str):
        """Admin approves leave request"""
        result = self.db[self.COLLECTION].update_one(
            {'_id': ObjectId(leave_id)},
            {
                '$set': {
                    'status': LeaveStatus.APPROVED.value,
                    'approved_by': ObjectId(admin_id),
                    'approved_at': datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
