
# submit 提交任务
# region
# from concurrent.futures import ProcessPoolExecutor
# import os
# import time

# def work(n):
#     print(f'work正在执行{n}, pid = {os.getpid()}')
#     time.sleep(1)
#     return f"work执行完成-{n}"

# if __name__ == "__main__":
#     # 创建一个进程池执行器
#     print("==============start===============")
#     excutor = ProcessPoolExecutor(3)

#     # 使用submit提交任务
#     taskIds = [n for n in range(1, 8)]
#     print(f'taskids = {taskIds}')
    
#     futures = [excutor.submit(work, taskId).result() for taskId in range(1,8)]
#     # excutor.shutdown(wait=True) # 阻塞等待excutor所有任务执行完毕

#     print(futures)

#     print("==============end===============")

# endregion



###################
# 使用 as_completed 按照 完成顺序 获取结果

# region
# from concurrent.futures import ProcessPoolExecutor, as_completed
# import os
# import time

# def work(n):
#     print(f'work正在执行{n}, pid = {os.getpid()}')
#     time.sleep(n % 3)
#     return f"work执行完成-> {n}"

# if __name__ == "__main__":
#     # 创建一个进程池执行器
#     print("==============start===============")
#     excutor = ProcessPoolExecutor(3)

#     # 使用submit提交任务
#     taskIds = [n for n in range(1, 8)]
#     print(f'taskids = {taskIds}')
    
#     futures = [excutor.submit(work, taskId) for taskId in range(1,8)]

#     print([f.result() for f in as_completed(futures)])
#     excutor.shutdown(wait=True) # 阻塞等待excutor所有任务执行完毕
#     print("==============end===============")

# endregion

##############################
# 使用add_done_callback方法

# region
# from concurrent.futures import ProcessPoolExecutor, as_completed
# import os
# import time

# def work(n):
#     print(f'work正在执行{n}, pid = {os.getpid()}')
#     time.sleep(n % 3)
#     return f"work执行完成-> {n}"

# if __name__ == "__main__":
#     # 创建一个进程池执行器
#     print("==============start===============")
#     excutor = ProcessPoolExecutor(3)

#     def done_func(future):
#         print(f"回调执行【{future.result()}】")
#         return f"{future} 的回调"

#     # 使用submit提交任务
#     taskIds = [n for n in range(1, 8)]
#     print(f'taskids = {taskIds}')
    
#     futures = [excutor.submit(work, taskId).add_done_callback(done_func) for taskId in range(1,8)]

#     excutor.shutdown(wait=True) # 阻塞等待excutor所有任务执行完毕
#     print("futures = ", futures)
#     print("==============end===============")

# endregion

###############################
# 使用map 方法 批量提交任务
# region
# from concurrent.futures import ProcessPoolExecutor, as_completed
# import os
# import time

# def work(n):
#     print(f'work正在执行{n}, pid = {os.getpid()}')
#     time.sleep(n % 3)
#     return f"work执行完成-> {n}"

# if __name__ == "__main__":
#     # 创建一个进程池执行器
#     print("==============start===============")
#     excutor = ProcessPoolExecutor(3)


#     # 使用submit提交任务
#     results = excutor.map(work, [n for n in range(1,8)])
#     print([r for r in results])

    
#     excutor.shutdown(wait=True) # 阻塞等待excutor所有任务执行完毕
#     print("==============end===============")
# endregion

#######################################
# 使用with ， 离开with代码块，会自动进行 shutdown(wait=True)
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import time

def work(n):
    print(f'work正在执行{n}, pid = {os.getpid()}')
    time.sleep(n % 3)
    return f"work执行完成-> {n}"

if __name__ == "__main__":
    # 创建一个进程池执行器
    print("==============start===============")
    with ProcessPoolExecutor(3) as excutor:
        results = excutor.map(work, [n for n in range(1,8)])

    # excutor.shutdown(wait=True) # 阻塞等待excutor所有任务执行完毕
    print(f"results = {results}")
    print("==============end===============")