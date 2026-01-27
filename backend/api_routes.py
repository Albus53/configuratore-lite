from flask import Blueprint, request, jsonify
from firebase_admin import auth
from models import db, User

api = Blueprint('api', __name__)

@api.route("/profile", methods=["GET"])
def get_profile():
    """
    Fetches the user profile. 
    Implements 'Lazy Sync': if the user exists in Firebase but not in SQL, 
    it creates the record locally on the fly.
    """
    
    # Auth Check
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization Header"}), 401
    
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email", "")
    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Database Sync
    user = User.query.filter_by(firebase_uid=uid).first()

    if not user:
        # Create new user if not found
        username = email.split("@")[0] if "@" in email else "user"
        new_user = User(
            firebase_uid=uid,
            email=email,
            username=username,
            role="client"
        )
        db.session.add(new_user)
        db.session.commit()
        user = new_user

    return jsonify({
        "message": "Success",
        "user": {
            "id": user.id,
            "uid": user.firebase_uid,
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    }), 200