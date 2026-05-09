import redis
import json

class Database:
    def __init__(self):
        try:
            self.r = redis.Redis(host='localhost', port=6379, db=0)
            self.r.ping()  # Test connection
            self.use_redis = True
        except redis.exceptions.ConnectionError:
            print("Redis not available, using in-memory storage.")
            self.use_redis = False
            self.employees = []
        self.initialize_dummy_data()
    
    def initialize_dummy_data(self):
        dummy_employees = [
            {"name": "John Doe", "hours": 40, "rate": 20, "deductions": 100, "tax_rate": 10, "bonus": 50, "net_salary": 650},
            {"name": "Jane Smith", "hours": 35, "rate": 25, "deductions": 150, "tax_rate": 15, "bonus": 75, "net_salary": 662.5}
        ]
        if self.use_redis:
            if not self.r.exists('employees'):
                for emp in dummy_employees:
                    self.r.rpush('employees', json.dumps(emp))
        else:
            self.employees.extend(dummy_employees)
    
    def save_employee(self, employee):
        if self.use_redis:
            self.r.rpush('employees', json.dumps(employee))
        else:
            self.employees.append(employee)
    
    def get_all_employees(self):
        if self.use_redis:
            employees = self.r.lrange('employees', 0, -1)
            return [json.loads(emp) for emp in employees]
        else:
            return self.employees
