from rediscluster import RedisCluster


class RedisClusterClient:
    """
    This is a cluster client. A wrapper over cluster-py library.
    """
    def __init__(self):
        startup_nodes = [
            {"host": "127.0.0.1", "port": 7000},
            {"host": "127.0.0.1", "port": 7001},
            {"host": "127.0.0.1", "port": 7002},
        ]

        # Note: decode_responses must be set to True when used with python3
        redis_cluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

        if redis_cluster is None:
            print("Could not connect to redis cluster.Exiting.")
            exit(1)

        self.__redis_cluster = redis_cluster

    def instance(self):
        return self.__redis_cluster

    def set(self,key,value,ex,px,nx,xx):
        return self.__redis_cluster.set(key,value,ex,px,nx,xx)

    def get(self,key):
        return self.__redis_cluster.get(key)