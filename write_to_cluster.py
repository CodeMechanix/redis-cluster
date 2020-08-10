from bootstrap import load_env
from redis_cluster_client import RedisClusterClient
from faker import Faker
import uuid
import os


# from multiprocessing import Process

# an unique id as the key for redis
def get_random_number():
    return uuid.uuid4().hex[:6].upper()


# the actual worker that is writing to redis
def worker(redis_cluster_client, faker_client, data, single_worker_limit):
    for x in range(single_worker_limit):
        unique_id = get_random_number()
        name = faker_client.name()
        redis_cluster_client.instance().set(unique_id, name)
        data.append(unique_id)
        print("{0} | uuid : {1} | {2}".format(x, unique_id, name))


# write data to a database (file for this demo)
def save_data(data_source):
    print("Saving data to ")
    with open('data.txt', 'w') as f:
        for item in data_source:
            f.write("%s\n" % item)


# bootstrap app.
# enables support for environment variables via .env file
load_env()

# create new redis cluster client instance
redis_cluster = RedisClusterClient()

db_data = []

faker = Faker()

single_worker_handles = int(os.getenv("SINGLE_WORKER_HANDLES"))

counter = int(os.getenv("COUNTER"))

for x in range(counter):
    worker(redis_cluster_client=redis_cluster,
           faker_client=faker,
           data=db_data,
           single_worker_limit=single_worker_handles)

save_data(data_source=db_data)

print("[+] -------------- Done ----------------")

