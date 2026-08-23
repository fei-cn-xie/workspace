# 
from collections.abc import Callable
import time, os
from multiprocessing import Process
from threading import get_native_id, Thread
from typing import Any, Callable, Iterable, Mapping

# 1. 使用内置Thread创建线程
# region
# 定义一个speak函数，功能是每隔一秒说话1次，一共说10次
# 定义一个study函数，功能是每隔一秒学习1次，一共说15次
# def speak(lock):
    
#     for i in range(10):
#         with(lock):
#             print(f"speak [{i}] = [pid = {os.getpid()}], 【线程id = {get_native_id()}】")
#         time.sleep(1)

# def study(lock):
#     for i in range(15):
#         with lock:
#             print(f'Study [{i}] = [pid = {os.getpid()}], 【线程id = {get_native_id()}】')
#         time.sleep(1)
# # speak()
# # study()
# if __name__ == '__main__':
#     from threading import Thread
#     from threading import RLock # 线程锁

#     lock = RLock()

#     print("="*5, "start", "="*5)
#     print(f"当前main 进程id = {os.getpid()}")

#     t1 = Thread(target=speak, args=(lock,))
#     t2 = Thread(target=study, args=(lock,))

#     t1.start() # 操作系统开始处理
#     t2.start() 

#     print("="*5, "end", "="*5)



# endregion


# 2. 使用继承Thread类创建线程

class SpeakThread(Thread):

    def __init__(self, lock, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = (), kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.lock = lock

    def run(self) -> None:
        for i in range(10):
            with(lock):
                print(f"speak thread class [{i}] = [pid = {os.getpid()}], 【线程id = {get_native_id()}】")
            time.sleep(1)

class StudyThread(Thread):
    def __init__(self, lock, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = (), kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.lock = lock
    def run(self):
        for i in range(15):
            with self.lock:
                print(f'Study  thread class [{i}] = [pid = {os.getpid()}], 【线程id = {get_native_id()}】')
            time.sleep(1)
# speak()
# study()
if __name__ == '__main__':
    from threading import Thread
    from threading import RLock # 线程锁

    lock = RLock()

    print("="*5, "start", "="*5)
    print(f"当前main 进程id = {os.getpid()}")

    t1 = SpeakThread(lock)
    t2 = SpeakThread(lock)

    t1.start() # 操作系统开始处理
    t2.start() 

    print("="*5, "end", "="*5)















