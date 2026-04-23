from datetime import datetime
from dateutil.relativedelta import relativedelta
from bson import ObjectId

class Billing:
    COLLECTION = 'billing'
    
    def __init__(self, mongo: PyMongo):
        self.db = mongo.db
    
    def calculate_monthly_bill(self, member_id: str, base_fee: float = 3000, current_month: str = None):
        """Calculate monthly bill with leave deductions"""
        if not current_month:
            current_month = datetime.utcnow().strftime('%Y-%m')
        
        # Get approved leaves for the month
        leaves = self.db.leaves.find({
            'member_id': ObjectId(member_id),
            'status': 'approved',
            'start_date': {'$gte': datetime.strptime(f'{current_month}-01', '%Y-%m-%d')}
        })
        
        total_leave_days = sum((leave['end_date'] - leave['start_date']).days + 1 for leave in leaves)
        daily_rate = base_fee / 30  # Assuming 30-day month
        deduction = total_leave_days * daily_rate
        
        bill_amount = max(0, base_fee - deduction)
        
        # Update member's profile
        self.db.users.update_one(
            {'_id': ObjectId(member_id)},
            {'$set': {'profile.current_month_bill': bill_amount}}
        )
        
        # Create billing record
        bill_data = {
            'member_id': ObjectId(member_id),
            'month': current_month,
            'base_fee': base_fee,
            'leave_days': total_leave_days,
            'deduction': deduction,
            'final_amount': bill_amount,
            'generated_at': datetime.utcnow()
        }
        
        result = self.db[self.COLLECTION].insert_one(bill_data)
        return {
            'bill_id': str(result.inserted_id),
            'base_fee': base_fee,
            'leave_days': total_leave_days,
            'deduction': deduction,
            'final_amount': bill_amount
        }
