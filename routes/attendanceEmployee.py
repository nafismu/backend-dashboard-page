from flask import Flask, request, jsonify,Blueprint
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from config import Config
# import face_recognition
import numpy as np
import base64
import re
from io import BytesIO
from PIL import Image
from models import db
from models.verifyFace import verifyFace
from models.attendance import Attendance
import locale
import os
import base64
import cv2
from werkzeug.utils import secure_filename
from utils import eigenface  # Helper untuk pemrosesan wajah

UPLOAD_FOLDER = "./uploads/profile_pictures/"
TEMP_UPLOAD_FOLDER = "./uploads/profile_pictures/temp"
# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

recognizer = eigenface.EigenfaceRecognizer()
attendanceEmployee_blueprint = Blueprint('attendanceEmployee', __name__)

def base64_to_image(base64_string):
    # Hapus header data:image jika ada
    if 'data:image' in base64_string:
        base64_string = re.sub('^data:image/.+;base64,', '', base64_string)
    
    # Decode base64 ke bytes
    image_bytes = base64.b64decode(base64_string)
    
    # Konversi bytes ke image
    image = Image.open(BytesIO(image_bytes))
    return np.array(image)
def prepare_training_data():
    """
    Fungsi untuk mempersiapkan data pelatihan dari database.
    Gambar diambil dari path yang tersimpan di tabel VerifyFace.
    """
    images = []
    labels = []

    # Query semua data dari tabel VerifyFace
    users = verifyFace.query.all()
    name = request.form.get("name")

    for user in users:
        # Cek apakah nama sesuai dengan request
        if user.name == name:
            img_path = user.image_path  # Ambil path gambar
            label = user.id  # Ambil id user sebagai label

            # Pastikan file gambar ada
            if os.path.exists(img_path):
                # Baca gambar dalam grayscale
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

                # Tambahkan gambar dan label ke daftar
                images.append(image)
                labels.append(label)

    return images, labels
@attendanceEmployee_blueprint.route('/verify-face', methods=['POST'])
@cross_origin()
def verify_face():
    try:
        # Ambil data dari request
        name = request.form.get("name")
        base64image = request.form.get("image")
        file = request.files.get('image')

        # Validasi input
        if not base64image and not file:
            return jsonify({"error": "Profile picture is required"}), 400

        # Buat folder sementara jika belum ada
        if not os.path.exists(TEMP_UPLOAD_FOLDER):
            os.makedirs(TEMP_UPLOAD_FOLDER)

        # Simpan gambar sementara
        if base64image:
            # Jika input berupa base64
            image = base64_to_image(base64image)
            image_filename = f"{name}_{datetime.now().strftime('%d-%m-%Y-%H-%M')}.jpg"
            temp_path = os.path.join(TEMP_UPLOAD_FOLDER, image_filename)
            Image.fromarray(image).save(temp_path)  # Konversi array ke gambar
        elif file:
            # Jika input berupa file
            image_filename = f"{name}_{datetime.now().strftime('%d-%m-%Y-%H-%M')}.jpg"
            temp_path = os.path.join(TEMP_UPLOAD_FOLDER, image_filename)
            file.save(temp_path)
        
        # Baca gambar untuk prediksi
        test_image = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)
        if test_image is None:
            os.remove(temp_path)
            return jsonify({"error": "Invalid or unreadable image"}), 400

        # Muat data pelatihan
        training_images, training_labels = prepare_training_data()
        if not training_images or not training_labels:
            os.remove(temp_path)
            return jsonify({"success": False, "error": "No training data available"}), 400

        # Latih model
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # Gunakan recognizer LBPH
        recognizer.train(training_images, np.array(training_labels))

        # Lakukan prediksi
        predicted_label, confidence = recognizer.predict(test_image)

        # Jika confidence di atas 20, kembalikan gagal
        if confidence > 20:
            os.remove(temp_path)
            return jsonify({"success": False, "error": "Face verification failed due to high confidence value", "confidence": confidence}), 400

        # Ambil data pengguna berdasarkan label
        user = verifyFace.query.filter_by(id=predicted_label).first()
        if not user:
            os.remove(temp_path)
            return jsonify({"success": False, "error": "No matching user found"}), 404

        # Simpan data ke tabel attendance
        new_attendance = Attendance(employee_id=user.id, confidence=confidence, timestamp=datetime.now())
        db.session.add(new_attendance)
        db.session.commit()

        # Hapus file sementara
        os.remove(temp_path)

        # Kembalikan respons sukses
        return jsonify({
            "success": True,
            "message": f"Face verified successfully for user: {user.name}",
            "user": {
                "id": user.id,
                "name": user.name,
                "role": user.role,
                "image_path": user.image_path
            },
            "attendance": {
                "employee_id": new_attendance.employee_id,
                "confidence": new_attendance.confidence,
                "timestamp": new_attendance.timestamp
            },
            "confidence": confidence
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500

@attendanceEmployee_blueprint.route('/register', methods=['POST'])
@cross_origin()
def register():
    # print(request.form)
    # Ambil data dari form
    name = request.form.get("name")
    role = request.form.get("role")
    base64image = request.form.get("image")
    file = request.files.get('image')

    # Validasi input
    if not name or not role:
        return jsonify({"error": "Name and role are required"}), 400
    if not base64image:
        return jsonify({"error": "Profile picture is required"}), 400

    # Pastikan folder untuk menyimpan gambar ada
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Konversi gambar dari base64
    image = base64_to_image(base64image)

    # Simpan gambar dengan nama unik berdasarkan nama dan role
    image_filename = f"{name}_{role}_{datetime.now().strftime('%d-%m-%Y-%H-%M')}.jpg"
    image_path = os.path.join('./uploads/profile_pictures', image_filename)
    img = Image.fromarray(image)
    img.save(image_path)

    # Jika file gambar juga diunggah, simpan file tersebut
    if file:
        filename = f"{name.replace(' ', '')}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

    # Simpan informasi pengguna ke database
    user = verifyFace(name=name, role=role, image_path=image_path)
    db.session.add(user)
    db.session.commit()

    # Return respons sukses
    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "role": user.role,
        }
    }), 201
