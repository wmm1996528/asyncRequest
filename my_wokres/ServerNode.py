import random, time, queue
from multiprocessing.managers import BaseManager

task_queue = queue.Queue()

result_queue = queue.Queue()

BaseManager.register('get_task_queue', callable=lambda: task_queue)
BaseManager.register('get_result_queue', callable=lambda: result_queue)

manager = BaseManager(address=('0.0.0.0', 8001), authkey=b'qiye')

manager.start()

task = manager.get_task_queue()
result = manager.get_result_queue()

for url in ['http://seputu.com/biji1/' + str(i) + '.html' for i in range(1, 76)]:
    print('put task %s ...' % url)
    task.put(url)

print('try get result...')
for i in range(100):
    if result.empty():
        print('result is %s. ' % result.get(timeout=10))

manager.shutdown()
