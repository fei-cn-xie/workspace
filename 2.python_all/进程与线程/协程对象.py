async def work():
    print("work start")
    print("work running......")
    print("word end")
    return "result of work"

# 调用协程函数，会获取一个协程对象

coroutine_object = work()
print("coroutine_object = ", coroutine_object)

import asyncio
# asyncio.run 方法做了3件事:
# 1.创建一个事件循环。
# 2.将收到的协程对象，包装成一个任务(task)，交给事件循环。
# 3.启动事件循环。
# 注意:asyncio.run 会阻塞当前线程, 直到任务执行完毕，并返回该任务 return的最终结果。
res = asyncio.run(coroutine_object)
print(res)