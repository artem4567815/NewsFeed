import jwt
import uuid
from flask_jwt_extended import create_access_token

def get_refresh_token(response, cookie_name):
    """Custom function to extract refresh token from cookies"""
    cookie = response.cookies.get(cookie_name)
    if not cookie:
        raise ValueError(f"Cookie {cookie_name} not found in response")

    try:
        decoded = jwt.decode(
            cookie,
            options={"verify_signature": False},  # Для тестов подпись не проверяем
            algorithms=["HS256"]
        )
        csrf_token = decoded.get("csrf")
    except Exception as e:
        return {"JWT decoding failed": str(e)}

    return {"refresh_token": cookie,
            "csrf_token": csrf_token}

def generate_invalid_user_jwt():
    """Generate JWT token with non-existent UUID for testing"""
    # Генерируем новый UUID, который гарантированно не существует в базе
    non_existent_uuid = str(uuid.uuid4())

    access_token = create_access_token(identity=non_existent_uuid,
                                       additional_claims={"user_id": non_existent_uuid, "is_admin": False})

    
    return access_token
