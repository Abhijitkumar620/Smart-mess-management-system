from datetime import datetime
from bson import ObjectId

class Attendance:
    COLLECTION = 'attendance'
    
    def __init__(self, mongo: PyMongo):
        self.db = mongo.db
    
    def mark_attendance(self, member_id: str, date: str, meals: list):
        """Mark attendance for member (QR scan or admin mark)"""
        att_date = datetime.strptime(date, '%Y-%m-%d')
        att_data = {
            'member_id': ObjectId(member_id),
            'date': att_date,
            'meals': meals,  # ['breakfast', 'lunch', 'dinner']
            'marked_at': datetime.utcnow(),
            'marked_by': None  # Will be set by admin or QR system
        }
        
        # Remove existing attendance for same date
        self.db[self.COLLECTION].delete_one({'member_id': ObjectId(member_id), 'date': att_date})
        
        result = self.db[self.COLLECTION].insert_one(att_data)
        return str(result.inserted_id)
