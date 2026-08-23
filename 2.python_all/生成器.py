# 1. 生成器函数：如果函数中出现了yield， 那么该函数就是【生成器函数】. 不论yield存在哪个位置，只要有这一条件就成立
# 2. 生成器对象：调用【生成器函数】时，函数不会立即执行，会返回一个【生成器对象】
# region

from typing import Generator

# def demo():
#     print('demo start')
#     a = 100
#     yield f'yield {a}'
#     print(a)
#     a += 10
#     return 0

# d = demo()
# print(d)
# endregion

###################
# 写在生成器函数中的代码，需要通过生成器对象来执行
# 1. 调用生成器对象中的 __next__方法， 会让 生成器函数中的代码开始执行
# 2. 当生成器函数中的代码开始执行后， 遇到yield后会暂停执行，并在内部记录‘暂停’位置
# 3. 遇到return时，会抛出StopIterator异常，并将return 后的表达式，作为异常信息
# 4. yield 后面的表达式就是本次__next__方法的返回值，如果没有就是None
# region

# print(next(d))
# print("continue...")
# # next(d)

# print("*="*20)

# def demo2():
#     for i in range(5):
#         yield 100 + i
#     print("over")
#     return 0 # for底层循环会遇到StopIteration 会break

# d2 = demo2()

# for item in demo2():
#     print(item)



# endregion

############################
# yield 能够写在循环里
# region
# def create_car(total):
#     for index in range(total):
#         yield f'我是第{index} 台车'

# cars = create_car(5)
# print(f'cars = {cars}')

# print(f"{next(cars)}")

# for c in cars:
#     print(c)
# endregion

###########################
# yield from能把 一个可迭代对象 中的内容依次 yield出去
# region
# def demo5():
#     yield from [2,3,4,5,6,7]
#     print("over")

# for item in demo5():
#     print(item)

# endregion


#################
# 6.使用  生成器.send(value), 可以让生成器继续执行的同时，给上一次yield传值
#   注意：第一次调用生成器时，如果使用send，只能传入None
# region

# def demo6() -> Generator[str, str, int]:
#     print("======== start ===========")
#     a:str = yield 'first yield'
#     print(a)
#     b = yield 'second yield'
#     print(b)
#     c:str = yield 'third yield'
#     print(c)
#     return 444

# gen = demo6()

# # print(gen.send(None))
# print(next(gen))
# print(gen.send(242))
# print(gen.send(333))
# # print(gen.send(444))


# endregion

##############
# 生成器的斐波那契
# region
# def fibo(num):
#     cur = 1
#     last = 1
#     for i in range(num):
#         if(i < 2):
#             value = 1
#         else:
#             value = cur + last
#         last = cur
#         cur = value
#         yield value

# f = fibo(10)
# for item in f:
#     print(item)
# endregion


####################
# 生成器表达式
nums = [1,3,4,5,6,7]
result = (n * 10 for n in nums)
print(result)
for item in result:
    print(item)
