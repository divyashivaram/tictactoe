# from django.db import models
import redis
from django.conf import settings


class Redis():
    def __init__(self):
        self.redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                                port=settings.REDIS_PORT, db=0)

    def write(self, key, val):
        return self.redis_instance.set(key, val)

    def read(self, key):
        return self.redis_instance.get(key)

    def peek(self, key):
        return self.redis_instance.exists(key)
