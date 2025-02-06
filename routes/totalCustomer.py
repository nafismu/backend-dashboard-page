from flask import Blueprint, jsonify
from models.customers import Customer

get_customer_count_blueprint = Blueprint('get_customer_count', __name__)

@get_customer_count_blueprint.route('/', methods=['GET'])
def get_total_customer_count():
    Customer = Customer.query.all()
    customer_count = Customer.query.count()
    return jsonify({"count": customer_count}), 200


