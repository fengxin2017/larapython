import queue
import sys
import threading
import time

sys.path.append('/larapy/venv/Lib/site-packages')

import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
client = redis.Redis(connection_pool=pool)
pipe = client.pipeline()

jobs = client.zrange('queue:default:delayed',0,-1,withscores=True)

print(jobs)

exit()
# 三个队列
# queue:default:delayed
# queue:default
# queue:reserved

client.zremrangebyrank('queue:default:delayed', 0, -1)
client.zremrangebyrank('queue:default', 0, -1)
client.zremrangebyrank('queue:reserved', 0, -1)

exit()

# 添加到延迟队列
client.zadd('queue:default:delayed',
            {
                'job1': int(time.time()) + 10,
                'job2': int(time.time()) + 10,
                'job3': int(time.time()) + 10,
                'job4': int(time.time()) + 10,
                'job5': int(time.time()) + 10,
                'job6': int(time.time()) + 15,
                'job7': int(time.time()) + 15,
                'job8': int(time.time()) + 15,
                'job9': int(time.time()) + 15,
                'job10': int(time.time()) + 15,
                'job11': int(time.time()) + 20,
                'job12': int(time.time()) + 20,
                'job13': int(time.time()) + 20,
                'job14': int(time.time()) + 20,
                'job15': int(time.time()) + 20,
                'job16': int(time.time()) + 20,
                'job17': int(time.time()) + 20
            })

exit()
time.sleep(2)

# 当前时间
now = int(time.time())

# 实时获取队列
l = client.zrangebyscore('queue:default:delayed', 0, now, withscores=True)

# 移除当前需要执行的队列任务到reserved
client.zremrangebyscore('queue:default:delayed', 0, now)

client.zadd('queue:reserved', dict(l))

print(client.zscan('queue:default:delayed')[1])

print(client.zscan('queue:reserved')[1])

exit()

l = client.zrange('queue:default', 0, -1, withscores=True, score_cast_func=int)

print(l)

exit()

client.setex('name', 3, 'foxriver')

time.sleep(4)

print(client.get('name'))

exit()
queue = queue.Queue()

for i in range(20):
    queue.put(i)


class MyThreading(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            print(self.queue.get())
            time.sleep(1)
            self.queue.task_done()


# def consumer():
#     while True:
#         print(q.get())
#         time.sleep(3)
#         q.task_done()


for i in range(3):
    threading = MyThreading(queue)
    threading.setDaemon(True)
    threading.start()

# for i in range(3):
#     t=threading.Thread(target=product,args=(i,))
#     t.start()

# for j in range(20):
#     t=threading.Thread(target=consumer,args=(j,))
#     t.start()

queue.join()

print('gewgwge')
