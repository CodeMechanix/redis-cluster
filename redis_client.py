import redis
from rediscluster import RedisCluster

class RedisClusterClient:
    """
    This is a redis client. A wrapper over redis-py library.
    """
    def __init__(self,host,port):
        startup_nodes = [{"host": host, "port": port}]
        self.__redis_cluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    def redis_cluster(self):
        return self.__redis_cluster

    def set(self,key,value,ex,px,nx,xx):
        return self.__redis_cluster.set(key,value,ex,px,nx,xx)

    def get(self,key):
        return self.__redis_cluster.get(key)