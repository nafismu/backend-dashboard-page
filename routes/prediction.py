from flask import Blueprint, jsonify, request
from models.prediction_model import predict_sales, predict_customers

prediction_blueprint = Blueprint('prediction', __name__)

@prediction_blueprint.route('/', methods=['GET'])
def predict():
    future_months = int(request.args.get('months', 3))  # Default prediksi 3 bulan ke depan
    
    # Prediksi penjualan dan pelanggan
    sales_predictions = predict_sales(future_months)
    customer_predictions = predict_customers(future_months)
    
    return jsonify({
        "sales": sales_predictions,
        "customers": customer_predictions
    })
