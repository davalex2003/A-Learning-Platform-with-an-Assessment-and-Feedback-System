import json
import hmac
import hashlib

def get_hash_string(object):
    with open('configs/hash.json', 'r') as f:
        config = json.load(f)
        f.close()
    key = config['secret'].encode()
    hmac_object = hmac.new(key, object.encode(), hashlib.sha256)
    hex_dig = hmac_object.hexdigest()
    return hex_dig