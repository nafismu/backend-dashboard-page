# routes/CRUDemployees.py
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models.employees import Employee
from models.users import User
from models import db

inputEmployees_blueprint = Blueprint('CRUDemployees', __name__)

# Create (Add new employee)
@inputEmployees_blueprint.route('/', methods=['POST'])
@cross_origin()  # This will add CORS headers to this route
def create_employee():
    data = request.json
    new_employee = Employee(
        name=data.get('name'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        position=data.get('position')
    )
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"status": "employee created"}), 201


# Read (Fetch all employees)
@inputEmployees_blueprint.route('/', methods=['GET'])
def get_employees():
    employees = Employee.query.join(User, Employee.employee_id == User.id).all()
    employees_list = [{'id': e.id, 'employee_id': e.employee_id, 'phone': e.phone , 'email': e.email, 'address': e.address, 'position': e.position} for e  in employees]
    return jsonify(employees_list), 200

# Read (Fetch single employee by ID)
@inputEmployees_blueprint.route('/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify({'id': employee.id, 'employee_id': employee.employee_id, 'phone': employee.phone, 'email': employee.email, 'address': employee.address, 'position': employee.position}), 200

# Update (Modify existing employee by ID)
@inputEmployees_blueprint.route('/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    employee = Employee.query.get_or_404(id)
    employee.name = data.get('name')
    employee.phone = data.get('phone')
    employee.email = data.get('email')
    employee.address = data.get('address')
    employee.position = data.get('position')

    db.session.commit()

    return jsonify({'message': 'Employee updated successfully!'}), 200

# Delete (Remove employee by ID)
@inputEmployees_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()

    return jsonify({'message': 'Employee deleted successfully!'}), 200
