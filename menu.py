from datetime import datetime
from bson import ObjectId

class Menu:
    COLLECTION = 'menu'
    
    def __init__(self, mongo: PyMongo):
        self.db = mongo.db
    
    def add_daily_menu(self, date: str, breakfast: str, lunch: str, dinner: str, admin_id: str):
        """Add daily menu for specific date"""
        menu_data = {
            'date': datetime.strptime(date, '%Y-%m-%d'),
            'meals': {
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner
            },
            'created_by': ObjectId(admin_id),
            'created_at': datetime.utcnow()
        }
        
        result = self.db[self.COLLECTION].insert_one(menu_data)
        return str(result.inserted_id)
    
    def get_menu_by_date(self, date: str):
        """Get menu for specific date"""
        menu_date = datetime.strptime(date, '%Y-%m-%d')
        menu = self.db[self.COLLECTION].find_one({'date': menu_date})
        if menu:
            menu['_id'] = str(menu['_id'])
            return menu
        return None
