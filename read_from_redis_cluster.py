from random import randrange
import os
import bootstrap
from redis_cluster_client import RedisClusterClient

bootstrap.boot()

total = 0

data = []

with open('data.txt', 'r') as f:
    for x in f:
        total += 1
        data.append(x.rstrip())

print(total)

redis_cluster = RedisClusterClient()

for x in range(int(os.getenv("TEST_COUNT"))):
    index = randrange(0,total)
    key = data[index]
    print(redis_cluster.get(key))