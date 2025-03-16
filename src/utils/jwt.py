import jwt
import json

def encode_data(data: dict) -> str:
    with open('configs/jwt.json', 'r') as f:
        config = json.load(f)
        f.close()
    return jwt.encode(data, config['secret'], algorithm='HS256')


def decode_data(jwt_token: str) -> dict:
    with open('configs/jwt.json', 'r') as f:
        config = json.load(f)
        f.close()
    try:
        return jwt.decode(jwt_token, config['secret'], algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return {}
