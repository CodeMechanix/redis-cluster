import bootstrap
from redis_cluster_client import RedisClusterClient
from faker import Faker
import uuid
import os
#from multiprocessing import Process

bootstrap.boot()


redis_cluster = RedisClusterClient()
faker = Faker()


def get_random_number():
    return uuid.uuid4().hex[:6].upper()


data = []

single_worker_handles = int(os.getenv("SINGLE_WORKER_HANDLES"))
counter = int(os.getenv("COUNTER"))
test_count = int(os.getenv("TEST_COUNT"))


def worker():
    for x in range(single_worker_handles):
        unique_id = get_random_number()
        name = faker.name()
        redis_cluster.instance().set(unique_id,name)
        data.append(unique_id)
        print("{0} | uuid : {1} | {2}".format(x,unique_id,name))

#
# def execute_in_parallel(*fns):
#     proc = []
#     for fn in fns:
#         p = Process(target=fn)
#         p.start()
#         proc.append(p)
#     for p in proc:
#         p.join()


for x in range(counter):
    worker()

print("[+] -------------- Done ----------------")

with open('data.txt', 'w') as f:
    for item in data:
        f.write("%s\n" % item)

#
# for x in range(test_count):
#     the_chosen_one = random.choice(data)
#
#     print("{0} => {1}".format(the_chosen_one,redis_cluster.get(the_chosen_one)))
#
#
# print("[+] End of the line.")