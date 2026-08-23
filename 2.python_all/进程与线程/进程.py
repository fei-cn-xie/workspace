import os
import time
from typing import Any

# 1. 获取进程 pid
# region
# print(os.getpid())
# print(os.getppid())
# endregion

#######################
# 2. 使用内置Process创建进程
# region
# 定义一个speak函数，功能是每隔一秒说话1次，一共说10次
# 定义一个study函数，功能是每隔一秒学习1次，一共说15次
# def speak():
#     for i in range(10):
#         print(f"speak [{i}] = [pid = {os.getpid()}]")
#         time.sleep(1)

# def study():
#     for i in range(15):
#         print(f'Study [{i}] = [pid = {os.getpid()}]')
#         time.sleep(1)
# # speak()
# # study()
# if __name__ == '__main__':

#     from multiprocessing import Process
#     p1 = Process(target=speak)
#     p2 = Process(target=study)

#     p1.start() # 操作系统开始处理
#     p2.start() 


# endregion

#########################################
# 3. Process 参数
# Process(group=None, target=None, name=None, args=(), kwargs={},*,damon=None)
# group: 默认值为None，应该始终为None，只是为了与threading.Thread兼容
# target: 子进程要执行的可调用对象（函数）
# name: 进程名称，None会自动分配名称
# args: 给target传入的参数
# kwargs: 给target传递的关键字参数
# *：后面的参数只能通过关键字参数传递，比如这里要传入damon只能Process(damon=xxx)
# damon: 标记进程是否为守护进程，取值为布尔值(默认为None，表示从创建方进程继承)

# region
# def speak(a=None, b=None):
#     for i in range(10):
#         print(f"speak 【{a}】【{b}】 [{i}] = [pid = {os.getpid()}]")
#         time.sleep(1)

# def study(c=None, d=None):
#     for i in range(15):
#         print(f'Study 【{c}】【{d}】 [{i}] = [pid = {os.getpid()}]')
#         time.sleep(1)
# # speak()
# # study()
# if __name__ == '__main__':

#     from multiprocessing import Process, current_process
#     p1 = Process(target=speak, args=('张三', '李四'))
#     p2 = Process(target=study, kwargs={"d": 'd tom', 'c': "c jerry"})
#     print("current_process = ", current_process().pid)
#     p1.start() # 操作系统开始处理
#     p2.start() 

# endregion


###########################################
# 4. Lock 进程锁， RLock
#    RLock可以多次上锁，上锁几次，释放几次
# from multiprocessing import Process, Lock, RLock

# region
# def speak(lock: RLock):
#     for i in range(10):
#         # 上锁：
#         lock.acquire()
#         print(f"{i}一", end="", flush=True)
#         print("二", end="", flush=True)
#         print("三", end="", flush=True)
#         print("四", end="\n", flush=True)

#         # 释放锁
#         lock.release()
#         time.sleep(1)

# def study(lock: RLock):
#     for i in range(15):
#         with lock:
#             print(f"{i}-A", end="", flush=True)
#             print("B", end="", flush=True)
#             print("C", end="", flush=True)
#             print("D", end="\n", flush=True)
#         time.sleep(1)
# # speak()
# # study()
# if __name__ == '__main__':

#     lock = RLock()
#     p1 = Process(target=speak, args=(lock,))
#     p2 = Process(target=study, args=(lock,))
#     p1.start() # 操作系统开始处理
#     p2.start() 

# endregion

##########################################
# 5. join 方法
#   5.1： p.join()不是让p进程等待，而是让执行p.join()这行代码的进程去等待
#   5.2： join()必须在start()之后
#   5.3:  p.join(time) 表示让执行这行代码的进程等待time秒，即p进程抢占time秒

from multiprocessing import Process, Lock, RLock

# region
# def speak(lock: RLock):
#     for i in range(10):
#         # 上锁：
#         lock.acquire()
#         print(f"{i}一", end="", flush=True)
#         print("二", end="", flush=True)
#         print("三", end="", flush=True)
#         print("四", end="\n", flush=True)

#         # 释放锁
#         lock.release()
#         time.sleep(1)

# def study(lock: RLock):
#     for i in range(15):
#         with lock:
#             print(f"{i}-A", end="", flush=True)
#             print("B", end="", flush=True)
#             print("C", end="", flush=True)
#             print("D", end="\n", flush=True)
#         time.sleep(1)
# # speak()
# # study()
# if __name__ == '__main__':

#     print("====== ====== ====== start")
#     lock = RLock()
#     p1 = Process(target=speak, args=(lock,))
#     p2 = Process(target=study, args=(lock,))
#     p1.start() # 操作系统开始处理

#     p1.join(5) # 抢占5秒
#     # p1.terminate() # 强行终止 p1
#     p2.start()
#     # p2.join()
#     print("====== ====== ====== end")

# endregion


########################################## 
# 6. 什么是守护进程?
    # 1.一种“依附于主进程存在的子进程”，一旦主进程结束，它就会被自动终止。
    # 2.简言之:主进程一死，守护进程必跟着死。
#守护进程的使用场景:
    # 1.后台监控类任务
    # 2.日志/统计/采样类任务
    # 3.辅助型“陪跑任务”
# 注意：
    # 1. 守护进程必须在start()之前
    # 2. 守护进程中不能再创建进程


# region

# def monitor():
#     while True:
#         try:
#             with open('2.python_all\\进程与线程\\log.txt', 'r', encoding='utf-8') as f:
#                 lines = sum(1 for _ in f)
#         except FileNotFoundError:
#             lines = 0

#         print(f"守护进程， lines = {lines}\r", end='', flush=True)

#         time.sleep(0.2)

# if __name__ == "__main__":
#     print(f"main Process ------------------ start")

#     p1 = Process(target=monitor, daemon=True)
#     p1.start()

#     with open('2.python_all\\进程与线程\\log.txt', 'a',encoding='utf-8') as f:
#         for i in range(10):
#             f.write(f"Line = {i} \n")
#             f.flush()
#             time.sleep(1)
#     print(f"\nmain Process ------------------ end")


# endregion


#########################################
# 7. 进程之间不共享变量

# region
# num = 100

# def test1(data):
#     global num
#     num += 10
#     data.append('test1')
#     print(f"test1 -> num = {num}, data = {data}, id(num) = {id(num)}, id(data) = {id(data)}")

# def test2(data ):
#     global num
#     num -= 10
#     data.append('test2')
#     print(f"test2 -> num = {num}, data = {data}, id(num) = {id(num)},  id(data) = {id(data)}")

# if __name__ == "__main__":
#     data = ['main']
#     print(f'mian -> num = {num}, data = {data}, id(num) = {id(num)},  id(data) = {id(data)}')
#     p1 = Process(target=test1, args=(data,))
#     p2 = Process(target=test2, args=(data,))
#     p1.start()
#     p1.join()
#     p2.start()
#     p2.join()
#     print(f'mian -> num = {num}, data = {data}, id(num) = {id(num)},  id(data) = {id(data)}')

# endregion

############################
# 8. 通过继承Process创建进程

# 如果直接调用Process.run方法，则就是单进程

from multiprocessing import Process
import time

class SpeakProcess(Process):
    def run(self):
        for i in range(10):
            print(f"Speak进程: 我在说话 {i}")
            time.sleep(1)

class StudyProcess(Process):
    def run(self):
        for i in range(15):
            print(f"Study进程: 我在学习 {i}")
            time.sleep(1)

if __name__ == "__main__":
    p1 = SpeakProcess()
    p2 = StudyProcess()

    p1.start()
    p2.start()



