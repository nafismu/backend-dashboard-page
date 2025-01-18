from flask import Flask, request, jsonify,Blueprint
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import face_recognition
import numpy as np
import base64
import re
from io import BytesIO
from PIL import Image
from models import db
from models.verifyFace import verifyFace
import locale

locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
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

@attendanceEmployee_blueprint.route('/verify-face', methods=['POST'])
@cross_origin()
def verify_face():
    try:
        # Ambil gambar dari request
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({'success': False, 'message': 'No image provided'}), 400

        # Konversi base64 ke image
        input_image = base64_to_image(image_data)
        
        # Deteksi wajah dari input
        face_locations = face_recognition.face_locations(input_image)
        if not face_locations:
            return jsonify({'success': False, 'message': 'No face detected'}), 400
        
        # Dapatkan encoding wajah
        input_encoding = face_recognition.face_encodings(input_image, face_locations)[0]
        
        # Ambil semua employee dari database
        employee = verifyFace.query.all()
        
        for employee in employees:
            # Bandingkan dengan wajah yang tersimpan
            matches = face_recognition.compare_faces([employee.face_encoding], input_encoding)
            if matches[0]:
                # Jika cocok, simpan attendance
                attendance = Attendance(employee_id=employee.id)
                db.session.add(attendance)
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'name': employee.name,
                    'timestamp': attendance.timestamp.isoformat()
                })
        
        # Jika tidak ada yang cocok
        return jsonify({'success': False, 'message': 'Face not recognized'}), 404

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@attendanceEmployee_blueprint.route('/register', methods=['POST'])
@cross_origin()
def register_employee():
    try:
        data = request.json
        name = data.get('username')
        image_data = data.get('image')
        
        if not name or not image_data:
            return jsonify({'success': False, 'message': 'Name and image required'}), 400
            
        # Konversi base64 ke image
        input_image = base64_to_image(image_data)
        
        # Deteksi dan encode wajah
        face_locations = face_recognition.face_locations(input_image)
        if not face_locations:
            return jsonify({'success': False, 'message': 'No face detected'}), 400
            
        face_encoding = face_recognition.face_encodings(input_image, face_locations)[0]
        
        # Simpan ke database
        new_verifyface = verifyFace(name=name, face_encoding=face_encoding)
        db.session.add(new_verifyface)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Employee registered successfully',
            'id': new_verifyface.id,
            'name': new_verifyface.name,
            'date' : datetime.now().strftime("%A-%d-%m-%Y"),
        })
        
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 500
