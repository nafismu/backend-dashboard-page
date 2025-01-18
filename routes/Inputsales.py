# routes/CRUDemployees.py
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models.Inputsales import Inputsales
from models import db

Salesinput_blueprint = Blueprint('Inputsales', __name__)

@Salesinput_blueprint.route('/', methods=['POST'])
@cross_origin()  # This will add CORS headers to this route
def create_salesinput():
    data = request.json
    new_salesinput = Inputsales(
        name = data[0].get('name'),
        email = data[0].get('email'),
        stage = data[0].get('stage'),
        comments = data[0].get('comments')
    )
    db.session.add(new_salesinput)
    db.session.commit()

    return jsonify({"status": "Inputsales successfully created"}), 201


# Read (Fetch all employees)
@Salesinput_blueprint.route('/', methods=['GET'])
def get_salesinput():
    salesinput = Inputsales.query.all()
    inputsales_list = [{'id': e.id, 'name': e.name, 'email': e.email, 'stage': e.stage, 'comments': e.comments} for e in salesinput]
    return jsonify(inputsales_list), 200

# Read (Fetch single employee by ID)
# @Salesinput_blueprint.route('/<int:id>', methods=['GET'])
# def get_salesinput(id):
#     salesinput = Inputsales.query.get_or_404(id)
#     return jsonify({'id': salesinput.id, 'name': salesinput.name, 'email': salesinput.email, 'stage': employee.stage, 'comments': employee.comments}), 200

# # Update (Modify existing employee by ID)
# @inputEmployees_blueprint.route('/<int:id>', methods=['PUT'])
# def update_employee(id):
#     data = request.json
#     employee = Employee.query.get_or_404(id)
#     employee.name = data.get('name')
#     employee.phone = data.get('phone')
#     employee.email = data.get('email')
#     employee.address = data.get('address')
#     employee.position = data.get('position')

#     db.session.commit()

#     return jsonify({'message': 'Employee updated successfully!'}), 200

# Delete (Remove employee by ID)
@Salesinput_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_salesinput(id):
    salesinput = Inputsales.query.get_or_404(id)
    db.session.delete(salesinput)
    db.session.commit()

    return jsonify({'message': 'Sales input deleted successfully!'}), 200
