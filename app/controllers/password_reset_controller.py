from app.models.user import User
from flask import jsonify, request
from app.config.db import db
from flask_jwt_extended import get_jwt_identity
import bcrypt

def forgot_password_reset():
    """
    Reset password by email (no token required)
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
              description: The new password to set
    responses:
      200:
        description: Password reset successfully
      400:
        description: Missing email or password
      404:
        description: No account with that email
    """
    # Password recovery needs a verified, single-use token delivered out of band.
    # Until email delivery is configured, fail safely instead of accepting an
    # email address and a replacement password from an unauthenticated caller.
    return jsonify({
        'error': 'Password recovery is temporarily unavailable. Contact support.'
    }), 501

def reset_password():
    """
    Change password while logged in
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - old_password
            - new_password
          properties:
            old_password:
              type: string
            new_password:
              type: string
    responses:
      200:
        description: Password changed successfully
      401:
        description: Old password is incorrect
    """
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    data = request.get_json(silent=True) or {}
    old_pass = data.get('old_password') or ''
    if not bcrypt.checkpw(old_pass.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'error': 'Invalid password'}), 401
    new_pass = data.get('new_password') or ''
    if len(new_pass) < 8:
        return jsonify({'error': 'New password must be at least 8 characters'}), 400
    hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password = hashed
    db.session.commit()
    return jsonify({"Success":f"Password reset for {user.email}"}), 200

    
