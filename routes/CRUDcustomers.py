# routes/CRUDcustomers.py

from urllib import response
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models.customers import Customer
from models import db
from datetime import datetime
from sqlalchemy import func

inputCustomers_blueprint = Blueprint('CRUDcustomers', __name__)

# Create (Add new customer)
@inputCustomers_blueprint.route('/', methods=['POST'])
@cross_origin()  # This will add CORS headers to this route
def create_customer():
        data = request.json
        new_customer = Customer(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            subscription=data.get('subscription'),
            signup_date=datetime.strptime(data.get('signup_date'),'%Y-%m-%dT%H:%M')
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"status": "Customer created"}), 201


# Read (Fetch all customers)
@inputCustomers_blueprint.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customers_list = [{'id': c.id, 'name': c.name, 'email': c.email,'phone': c.phone,'subscription': c.subscription, 'signup_date': c.signup_date} for c in customers]
    return jsonify(customers_list), 200

# Read (Fetch single customer by ID)
@inputCustomers_blueprint.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({'id': customer.id, 'name': customer.name, 'email': customer.email,'phone': customer.phone,'subscription': customer.subscription, 'signup_date': customer.signup_date}), 200

# Update (Modify existing customer by ID)
@inputCustomers_blueprint.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    customer = Customer.query.get_or_404(id)
    customer.name = data.get('name')
    customer.email = data.get('email')
    customer.phone = data.get('phone')
    customer.subscription = data.get('subscription')
    signup_date_str = data.get('signup_date')
    if signup_date_str:
        customer.signup_date = datetime.strptime(signup_date_str, '%Y-%m-%dT%H:%M')

    db.session.commit()

    return jsonify({'message': 'Customer updated successfully!'}), 200

# Delete (Remove customer by ID)
@inputCustomers_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({'message': 'Customer deleted successfully!'}), 200


@inputCustomers_blueprint.route('/customer-count', methods=['GET'])
def get_total_customer_count():
    # Customer = Customer.query.all()
    customer_count = Customer.query.count()
    return jsonify({"total_customers": customer_count}), 200

# Endpoint untuk new customers (bulan ini)
@inputCustomers_blueprint.route('/new-customers', methods=['GET'])
def new_customers():
    current_month = datetime.now().strftime('%Y-%m')
    new_customers_count = db.session.query(Customer).filter(
        func.strftime('%Y-%m', Customer.signup_date) == current_month
    ).count()
    return jsonify({"new_customers": new_customers_count})

# Endpoint untuk returning customers
@inputCustomers_blueprint.route('/customers-return', methods=['GET'])
def returning_customers():
    returning_customers_count = db.session.query(Customer.email).group_by(Customer.email).having(func.count(Customer.email) > 1).count()
    return jsonify({"returning_customers": returning_customers_count})