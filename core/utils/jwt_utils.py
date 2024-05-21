import jwt

SECRET_KEY = '&^%-st5r0p4s92%5y-8mx(*)(*)63&521()&iv__$bm!+s0y2h'


def jwt_encode(json_data):
    try:
        return jwt.encode(json_data, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        print(f"JWT Encode exception {e}")
        return None


def jwt_decode(encoded_jwt):
    try:
        return jwt.decode(encoded_jwt, SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        print(f"JWT Decode exception {e}")
        return None
