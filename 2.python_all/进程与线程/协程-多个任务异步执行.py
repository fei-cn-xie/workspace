import asyncio

# 1. asyncio.create_task() -> Task
# region

# 定义一个协程函数
# async def work(n, delay):
#     print(f'work{n} start')
#     print(f'work{n} running.....')

#     # 模拟一个IO等待
#     await asyncio.sleep(3)
    
#     print(f'work{n} end')
#     return f'work{n} done'


# async def master():
#     print("master start")

#     # asyncio.create_task 会把一个协程对象包装成一个可被事件循环调度的任务，并注册到事件循环中-  返回Task对象 （对应前文 await后面可以是 Task Future 协程 等对象
#     task1 = asyncio.create_task(work(1,1))
#     task2 = asyncio.create_task(work(2,1))
#     task3 = asyncio.create_task(work(3,1))

#     # 多任务异步执行
#     res = await task1
#     print("res1", res)
#     res = await task2
#     print("res2", res)
#     res = await task3
#     print("res3", res)

    

#     print("master end")
#     return "master done"

# print("last", asyncio.run(master()))

# endregion


#################################################### 2. async.gather() -> Future
# region

# 定义一个协程函数
async def work(n, delay):
    print(f'work{n} start')
    print(f'work{n} running.....')

    # 模拟一个IO等待
    await asyncio.sleep(3)
    
    print(f'work{n} end')
    return f'work{n} done'


async def master():
    print("master start")

    # asyncio.create_task 会把一个协程对象包装成一个可被事件循环调度的任务，并注册到事件循环中-  返回Task对象 （对应前文 await后面可以是 Task Future 协程 等对象
    task1 = asyncio.create_task(work(1,1))
    task2 = asyncio.create_task(work(2,1))
    task3 = asyncio.create_task(work(3,1))

    # 多任务异步执行, gather可以接收 Task和协程对象
    res = await asyncio.gather(task1, task2, task3)
    print(f"res = {res}")

    print("master end")
    return "master done"

print("last", asyncio.run(master()))
# endregion