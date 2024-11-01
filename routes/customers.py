from flask import Blueprint, jsonify

customers_blueprint = Blueprint('customers', __name__)

@customers_blueprint.route('/', methods=['GET'])
def get_customer_growth_data():
    # Data yang akan dikirim ke frontend
    data = {
        "labels": ['January', 'February', 'March', 'April', 'May'],
        "growth": [40, 30, 20, 25, 15]  # Contoh data pertumbuhan pelanggan
    }
    return jsonify(data)
