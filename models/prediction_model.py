import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# Data dummy untuk training
data = {
    "Sales_ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "F0_Lead": [50, 70, 40, 100, 60, 80, 30, 90, 55, 65],
    "F1_Opportunity": [30, 40, 20, 80, 35, 60, 15, 70, 25, 30],
    "F2_Proposal": [20, 25, 10, 50, 18, 40, 8, 45, 12, 15],
    "F3_Bidding": [10, 15, 5, 30, 8, 20, 3, 25, 6, 7],
    "F4_Negotiation": [8, 12, 4, 25, 7, 15, 2, 18, 5, 6],
    "F5_Contract": [5, 8, 2, 20, 4, 12, 1, 15, 3, 4],
}

# Convert ke DataFrame
df = pd.DataFrame(data)

# Fitur yang digunakan untuk clustering
X = df[["F0_Lead", "F1_Opportunity", "F2_Proposal", "F3_Bidding", "F4_Negotiation"]]

# Melatih model K-Means
kmeans = KMeans(n_clusters=3, random_state=42)  # Tentukan 3 cluster
kmeans.fit(X)

# Tambahkan cluster hasil ke data
df["Cluster"] = kmeans.labels_

# Fungsi untuk prediksi sales berbasis cluster
def predict_sales(months):
    # Membuat data dummy untuk masa depan
    future_data = np.random.randint(30, 100, size=(months, X.shape[1]))
    
    # Convert data dummy ke DataFrame dengan nama kolom yang sama
    future_df = pd.DataFrame(future_data, columns=X.columns)
    
    # Menentukan cluster masa depan
    future_clusters = kmeans.predict(future_df)
    
    # Rata-rata jumlah kontrak (F5_Contract) per cluster
    cluster_means = df.groupby("Cluster")["F5_Contract"].mean()
    
    # Prediksi penjualan berdasarkan cluster
    predictions = [cluster_means[cluster] for cluster in future_clusters]
    return predictions


# Fungsi untuk prediksi pelanggan
def predict_customers(months):
    sales_predictions = predict_sales(months)
    customer_predictions = [round(sale * 5) for sale in sales_predictions]
    return customer_predictions
