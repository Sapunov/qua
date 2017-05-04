from redis import StrictRedis

from qua import settings


def create_redis_client(host, port, db):

    return StrictRedis(host=host, port=port, db=db)


class Redis:

    def __init__(
            self, host=settings.REDIS['host'], port=settings.REDIS['port'],
            db=settings.REDIS['db_cache']):

        self.client = create_redis_client(host, port, db)

    def set(self, name, value, *args, **kwargs):

        return self.client.set(name, value, *args, **kwargs)

    def get(self, name, *args, **kwargs):

        return self.client.get(name, *args, **kwargs)

    def keys(self, *args, pattern="*", **kwargs):

        return self.client.keys(pattern, *args, **kwargs)

    def delete(self, keys, **kwargs):

        return self.client.delete(*keys, **kwargs)

    def exists(self, key):

        return self.client.exists(key)
