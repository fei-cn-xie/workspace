# 1. 文件的分类 
#   1. 纯文本文件 .txt .py .md .html
#   2. 二进制文件 .mp3 .mp4 .doc .jpg .png

###################################
# 2. 文件操作核心：open函数， 返回值是 【文件对象】
# open函数常用的3个核心参数：
#  2.1 file：要操作的文件路径
#  2.2 mode：文件打开的模式
#       r: 读取（默认值）
#       w: 写入，并先截断文件
#       x: 排他性创建，如果文件存在，则创建失败
#       a: 打开文件写入，如果文件存在，则追加内容
#       b: 二进制模式
#       t: 文本模式（默认值）
#       +: 打开文件用于更新（读取或者写入）
#  2.3 encoding: 字符编码
# region
# file_path = '2.python_all\\文件操作\\demo.txt'

# with open(file_path, 'r', encoding='utf-8') as f:
#     print(f.read())

# file = open(file=file_path, mode='rt', encoding='utf-8')
# res = file.read()
# print(repr(res)) # repr查看文件原始格式， 比如可以看到\n \t \r等

# file2 = open(file=file_path, mode='rt', encoding='utf-8')
# while(True):
#     result = file2.read(1)
#     if(result == ''): # 如果读取的是空字符串，则表示文件读取到最后了
#         break
#     print(f"[{repr(result)}]", end='')


# file.close()
# file2.close()
# endregion

#####################################
# 3. 上下文管理器
#    3.1 语法： with 获取上下文管理器的表达式 as 变量:
                        # 操作
#   3.2 两个协议：
#       (1) __enter__
#       (2) __exit__
class Test:
    def __init__(self, name) -> None:
        self.name = name

    def speak(self):
        return self.name

    def __enter__(self):
        print("===================start Test")
        return self

    def __exit__(self, exc_type, exc, tb):
        print("===================end")
        if(exc):
            print(f'异常类型：{exc_type}')
            print(f'异常对象：{exc}')
            print(f'异常追踪堆栈信息：{tb}')
            return True # 返回True表示处理了异常， 不再抛出

with Test("tom") as t, Test("jack") as t2:
    print(t.speak())
    t.tt()

