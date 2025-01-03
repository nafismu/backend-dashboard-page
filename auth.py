# routes/auth.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from models.users import User,db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from werkzeug.security import generate_password_hash
from utils.decorators import role_required

auth = Blueprint('auth', __name__)

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

        # Buat access token dengan ID user sebagai identity
        access_token = create_access_token(identity=user.id)

        # Cek role user (admin atau employee)
        return jsonify({
            "access_token": access_token,
            "role": user.role  # Kembalikan role user dalam response
        }), 200

    except SQLAlchemyError as e:
        # Handle error dari database
        return jsonify({"msg": "Database error", "error": str(e)}), 500
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

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # Check if all fields are provided
    if not username or not password or not role:
        return jsonify({'message': 'Missing required fields'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create new user
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