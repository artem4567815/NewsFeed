import jwt


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
