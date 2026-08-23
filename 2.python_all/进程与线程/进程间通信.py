import time
# 1. 使用Queue进程间通信
# region
# from multiprocessing import Process
# import time
# def test1(queue):
#     while True:
#         print(f"test1 get {queue.get()}")
#         time.sleep(1)
        

# def test2(queue):
#     while(True):
#         print(f"test2 get {queue.get()}")
#         time.sleep(1)

        
# if __name__ == "__main__":
#     print("============== start")
#     q = Queue(3)
#     p1 = Process(target=test1, args=(q,))
#     p2 = Process(target=test2, args=(q,))

#     p1.start()
#     p2.start()
#     q.put(1)
#     q.put(2)
#     q.put(3)
#     q.put(4)
# endregion

#####################
# 2. 使用Pipe实现进程间通信
# Pipe()返回两个对象，一个是首端，一个是尾端
# 双向队列

# region
from multiprocessing import Process, Pipe

def test1(con1):
    for i in range(10):
        if(i < 6):
            con1.send(f"send from test1 = {i}")
        else:
            print(f"get from test1 <====> {con1.recv()}")
        time.sleep(1)

def test2(con2):
    for i in range(10):
        if (i < 6):
            print(f"get from test2 <====> {con2.recv()}")
        else:
            con2.send(f"send from test2 = {i}")


if __name__ ==  "__main__":
    conection1, conection2 = Pipe()


    p1 = Process(target=test1, args=(conection1,))
    p2 = Process(target=test2, args=(conection2,))

    p1.start()
    p2.start()


# endregion



