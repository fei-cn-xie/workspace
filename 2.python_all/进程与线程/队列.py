# QUEUE：
# FIFO
from multiprocessing import Queue

#######################
# put和get
# region
# 1. 如果queue满了，put会阻塞

# q1 = Queue(2)
# q1.put(1)
# print(q1)
# q1.put(2)
# print(q1)
# q1.put(3) # 阻塞
# print(q1)


# 2. 如果queue满了, 在put时设置了timeout, 超过timeout就会抛出异常
# q2 = Queue(maxsize=1)
# q2.put(1, timeout=2)
# print("test2", q1)
# q2.put(2, timeout=2) # 2s
# print("test2", q1)

# 3. 如果queue满了，put_nowait()会直接抛出异常，等价于put(block=False)
# q3 = Queue(maxsize=1)
# q3.put(1, block=False)
# q3.put(2, block=False)

# q3.put_nowait(1)
# q3.put_nowait(2)

# endregion

#######################
## 进程间通信
from multiprocessing import Process
import time
def test1(queue):
    while True:
        print(f"test1 get {queue.get()}")
        time.sleep(1)
        

def test2(queue):
    while(True):
        print(f"test2 get {queue.get()}")
        time.sleep(1)

        
if __name__ == "__main__":
    print("============== start")
    q = Queue(3)
    p1 = Process(target=test1, args=(q,))
    p2 = Process(target=test2, args=(q,))

    p1.start()
    p2.start()
    q.put(1)
    q.put(2)
    q.put(3)
    q.put(4)
