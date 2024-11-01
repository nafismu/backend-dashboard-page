from flask import Blueprint, jsonify

sales_blueprint = Blueprint('sales', __name__)

@sales_blueprint.route('/', methods=['GET'])
def get_sales_data():
    # Data yang diambil dari model atau database
    data = {
        "labels": ['Category A', 'Category B', 'Category C', 'Category D'],
        "sales": [20, 30, 40, 50]  # Contoh data penjualan
    }
    return jsonify(data)
