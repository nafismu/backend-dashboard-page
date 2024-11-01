import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Contoh data penjualan dan pelanggan
data = {
    'month': ['January', 'February', 'March', 'April', 'May'],
    'sales': [15000, 18000, 17000, 16000, 20000],
    'customers': [50, 55, 53, 60, 58]
}

df = pd.DataFrame(data)

# Model untuk prediksi penjualan
sales_model = LinearRegression()
X_sales = np.arange(len(df['sales'])).reshape(-1, 1)  # Menjadikan bulan sebagai fitur
y_sales = df['sales']
sales_model.fit(X_sales, y_sales)

# Model untuk prediksi pertumbuhan pelanggan
customer_model = LinearRegression()
X_customers = np.arange(len(df['customers'])).reshape(-1, 1)
y_customers = df['customers']
customer_model.fit(X_customers, y_customers)

def predict_sales(future_months):
    future_X = np.arange(len(df['sales']), len(df['sales']) + future_months).reshape(-1, 1)
    return sales_model.predict(future_X).tolist()

def predict_customers(future_months):
    future_X = np.arange(len(df['customers']), len(df['customers']) + future_months).reshape(-1, 1)
    return customer_model.predict(future_X).tolist()
