from redis_client import RedisClusterClient
import bootstrap
import os


# TODO make a class for userland.
bootstrap.boot()

print("welcome to " + os.getenv("APP_NAME"))

try:

    redis_client = RedisClusterClient(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT')
    )

    redis_client.set("hello","is world")

    redis_client.get("hello")

except Exception as e:
    print(e)




