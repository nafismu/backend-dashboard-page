from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity
)
from models.users import User, db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.security import generate_password_hash
from utils.decorators import role_required
from datetime import timedelta

auth = Blueprint('auth', __name__)

# Login endpoint dengan refresh token
@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Cari user berdasarkan username
        user = User.query.filter_by(username=username).first()

        # Validasi user dan password
        if not user or not user.check_password(password):
            return jsonify({"msg": "Invalid credentials"}), 401

        # Generate access dan refresh token
        access_token = create_access_token(
            identity={"id": user.id, "role": user.role}, 
            expires_delta=timedelta(hours=1)  # Kedaluwarsa 1 jam
        )
        refresh_token = create_refresh_token(
            identity={"id": user.id, "role": user.role}, 
            expires_delta=timedelta(days=7)  # Kedaluwarsa 7 hari
        )

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role  # Kembalikan role user dalam response
        }), 200

    except SQLAlchemyError as e:
        return jsonify({"msg": "Database error", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"msg": "Something went wrong", "error": str(e)}), 500

# Endpoint untuk refresh token
@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Hanya menerima refresh token
def refresh_token():
    try:
        # Ambil data user dari refresh token
        current_user = get_jwt_identity()

        # Generate access token baru
        new_access_token = create_access_token(
            identity=current_user, 
            expires_delta=timedelta(hours=1)
        )

        return jsonify({"access_token": new_access_token}), 200
    except Exception as e:
        return jsonify({"msg": "Something went wrong", "error": str(e)}), 500

# Endpoint protected untuk admin
@auth.route('/admin', methods=['GET'])
@role_required('admin')
def admin_dashboard():
    return jsonify({"msg": "Welcome to the Admin Dashboard!"})

# Endpoint protected untuk employee
@auth.route('/employee', methods=['GET'])
@role_required('employee')
def employee_dashboard():
    return jsonify({"msg": "Welcome to the Employee Dashboard!"})
# def fetch_user_by_id(user_id):
#     return User.query.get(user_id)

# Endpoint untuk registrasi user
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({'message': 'Missing required fields'}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password_hash=hashed_password, role=role)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Username already exists'}), 409
    except Exception as e:
        return jsonify({'message': 'An error occurred during registration'}), 500
