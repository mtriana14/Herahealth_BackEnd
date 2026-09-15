from app.config.db import db
from app.models import User
from flask import jsonify, Blueprint, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

users_bp = Blueprint('users', __name__)

# Simply prints all the users in the Users table
@users_bp.route('/getusers', methods=["GET"])
@jwt_required()
def get_users():
    """
    Get all users or a single user by ID
    ---
    tags:
      - User Management
    parameters:
      - in: query
        name: user_id
        type: integer
        description: Omit to return all users
    responses:
      200:
        description: User record(s)
      404:
        description: No users found
    """
    user_id = request.args.get("user_id")
    current_user_id = int(get_jwt_identity())
    is_admin = get_jwt().get('role') == 'admin'

    if user_id:
        try:
            requested_user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'user_id must be an integer'}), 400
        if not is_admin and requested_user_id != current_user_id:
            return jsonify({'error': 'Forbidden'}), 403
        users = User.query.filter_by(user_id=requested_user_id).all()
    elif is_admin:
        users = User.query.all()
    else:
        users = User.query.filter_by(user_id=current_user_id).all()

    if not users:
        return jsonify({"Error":"No users found"}), 404

    return jsonify([{
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active,
        'last_login': user.last_login.isoformat() if user.last_login else None,
        'weight': float(user.weight) if user.weight is not None else None,
        'height': float(user.height) if user.height is not None else None,
        'phone': user.phone,
        'profile_photo': user.profile_photo,
        'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
        'gender': user.gender,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'updated_at': user.updated_at.isoformat() if user.updated_at else None,
    } for user in users]), 200

