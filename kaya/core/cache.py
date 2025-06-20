import redis
import json

redis_client = redis.Redis(host='redis', port=6379, db=0)

def set_cache(key, data, ttl=600):
    json_data = json.dumps(data)
    redis_client.setex(key, ttl, json_data)  # set with expiry (TTL)

def get_cache(key):
    value = redis_client.get(key)
    if value is None:
        return None
    return json.loads(value)

def delete_cache(key):
    redis_client.delete(key)