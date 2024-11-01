import sqlite3
from flask import Flask, jsonify, request, Blueprint
from flask_cors import cross_origin
import numpy as np
from sklearn.linear_model import LinearRegression
from models import db
from models.salesperformance import salesPerformance 


salesPerformance_blueprint = Blueprint('sales_performance', __name__)
@salesPerformance_blueprint.route('/', methods=['GET'])
@cross_origin()
def get_sales_performance():
    data = salesPerformance.query.all()
    salesPerformance_list = [{'id': c.id, 'kode': c.kode, 'mitra': c.mitra, 'namaSA': c.namaSA, 'sph': c.sph, 'f0': c.f0, 'f1': c.f1, 'f2': c.f2, 'f3': c.f3, 'f4': c.f4, 'f5': c.f5, 'tanggal': c.tanggal} for c in data]
    return jsonify(salesPerformance_list), 200
    # data = [
    #     { "no": 1, "kode": "M001", "mitra": "PT. ABC", "namaSA": "Nama SA 1", "spm": 100, "f0": 10, "f1": 15, "f2": 20, "f3": 5, "f4": 8, "f5": 9 },
    #     { "no": 2, "kode": "M002", "mitra": "PT. CBA", "namaSA": "Nama SA 2", "spm": 200, "f0": 12, "f1": 13, "f2": 25, "f3": 7, "f4": 6, "f5": 10 },
    #     # Data lainnya
    # ]
    return jsonify(data)

@salesPerformance_blueprint.route('/prediction')
def sales_prediction():
    # Data dummy sebagai contoh (ganti dengan data dari database)
    data = salesPerformance.query.all()
    sales_data = [{'sph': item.sph, 'mitra': item.mitra}for item in data]

    # Mengonversi data ke array numpy
    X = np.array(range(len(sales_data))).reshape(-1, 1)  # misal index sebagai waktu
    y = np.array([item['sph'] for item in sales_data])

    # Model regresi linear
    model = LinearRegression()
    model.fit(X, y)

    # Prediksi 5 langkah ke depan
    future_X = np.array(range(len(sales_data), len(sales_data) + 5)).reshape(-1, 1)
    future_y = model.predict(future_X)

    # Hasil prediksi
    predictions = future_y.tolist()
    return jsonify(predictions=predictions)

# def connect_db():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row  # Ini mengembalikan hasil sebagai dict
#     return conn

# # Endpoint untuk menampilkan data yang difilter dan diurutkan dari tabel salesPerformance
# @app.route('/sales-performance', methods=['GET'])
# def get_sales_performance():
#     # Mengambil parameter dari query string
#     funnel = request.args.get('funnel')  # Misal "f0", "f1", dll.
#     start_date = request.args.get('start_date')
#     end_date = request.args.get('end_date')
#     sort_key = request.args.get('sort_key')  # Kolom yang digunakan untuk sorting
#     sort_direction = request.args.get('sort_direction', 'ascending')  # Default ascending

#     conn = connect_db()
#     cursor = conn.cursor()

#     # Base query
#     query = "SELECT * FROM salesPerformance WHERE 1=1"
#     params = []

#     # Filter berdasarkan funnel
#     if funnel:
#         query += f" AND {funnel} > 0"  # Misalkan funnel bernilai > 0 jika aktif

#     # Filter berdasarkan rentang tanggal
#     if start_date:
#         query += " AND tanggal >= ?"
#         params.append(start_date)
#     if end_date:
#         query += " AND tanggal <= ?"
#         params.append(end_date)

#     # Sorting berdasarkan kolom yang dipilih
#     if sort_key:
#         query += f" ORDER BY {sort_key} {'ASC' if sort_direction == 'ascending' else 'DESC'}"

#     # Jalankan query
#     cursor.execute(query, params)
#     rows = cursor.fetchall()

#     # Ubah hasil query menjadi list of dicts
#     sales_performance = [dict(row) for row in rows]

#     conn.close()
#     return jsonify(sales_performance)
