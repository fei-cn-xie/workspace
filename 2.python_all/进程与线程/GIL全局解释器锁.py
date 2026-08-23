# GIL(Global Interpreter Lock) 

# 无论CPU有多少个核心，在某一时刻，只允许进程中的一个线程去执行Python代码
import sys

print(sys.getswitchinterval())

# CPython解释器中的多线程模型，本质上是并发，而不是并行!(是快速切换，而不是同时进行)

def description():
    """
    | 对比维度 | GIL（Global Interpreter Lock）全局解释器锁 | Lock / RLock |
    |----------|---------------------------------------------|---------------|
    | **核心本质** | 解释器级别的强制限制 | 代码级别的逻辑约定 |
    | **谁来控制** | Python解释器：解释器自动加锁，遇到IO或超时自动释放。 | 程序员：需要写代码 `lock.acquire()` 和 `lock.release()` |
    | **保护对象** | 保护“解释器不崩”——维护引用计数、垃圾回收等底层结构的线程安全。 | 保护“数据不算错”——维护用户定义的变量、操作顺序等业务逻辑的完整性。 |
    | **作用范围** | 全局唯一：一个进程里只有一个GIL，管着所有线程。 | 按需创建：可以创建100把不同的锁，分别保护100个不同的业务逻辑。 |
    | **如果没有它** | Python解释器可能会崩溃。 | 售票场景下，两个人可能买到同一张车票。 |

    """

current = 20
from threading import current_thread
import time
def sale(lock):
    while True:
        global current
        with lock:
            if current >= 0:
                print(f"{current_thread()} sale the ticket {current}")
                current -= 1
            else:
                break
        time.sleep(0.3)

from threading import Thread, RLock
lock = RLock()
t1 = Thread(target=sale, args=(lock,))
t2 = Thread(target=sale, args=(lock,))
t3 = Thread(target=sale, args=(lock,))

t1.start()
t2.start()
t3.start()