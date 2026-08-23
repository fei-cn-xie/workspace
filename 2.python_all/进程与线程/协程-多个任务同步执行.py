import asyncio

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

    # 调用三次work函数，分别得到三个协程对象
    coroutine1 = work(1,1)
    coroutine2 = work(2,1)
    coroutine3 = work(3,1)

    # 多任务同步执行
    res1 = await coroutine1
    print(res1)
    res2 = await coroutine2
    print(res2)
    res3 = await coroutine3
    print(res3)

    print("master end")
    return "master done"

print("last", asyncio.run(master()))