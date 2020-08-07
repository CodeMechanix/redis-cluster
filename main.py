from redis_client import RedisClusterClient
import bootstrap
import os


bootstrap.boot()

print("welcome to " + os.getenv("APP_NAME"))

try :

    redis_client = RedisClusterClient(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT')
    )

    redis_client.set("hello","is world")

    print(redis_client.get('hello'),os.getenv("REDIS_PORT"))

except Exception as e:
    print(e)



