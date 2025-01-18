import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request
from models.salesperformance import salesPerformance
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Blueprint Flask
prediction_blueprint = Blueprint('prediction', __name__)

# Fungsi untuk melatih model menggunakan Random Forest
def train_model():
    # Mengambil data dari database
    data = salesPerformance.query.all()

    # Convert data ke list dictionary
    data_list = [
        {
            "F0_Lead": row.f0,
            "F1_Opportunity": row.f1,
            "F2_Proposal": row.f2,
            "F3_Bidding": row.f3,
            "F4_Negotiation": row.f4,
            "F5_Contract": row.f5,
        }
        for row in data
    ]

    # Convert ke DataFrame
    df = pd.DataFrame(data_list)

    # Fitur dan target
    X = df[["F0_Lead", "F1_Opportunity", "F2_Proposal", "F3_Bidding", "F4_Negotiation"]]
    y = df["F5_Contract"]

    # Split data menjadi training dan testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inisialisasi model Random Forest Regressor dengan pengaturan hyperparameter
    model = RandomForestRegressor(
        n_estimators=200,  # Jumlah pohon dalam hutan
        max_depth=10,      # Kedalaman maksimum setiap pohon
        min_samples_split=5,  # Jumlah minimum sampel untuk membagi node
        min_samples_leaf=2,   # Jumlah minimum sampel pada setiap daun
        random_state=42
    )

    # Train model
    model.fit(X_train, y_train)

    # Evaluasi model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return model, X, mse, r2

# Endpoint untuk training model
@prediction_blueprint.route('/train', methods=['POST'])
def train():
    model, X, mse, r2 = train_model()
    return jsonify({
        "message": "Model trained successfully using Random Forest",
        "metrics": {
            "Mean Squared Error (MSE)": mse,
            "R-squared (R2)": r2
        }
    })

# Fungsi untuk prediksi data di masa depan
def predict_sales(model, X, months):
    # Data dummy masa depan (buat secara acak dengan fitur yang sama)
    future_data = np.random.randint(100, 200, size=(months, X.shape[1]))
    future_df = pd.DataFrame(future_data, columns=X.columns)
    future_predictions = model.predict(future_df)
    return future_predictions.tolist()

# Endpoint untuk prediksi
@prediction_blueprint.route('/', methods=['GET'])
def predict():
    # Melatih model
    model, X, _, _ = train_model()

    # Mendapatkan jumlah bulan dari parameter query
    future_months = int(request.args.get('months', 3))

    # Prediksi penjualan
    sales_predictions = predict_sales(model, X, future_months)

    return jsonify({
        "message": "Prediction successful using Random Forest",
        "sales_predictions": sales_predictions
    })
