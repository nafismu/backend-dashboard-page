# utils/decorators.py
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from flask import jsonify
from models.users import User  # Pastikan ini mengarah ke model User yang benar

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            # Periksa apakah user memiliki role yang dibutuhkan
            if not user or user.role != required_role:
                return jsonify({"msg": "Access forbidden: role not permitted"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
